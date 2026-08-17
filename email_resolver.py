"""Resolve one person's work email by the cheapest path that can pay.

The waterfall, per person:

  1. KNOWN / PUBLISHED address (from research) -> verify once.
       VERIFIED/HIGH -> done. MEDIUM/LOW -> keep it as a fallback but KEEP GOING,
       so Finder can beat it. A published address is never discarded.
  2. EMAIL FINDER (1 search credit, free on a null miss) -> keep only a result
       with `source_type == "found"` and sources. Then:
         - Finder's own verification says valid  -> VERIFIED (free, already in the reply)
         - catch-all domain                      -> HIGH  (verifier can't help; sources are proof)
         - score >= 90                           -> VERIFIED (trust; don't re-test the strong ones)
         - weak score on a checkable domain      -> VERIFY once (a live check adds info) -> grade
  3. PROBER (email_prober.py) -> catch-all control + ranked pattern probes.
  4. Nothing graded -> GUESSED, blank email, LinkedIn is the route.

We keep the highest-grade result found; once we hold HIGH or better we stop.
A guess is never returned as an address.

    ./.venv/bin/python email_resolver.py --domain openai.com --first Greg --last Brockman
    ./.venv/bin/python email_resolver.py --domain co.com --first X --last Y --known real@co.com
    ./.venv/bin/python email_resolver.py --batch daily/2026-08-16/candidates.json
    ./.venv/bin/python email_resolver.py --domain X --first F --last L --dry-run
    ./.venv/bin/python email_resolver.py --self-test
"""
import argparse
import json
import sys
import time
from pathlib import Path

import requests

from email_prober import (
    load_key, verify, catch_all_control, grade, pattern_from_known,
    PATTERNS, API,
)

ROOT = Path(__file__).resolve().parent
GRADE_RANK = {"VERIFIED": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1}


def higher(a, b):
    """Return the higher-ranked grade of two (either may be None)."""
    return a if GRADE_RANK.get(a, 0) >= GRADE_RANK.get(b, 0) else b


# ---------------------------------------------------------------------------
# Email Finder
# ---------------------------------------------------------------------------

def finder(domain, first, last, key):
    """One Email Finder call. Returns Hunter's data dict, or {'_error':...}.

    Charges 1 search credit if it returns an email (found OR generated);
    a null result is free.
    """
    try:
        r = requests.get("%s/email-finder" % API,
                         params={"domain": domain, "first_name": first,
                                 "last_name": last, "api_key": key}, timeout=30)
        payload = r.json()
    except Exception as e:
        return {"_error": str(e)[:60]}
    if "errors" in payload:
        return {"_error": payload["errors"][0].get("details", "")[:60]}
    return payload.get("data", {})


def finder_charged(d):
    """A search credit is spent iff the finder returned an email."""
    return bool(d and not d.get("_error") and d.get("email"))


def finder_signals(d):
    """Source_type gate. Returns {email, score, accept_all, fverify} or None.

    `found` + sources = a real sighting. `generated` / no sources = a blind
    pattern guess, thrown away no matter how high the score.
    """
    if not d or d.get("_error"):
        return None
    email = d.get("email")
    if not email:
        return None                                  # null miss (free)
    if d.get("source_type") != "found" or not (d.get("sources") or []):
        return None                                  # generated / unsourced -> junk
    return {"email": email, "score": d.get("score") or 0,
            "accept_all": bool(d.get("accept_all")),
            "fverify": (d.get("verification") or {}).get("status")}


def grade_finder_hit(sig, key, cost):
    """Grade a sourced Finder hit. Test with the Verifier only when a live check
    can add information (weak score, checkable domain). Returns (grade, method,
    note) or (None, None, None) to discard and fall through to the prober."""
    email, score, aa, fv = sig["email"], sig["score"], sig["accept_all"], sig["fverify"]

    if fv == "valid":                                 # Finder already SMTP-checked it (free)
        return "VERIFIED", "finder", "finder-verified"
    if fv == "invalid":
        return None, None, None                       # its own check says dead -> discard
    if aa:                                            # catch-all: verifier can't disambiguate
        return "HIGH", "finder", "catch-all, sourced"
    if score >= 90:                                   # strong: trust, don't re-test
        return "VERIFIED", "finder", "score %d, sourced" % score

    # Weak score on a checkable domain: a live Verify genuinely adds information.
    d = verify(email, key)
    cost["verify"] += 1
    st = (d or {}).get("status")
    vs = (d or {}).get("score") or 0
    if st == "valid" and not (d or {}).get("accept_all"):
        g = "VERIFIED" if vs >= 90 else "HIGH" if vs >= 70 else "MEDIUM"
        return g, "finder+verify", "verified %d" % vs
    if (d or {}).get("accept_all") or (d or {}).get("block") or st == "unknown":
        return "MEDIUM", "finder", "verify inconclusive"   # test couldn't decide -> keep, flag
    return None, None, None                           # live check says invalid -> discard


# ---------------------------------------------------------------------------
# The prober (quiet wrapper over email_prober's verifier logic)
# ---------------------------------------------------------------------------

def prober_step(domain, first, last, known, key, max_probes, cost):
    """Catch-all control + ranked pattern probes. Returns (email, note) or (None, note)."""
    trustworthy, why = catch_all_control(domain, key)
    cost["verify"] += 1
    if not trustworthy:
        return None, "catch-all"

    f, l = first.lower().strip(), last.lower().strip()
    if known:
        tmpl, name = pattern_from_known(known, f, l)
        if tmpl:
            cands = [(tmpl.format(first=f, last=l, f=f[:1], l=l[:1]) + "@" + domain, name)]
        else:
            cands = [(t.format(first=f, last=l, f=f[:1], l=l[:1]) + "@" + domain, n)
                     for t, n in PATTERNS]
    else:
        cands = [(t.format(first=f, last=l, f=f[:1], l=l[:1]) + "@" + domain, n)
                 for t, n in PATTERNS]

    for email, name in cands[:max_probes]:
        d = verify(email, key)
        cost["verify"] += 1
        g = grade(d, trustworthy)
        if g:
            return email, "%s (probe:%s)" % (g, name)
    return None, "no pattern verified"


# ---------------------------------------------------------------------------
# The waterfall
# ---------------------------------------------------------------------------

def resolve(person, key, max_probes=4, dry=False):
    """Run the full waterfall for one person. Returns a result record."""
    name = person.get("name") or ("%s %s" % (person.get("first", ""), person.get("last", ""))).strip()
    domain = (person.get("domain") or "").lower().strip()
    first = person.get("first") or (name.split()[0] if name else "")
    last = person.get("last") or (name.split()[-1] if len(name.split()) > 1 else "")
    known = person.get("known") or person.get("published_email")
    cost = {"search": 0, "verify": 0}

    def out(email, gr, method, note=""):
        return {"name": name, "email": email or "", "grade": gr, "method": method,
                "note": note, "cost_search": cost["search"], "cost_verify": cost["verify"]}

    if dry:
        plan = "published(+finder if weak)" if known else "finder->prober"
        return out(known or "", "DRY", plan, "domain=%s" % domain)

    best = [None]   # (email, grade, method, note)

    def consider(email, g, method, note):
        if g and (best[0] is None or GRADE_RANK.get(g, 0) > GRADE_RANK.get(best[0][1], 0)):
            best[0] = (email, g, method, note)

    def have_high():
        return best[0] is not None and GRADE_RANK.get(best[0][1], 0) >= GRADE_RANK["HIGH"]

    # STEP 1 - known / published address
    if known:
        kg = person.get("known_grade")               # research's source grade (team page=VERIFIED, site=HIGH, ...)
        d = verify(known, key)                        # one call: gives liveness AND the accept_all flag
        cost["verify"] += 1
        st = (d or {}).get("status")
        if (d or {}).get("accept_all"):
            # Catch-all: Hunter's "valid" is meaningless here (Hunter says so) -> grade by the source.
            consider(known, kg or "HIGH", "published", "catch-all; graded by source")
        elif st == "valid":
            consider(known, higher(grade(d, True), kg), "published",
                     "verified score %s" % (d or {}).get("score"))
        elif st == "invalid":
            consider(known, "LOW", "published", "verify says dead")   # confirmed bounce -> keep looking
        else:
            consider(known, higher(kg, "MEDIUM"), "published", "verify inconclusive")
        if have_high():
            return out(*best[0])                      # VERIFIED/HIGH published -> done

    # STEP 2 - Email Finder
    if domain:
        fd = finder(domain, first, last, key)
        if finder_charged(fd):
            cost["search"] += 1
        sig = finder_signals(fd)
        if sig:
            g, method, note = grade_finder_hit(sig, key, cost)
            if g:
                consider(sig["email"], g, method, note)
        if have_high():
            return out(*best[0])

    # STEP 3 - prober fallback
    if domain and not have_high():
        email, note = prober_step(domain, first, last, known, key, max_probes, cost)
        if email:
            consider(email, note.split(" ")[0], "prober", note)

    # STEP 4 - best result, else GUESSED
    if best[0]:
        return out(*best[0])
    return out("", "GUESSED", "none", "no address found")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_row(r):
    print("%-22s %-32s %-9s %-14s %s" % (
        r["name"][:22], r["email"][:32], r["grade"], r["method"], r["note"]))


def run_batch(path, key, max_probes, dry):
    people = json.loads(Path(path).read_text())
    results = []
    print("%-22s %-32s %-9s %-14s %s" % ("NAME", "EMAIL", "GRADE", "METHOD", "NOTE"))
    print("-" * 104)
    for p in people:
        r = resolve(p, key, max_probes=max_probes, dry=dry)
        results.append(r)
        print_row(r)
        time.sleep(0.3)
    folder = Path(path).parent
    (folder / "emails.json").write_text(json.dumps(results, indent=2))
    (folder / "hunter-receipt.json").write_text(json.dumps(
        {"searches": sum(r["cost_search"] for r in results),
         "verifications": sum(r["cost_verify"] for r in results),
         "people": len(results)}, indent=2))
    s = sum(r["cost_search"] for r in results)
    v = sum(r["cost_verify"] for r in results)
    graded = sum(1 for r in results if r["email"])
    print("-" * 104)
    print("%d people, %d with an address. Cost: %d searches, %d verifications."
          % (len(results), graded, s, v))
    print("Wrote %s and hunter-receipt.json" % (folder / "emails.json"))


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", help="path to candidates.json")
    ap.add_argument("--domain")
    ap.add_argument("--first")
    ap.add_argument("--last")
    ap.add_argument("--known", help="a known/published address to verify first")
    ap.add_argument("--max-probes", type=int, default=4)
    ap.add_argument("--dry-run", action="store_true", help="show the plan, spend nothing")
    ap.add_argument("--self-test", action="store_true", help="offline logic check, no network")
    args = ap.parse_args()

    if args.self_test:
        return self_test()

    key = None if args.dry_run else load_key()

    if args.batch:
        run_batch(args.batch, key, args.max_probes, args.dry_run)
        return 0

    if not args.domain:
        sys.exit("ERROR: pass --batch, or --domain (+ --first/--last), or --self-test")

    person = {"domain": args.domain, "first": args.first, "last": args.last,
              "known": args.known,
              "name": ("%s %s" % (args.first or "", args.last or "")).strip()}
    r = resolve(person, key, max_probes=args.max_probes, dry=args.dry_run)
    print("%-22s %-32s %-9s %-14s %s" % ("NAME", "EMAIL", "GRADE", "METHOD", "NOTE"))
    print_row(r)
    return 0 if r["email"] or r["grade"] == "DRY" else 1


# ---------------------------------------------------------------------------
# Offline self-test: exercises the waterfall against canned responses.
# ---------------------------------------------------------------------------

def self_test():
    import email_resolver as M
    orig = (M.verify, M.finder, M.catch_all_control)
    fails = []

    def case(desc, finder_ret, verify_map, catchall, person,
             want_email, want_method, want_grade=None):
        M.finder = lambda *a, **k: finder_ret
        M.verify = lambda email, key: verify_map.get(email, {"status": "invalid", "score": 0})
        M.catch_all_control = lambda domain, key: catchall
        r = M.resolve(person, key="x", max_probes=4)
        ok = (bool(r["email"]) == bool(want_email)) and r["method"] == want_method
        if want_email:
            ok = ok and r["email"] == want_email
        if want_grade:
            ok = ok and r["grade"] == want_grade
        print("  %s %-42s -> %-24s %-13s %s%s" % (
            "PASS" if ok else "FAIL", desc, r["email"] or "(blank)", r["method"], r["grade"],
            "" if ok else "  [want %s/%s/%s]" % (want_email or "(blank)", want_method, want_grade)))
        if not ok:
            fails.append(desc)

    p = {"name": "Test Person", "first": "Test", "last": "Person", "domain": "co.com"}
    src = [{"domain": "a.com"}]
    print("SELF-TEST (offline, no credits spent)\n")

    # Finder's own check says valid -> VERIFIED, free
    case("finder verification=valid -> VERIFIED",
         {"email": "t@co.com", "source_type": "found", "score": 40, "accept_all": False,
          "sources": src, "verification": {"status": "valid"}},
         {}, (True, "ok"), p, "t@co.com", "finder", "VERIFIED")

    # Strong score, not catch-all -> VERIFIED, no re-test
    case("strong score -> VERIFIED (no verify)",
         {"email": "t@co.com", "source_type": "found", "score": 95, "accept_all": False,
          "sources": src, "verification": {"status": None}},
         {}, (True, "ok"), p, "t@co.com", "finder", "VERIFIED")

    # Generated guess -> discarded -> prober rescues
    case("generated -> discarded -> prober",
         {"email": "g@co.com", "source_type": "generated", "score": 88, "accept_all": True,
          "sources": [], "verification": {"status": None}},
         {"test@co.com": {"status": "valid", "score": 92}},
         (True, "ok"), p, "test@co.com", "prober")

    # Weak score, checkable domain -> live verify confirms -> finder+verify
    case("weak -> live verify valid -> kept",
         {"email": "w@co.com", "source_type": "found", "score": 55, "accept_all": False,
          "sources": src, "verification": {"status": None}},
         {"w@co.com": {"status": "valid", "score": 93}},
         (True, "ok"), p, "w@co.com", "finder+verify", "VERIFIED")

    # Weak on a CATCH-ALL -> no verify spent -> HIGH
    case("weak on catch-all -> HIGH, no verify",
         {"email": "c@co.com", "source_type": "found", "score": 70, "accept_all": True,
          "sources": src, "verification": {"status": None}},
         {}, (True, "ok"), p, "c@co.com", "finder", "HIGH")

    # Weak, live verify says INVALID -> discard -> prober finds pattern
    case("weak + live invalid -> prober",
         {"email": "w@co.com", "source_type": "found", "score": 55, "accept_all": False,
          "sources": src, "verification": {"status": None}},
         {"w@co.com": {"status": "invalid", "score": 0},
          "test.person@co.com": {"status": "valid", "score": 85}},
         (True, "ok"), p, "test.person@co.com", "prober")

    # GAP 1: published only MEDIUM -> keep going -> Finder beats it
    case("published MEDIUM -> finder beats it",
         {"email": "f@co.com", "source_type": "found", "score": 95, "accept_all": False,
          "sources": src, "verification": {"status": "valid"}},
         {"pub@co.com": {"status": "valid", "score": 60}},
         (True, "ok"),
         {"name": "Test Person", "first": "Test", "last": "Person", "domain": "co.com",
          "known": "pub@co.com"},
         "f@co.com", "finder", "VERIFIED")

    # Published HIGH -> stop, Finder never consulted
    case("published HIGH -> stops early",
         {"email": "f@co.com", "source_type": "found", "score": 95, "accept_all": False,
          "sources": src, "verification": {"status": "valid"}},
         {"pub@co.com": {"status": "valid", "score": 78}},
         (True, "ok"),
         {"name": "Test Person", "first": "Test", "last": "Person", "domain": "co.com",
          "known": "pub@co.com"},
         "pub@co.com", "published", "HIGH")

    # Team-page address (source VERIFIED) on a CATCH-ALL domain -> stays VERIFIED
    case("team-page on catch-all -> stays VERIFIED",
         {"email": None},
         {"pub@co.com": {"status": "valid", "score": 50, "accept_all": True}},
         (True, "ok"),
         {"name": "T P", "first": "T", "last": "P", "domain": "co.com",
          "known": "pub@co.com", "known_grade": "VERIFIED"},
         "pub@co.com", "published", "VERIFIED")

    # Published on catch-all, no source grade -> HIGH
    case("published catch-all, no source grade -> HIGH",
         {"email": None},
         {"pub@co.com": {"status": "valid", "score": 50, "accept_all": True}},
         (True, "ok"),
         {"name": "T P", "first": "T", "last": "P", "domain": "co.com",
          "known": "pub@co.com"},
         "pub@co.com", "published", "HIGH")

    # Published address that verifies DEAD -> LOW -> finder rescues with a live one
    case("published dead -> finder rescues",
         {"email": "f@co.com", "source_type": "found", "score": 95, "accept_all": False,
          "sources": src, "verification": {"status": "valid"}},
         {"pub@co.com": {"status": "invalid", "score": 0}},
         (True, "ok"),
         {"name": "T P", "first": "T", "last": "P", "domain": "co.com",
          "known": "pub@co.com"},
         "f@co.com", "finder", "VERIFIED")

    # Nothing anywhere -> GUESSED
    case("catch-all + null finder -> GUESSED",
         {"email": None, "sources": []},
         {}, (False, "accept_all"), p, "", "none", "GUESSED")

    M.verify, M.finder, M.catch_all_control = orig
    print("\n%s" % ("ALL PASS" if not fails else "FAILURES: %s" % fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main())

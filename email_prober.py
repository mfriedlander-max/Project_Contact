"""Find and grade a work email without spending a Hunter search.

This systematises what the runs discovered by hand: the reason a pattern guess is
worthless is that you cannot tell a real mailbox from a domain that accepts
everything. Control for that and the same guess becomes evidence.

    ./.venv/bin/python email_prober.py --domain calendly.com --first Tope --last Awotona
    ./.venv/bin/python email_prober.py --domain vercel.com --catchall-only
    ./.venv/bin/python email_prober.py --domain uala.com.ar --first Pierpaolo --last Barbieri --known someone@uala.com.ar

Order of operations, and the order matters:

1. **Catch-all control.** Probe a nonsense mailbox. If the domain accepts it, no
   verification on that domain means anything and every result is GUESSED.
2. **Known-address pattern.** If you already have one real address at the domain,
   infer the format from it and test only that. One candidate, high prior.
3. **Ranked candidates.** Otherwise try the common formats in order of real-world
   frequency and stop at the first that verifies.

Verification uses Hunter's email-verifier, which costs 0.5 credit rather than the
1 credit an email-finder search costs, so this is cheaper as well as better.

Grades match the sheet's Email Confidence column exactly.
"""
import argparse
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
API = "https://api.hunter.io/v2"

# Ordered by how often they occur in the wild, most common first.
PATTERNS = [
    ("{first}", "first"),
    ("{first}.{last}", "first.last"),
    ("{f}{last}", "flast"),
    ("{first}{last}", "firstlast"),
    ("{first}_{last}", "first_last"),
    ("{f}.{last}", "f.last"),
    ("{last}", "last"),
    ("{first}{l}", "firstl"),
]

NONSENSE = "zqx9plarb7v"      # a mailbox no organisation has


def load_key():
    env = ROOT / "credentials" / ".env"
    if env.exists():
        for line in env.read_text().splitlines():
            if line.startswith("HUNTER_API_KEY=") and "HUNTER_API_KEY" not in os.environ:
                os.environ["HUNTER_API_KEY"] = line.split("=", 1)[1].strip()
    key = os.getenv("HUNTER_API_KEY")
    if not key:
        sys.exit("ERROR: HUNTER_API_KEY not set and not in credentials/.env")
    return key


def verify(email, key):
    """One verification. Returns Hunter's data dict, or None on API error."""
    try:
        r = requests.get("%s/email-verifier" % API,
                         params={"email": email, "api_key": key}, timeout=30)
        payload = r.json()
    except Exception as e:
        print("   ! request failed for %s: %s" % (email, str(e)[:60]))
        return None
    if "errors" in payload:
        detail = payload["errors"][0].get("details", "")
        print("   ! %s: %s" % (email, detail[:70]))
        return None
    return payload.get("data", {})


def catch_all_control(domain, key):
    """Is a 'valid' result on this domain meaningful at all?

    Returns (trustworthy: bool, explanation: str).
    """
    probe = "%s@%s" % (NONSENSE, domain)
    d = verify(probe, key)
    if d is None:
        return False, "control test could not be completed (Hunter error), so verification is unproven"

    status = d.get("status")
    accept_all = d.get("accept_all")

    if accept_all:
        return False, "domain is accept_all: it says yes to every address, so verification proves nothing"
    if status in ("valid", "accept_all"):
        return False, "domain accepted a nonsense mailbox, so verification proves nothing"
    return True, "domain rejected a nonsense mailbox and accept_all is false, so a valid result means the mailbox exists"


def grade(d, trustworthy):
    """Map a verification result onto the sheet's Email Confidence values."""
    if d is None:
        return None
    status = d.get("status")
    score = d.get("score") or 0
    if status != "valid":
        return None
    if not trustworthy:
        return None                      # a valid result we cannot believe is not a result
    if score >= 90:
        return "VERIFIED"
    if score >= 70:
        return "HIGH"
    return "MEDIUM"


def pattern_from_known(known, first, last):
    """Infer the org's format from one address that is already confirmed real."""
    local = known.split("@")[0].lower()
    f, l = first.lower(), last.lower()
    for tmpl, name in PATTERNS:
        if tmpl.format(first=f, last=l, f=f[:1], l=l[:1]) == local:
            return tmpl, name
    return None, None


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--domain", required=True)
    ap.add_argument("--first")
    ap.add_argument("--last")
    ap.add_argument("--known", help="a known-real address at this domain, to infer the format")
    ap.add_argument("--catchall-only", action="store_true",
                    help="just run the control test and stop")
    ap.add_argument("--max-probes", type=int, default=4,
                    help="cap on candidates tried (default 4)")
    args = ap.parse_args()

    key = load_key()
    domain = args.domain.lower().strip()

    print("Domain: %s" % domain)
    print("1. Catch-all control")
    trustworthy, why = catch_all_control(domain, key)
    print("   %s" % why)

    if args.catchall_only:
        print("\nVerdict: verification on this domain is %s."
              % ("MEANINGFUL" if trustworthy else "MEANINGLESS"))
        return 0 if trustworthy else 1

    if not (args.first and args.last):
        sys.exit("ERROR: --first and --last are required unless --catchall-only")

    if not trustworthy:
        print("\nStopping. Every candidate on this domain would verify as valid whether or not")
        print("it exists, so probing produces guesses, not evidence.")
        print("\nRESULT: no address. Grade GUESSED, leave the Email cell empty.")
        print("Try public commits, a personal site, or Hunter's email-finder instead.")
        return 1

    f, l = args.first.lower().strip(), args.last.lower().strip()

    if args.known:
        tmpl, name = pattern_from_known(args.known, f, l)
        if tmpl:
            print("2. Format inferred from %s: %s" % (args.known, name))
            candidates = [(tmpl.format(first=f, last=l, f=f[:1], l=l[:1]) + "@" + domain, name)]
        else:
            print("2. %s matches no known pattern, falling back to ranked candidates" % args.known)
            candidates = [(t.format(first=f, last=l, f=f[:1], l=l[:1]) + "@" + domain, n)
                          for t, n in PATTERNS]
    else:
        print("2. No known address, trying ranked candidates")
        candidates = [(t.format(first=f, last=l, f=f[:1], l=l[:1]) + "@" + domain, n)
                      for t, n in PATTERNS]

    print("3. Probing (max %d)" % args.max_probes)
    for email, name in candidates[:args.max_probes]:
        d = verify(email, key)
        g = grade(d, trustworthy)
        status = (d or {}).get("status", "error")
        score = (d or {}).get("score", "")
        print("   %-38s %-12s score=%-4s %s" % (email, status, score, g or ""))
        if g:
            print("\nRESULT: %s" % email)
            print("Grade:  %s  (pattern %s, control test passed)" % (g, name))
            return 0
        time.sleep(1)

    print("\nRESULT: no address found across %d candidates." % min(args.max_probes, len(candidates)))
    print("Grade GUESSED and leave the Email cell empty.")
    return 1


if __name__ == "__main__":
    sys.exit(main())

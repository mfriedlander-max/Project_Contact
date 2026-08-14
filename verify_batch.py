"""Check a batch against every rule the skill claims to enforce.

Run after any daily-outreach run. Exits non-zero if anything fails, so a run can
be graded without reading it.

    ./.venv/bin/python verify_batch.py                 # today
    ./.venv/bin/python verify_batch.py --date 2026-08-14

Every check here exists because a real run got it wrong at least once.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parent

BANDS = {
    "elite-brevity-10min": (50, 65),
    "elite-builder-10min": (90, 100),
    "cold-midd-personal-10min": (90, 95),
    "elite-decision-10min": (90, 95),
    "referral-15min": (90, 95),
}

BANNED = ["i came across", "i noticed", "your remarkable", "your impressive",
          "i would be honored", "resonates with me", "i hope this finds you"]

CONFIDENCE = {"VERIFIED", "HIGH", "MEDIUM", "LOW", "GUESSED"}

COLUMNS = ["Name", "Status", "Email", "Email Confidence", "Company", "Role", "Industry",
           "Phone", "LinkedIn", "Source", "Campaign", "Email Variant", "Personalized Insert",
           "Sent Date", "Last Contacted", "Meeting Notes", "Ask Them About",
           "What They Can Offer Me", "What I Can Offer Them", "Notion Page"]

# Facts that were true once and are not now. Any of these in an email is a stale-fact bug.
STALE = ["entrepreneur first", "heading to buenos aires", "next fall to study", "motiontech"]

results = []


def check(name, passed, detail=""):
    results.append((name, passed, detail))
    print("  %s %-46s %s" % ("PASS" if passed else "FAIL", name, detail))
    return passed


def body_of(text):
    m = re.search(r"^Hi [A-Z][\w'\-]+,", text, re.M)
    if not m:
        return None
    start = m.start()
    tail = text[start:]
    m2 = re.search(r"\nMax\s*$|\nMax\n", tail)
    if not m2:
        idx = tail.rfind("Max")
        return tail[:idx + 3] if idx > 0 else None
    return tail[:m2.end()].rstrip()


def load_drafts(folder):
    out = []
    for f in sorted(folder.glob("*.md")):
        if re.match(r"^\d+-", f.name) is None:
            continue
        t = f.read_text()
        body = body_of(t)
        if body is None:
            continue
        var = re.search(r"\*{0,2}Variant:?\*{0,2}\s*`?([a-z0-9\-]+)", t)
        subj = re.search(r"\*{0,2}Subject:?\*{0,2}\s*(.+)", t)
        out.append({
            "file": f.name,
            "body": body,
            "words": len(body.split()),
            "variant": var.group(1) if var else None,
            "subject": subj.group(1).strip().strip("*` ") if subj else None,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=str(date.today()))
    args = ap.parse_args()

    folder = ROOT / "daily" / args.date
    print("BATCH VERIFICATION - %s\n" % args.date)
    if not folder.exists():
        print("FAIL  no folder at %s" % folder)
        return 1

    drafts = load_drafts(folder)
    print("Drafts found: %d\n" % len(drafts))
    if not drafts:
        print("FAIL  no parsable drafts")
        return 1

    print("EMAIL COPY")
    for d in drafts:
        band = BANDS.get(d["variant"], (90, 95))
        ok = band[0] <= d["words"] <= band[1]
        check("%s word count in band" % d["file"][:22], ok,
              "%d words, band %d-%d, variant %s" % (d["words"], band[0], band[1], d["variant"]))

    check("no em dashes", all("—" not in d["body"] for d in drafts))
    bad = [(d["file"], p) for d in drafts for p in BANNED if p in d["body"].lower()]
    check("no banned AI phrases", not bad, str(bad[:3]) if bad else "")
    stale = [(d["file"], s) for d in drafts for s in STALE if s in d["body"].lower()]
    check("no stale personal facts", not stale, str(stale[:3]) if stale else "")

    subs = [d["subject"] for d in drafts if d["subject"]]
    check("every draft has a subject", len(subs) == len(drafts))
    dupes = [s for s, c in Counter(subs).items() if c > 1]
    check("subject lines are distinct", not dupes, "repeated: %s" % dupes if dupes else "")

    # The Middlebury wedge may only appear where a connection is evidenced.
    midd_subj = [d for d in drafts if d["subject"] and "middlebury" in d["subject"].lower()]
    research = ""
    for rf in folder.glob("research*.md"):
        research += rf.read_text().lower()
    wrong = []
    for d in midd_subj:
        name = re.sub(r"^\d+-", "", d["file"]).replace(".md", "").replace("-", " ")
        first = name.split()[0]
        near = [ln for ln in research.splitlines() if first in ln]
        if not any(("middlebury" in ln or "midd " in ln) for ln in near):
            wrong.append(d["file"])
    check("Middlebury subject only where evidenced", not wrong,
          "unevidenced: %s" % wrong if wrong else "%d of %d use it" % (len(midd_subj), len(drafts)))

    variants = [d["variant"] for d in drafts]
    check("more than one variant used", len(set(variants)) > 1,
          "used: %s" % sorted(set(v for v in variants if v)))

    print("\nARTIFACTS")
    check("research notes written", any(folder.glob("research*.md")))
    check("batch summary written", any(folder.glob("batch*.md")))
    dj = list(folder.glob("drafts*.json"))
    check("drafts.json written (python drafter path)", bool(dj))
    if dj:
        try:
            queued = json.loads(dj[0].read_text())
            ok = all(("@" in q.get("to", "")) for q in queued)
            check("every queued draft has a real address", ok, "%d queued" % len(queued))
        except Exception as e:
            check("drafts.json parses", False, str(e)[:50])

    print("\nSHEET")
    cfg = json.loads((ROOT / "outlook_config.json").read_text())
    creds = Credentials.from_service_account_file(
        str(ROOT / "credentials" / "google_sheets_key.json"),
        scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
    sh = gspread.authorize(creds).open_by_key(cfg["google_sheet_id"])

    tc = sh.worksheet("To Contact")
    v = tc.get_all_values()
    check("header matches the 20-column schema", v[0] == COLUMNS)

    names_all, rows_today = [], []
    for ws in sh.worksheets():
        for r in ws.get_all_values()[1:]:
            if r and r[0].strip():
                names_all.append(r[0].strip())
    dup = [n for n, c in Counter(names_all).items() if c > 1]
    check("no duplicates anywhere on the sheet", not dup, str(dup[:4]) if dup else "%d people" % len(names_all))

    body_rows = [r for r in v[1:] if any(c.strip() for c in r)]
    top = body_rows[:len(drafts)]
    campaign_col = COLUMNS.index("Campaign")
    at_top = all(len(r) > campaign_col and r[campaign_col].startswith("daily-") for r in top)
    check("today's batch is at the top of To Contact", at_top)

    filled = {c: 0 for c in ["Email Confidence", "Company", "Role", "Industry",
                             "LinkedIn", "Source", "Campaign", "Email Variant",
                             "Personalized Insert", "Meeting Notes"]}
    for r in top:
        for c in filled:
            i = COLUMNS.index(c)
            if i < len(r) and r[i].strip():
                filled[c] += 1
    for c, n in filled.items():
        check("%s filled on every row" % c, n == len(top), "%d/%d" % (n, len(top)))

    ci = COLUMNS.index("Email Confidence")
    ei = COLUMNS.index("Email")
    badconf = [r[0] for r in top if r[ci].strip() and r[ci].strip() not in CONFIDENCE]
    check("Email Confidence values are valid", not badconf, str(badconf) if badconf else "")
    contradiction = [r[0] for r in top if r[ei].strip() and r[ci].strip() == "GUESSED"]
    check("no row has both an Email and GUESSED", not contradiction, str(contradiction) if contradiction else "")

    print("\nLOCAL LOG")
    log = list(csv.DictReader(open(ROOT / "contacts-log.csv")))
    logn = {r["Name"].strip() for r in log}
    sheetn = set(names_all)
    check("contacts-log.csv matches the sheet", logn == sheetn,
          "log %d, sheet %d" % (len(logn), len(sheetn)))

    passed = sum(1 for _, p, _ in results if p)
    total = len(results)
    print("\n%s  %d/%d checks passed" % ("ALL PASS" if passed == total else "FAILURES PRESENT",
                                         passed, total))
    if passed != total:
        print("\nFailed:")
        for n, p, d in results:
            if not p:
                print("  - %s  %s" % (n, d))
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

# Project_Contact

Max Friedlander's networking system. Find people worth knowing, write each one a researched
email, track the relationship in a Google Sheet.

Rewritten 2026-08-13. The previous version described a Python pipeline and a 22-column sheet,
**both of which are gone.** If you are reading instructions about `email_drafter.py`,
`Connection Level`, `Email Status`, or availability windows, they are stale.

## How this works now

The daily routine is a skill, not a pipeline. Read
**`.claude/skills/daily-outreach/SKILL.md`** and do the work directly: research the people,
write the emails, file them in the sheet. There is no script to invoke.

`README.md` is the full description of the system, for a human reader.

## The sheet is the database

**Middlebury Connection Tracker** (`google_sheet_id` in `outlook_config.json`), six tabs sharing
one 20-column schema:

```
To Contact -> Message Sent -> Didn't Connect / Connected -> In Touch -> Friends
```

**The tab a person is in IS their status.** There is no separate status field, so there is
nothing to fall out of sync. Column 2, `Status`, mirrors the tab as a coloured label, and
changing it moves the row.

```
Name | Status | Email | Email Confidence | Company | Role | Industry | Phone | LinkedIn |
Source | Campaign | Email Variant | Personalized Insert | Sent Date | Last Contacted |
Meeting Notes | Ask Them About | What They Can Offer Me | What I Can Offer Them | Notion Page
```

`apps-script/RowMover.gs` (installed in the sheet as "Sheet Mover") performs the move. **It
copies by column position**, so every tab must keep identical headers in identical order. Run
its `validateHeaders()` after any schema change; `repairStatusLabels()` fixes labels that drift
from hand-pasted rows.

As of 2026-08-13: 81 people, no duplicates, every Status matching its tab.

### Access

Service account key at `credentials/google_sheets_key.json` (gitignored, has edit rights).
Interpreter with `gspread`: `./.venv/bin/python`. Nothing is installed globally.

```python
import json, gspread
from google.oauth2.service_account import Credentials
cfg = json.load(open('outlook_config.json'))
creds = Credentials.from_service_account_file(
    'credentials/google_sheets_key.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets'])
sh = gspread.authorize(creds).open_by_key(cfg['google_sheet_id'])
```

Secrets load from `credentials/.env` (gitignored): `set -a; . ./credentials/.env; set +a`.
A cron-triggered run does **not** source the shell profile, so never rely on it.

## Writing emails

Every email belongs to a variant in `variants/`, and its id goes in the sheet's **Email
Variant** column. That column is the only link between a send and its outcome, so it is never
left blank.

| id | when | ask |
|---|---|---|
| `cold-midd-personal-10min` | default cold email | 10 min |
| `referral-15min` | someone real offered a referral | 15 min |
| `warm-all-update` | periodic update to people already known | none |
| `cold-all-15min` | retired, rounds 1 and 2 | 15 min |

Read the variant file before writing. Do not paraphrase the reference emails - copy drifts.

**The rule that matters:** the middle of the email carries a **judgment, not a fact**. "You
founded Pinboard" proves a headline was read. "Spending three decades at Goldman and then
pivoting to lead research on the economics of AI infrastructure is strategic and smart" proves
a career was studied. Test every line: *could this be sent to any of the other nine people
today?* If yes, it is not finished.

House rules: **no em dashes**, no availability windows, and never "I came across", "I noticed",
"your remarkable", "I would be honored", "resonates with me".

**Length: 90-95 words.** A band, not a ceiling. Under 90 means detail that proved the research
got cut; over 95 means the read is stacking clauses. Each variant file carries its own budget
table (`elite-brevity-10min` is deliberately ~55). If the read runs past one sentence, it is not
finished.

Full writing rules live in `email_personalization_prompt.md`.

## Email honesty

A guessed `first.last@company.com` is not an address, it is a bounce. Grade it `GUESSED` and
**leave the Email cell blank**. A blank email beside a real LinkedIn URL is worth more, because
LinkedIn still reaches them.

`Email Confidence` is one of `VERIFIED` / `HIGH` / `MEDIUM` / `LOW` / `GUESSED`.

This is not theoretical. An earlier contact list contained pattern-guessed addresses for John
Deere (d. 1886), A. Barton Hepburn (d. 1922), and Willard C. Butcher (d. 2012), at banks that no
longer exist. **Confirm a person is living and currently working before adding them.**

## What is retired

Still present in the repo, no longer used, kept only as reference:

- `email_finder.py`, `insert_generator.py`, `linkedin_scraper.py`, `quick_start.py`,
  `verify_drafts.py` and their tests

**Outlook drafting works, headlessly.** `outlook_drafter.py` drives a headless browser using the
saved profile in `.playwright_session/`, which was re-authenticated 2026-08-13. It creates drafts
and has no send path anywhere in the file.

```bash
./.venv/bin/python outlook_drafter.py --check                    # session still alive?
./.venv/bin/python outlook_drafter.py --create daily/DATE/drafts.json
./.venv/bin/python outlook_drafter.py --delete daily/DATE/drafts.json [--yes]
./.venv/bin/python outlook_drafter.py --login                    # visible re-auth when cookies lapse
```

`--delete` is a dry run without `--yes`, matches subject plus address exactly, and only touches
Drafts. **Delete before recreating, never after**, or a replacement sharing a subject gets taken
too. Full notes in `README.md`, "Deleting drafts".

Cookies last roughly two to three months. When `--check` fails, `--login` opens a window, Max
signs in once, and it is headless again. Drafts are also always written to `daily/YYYY-MM-DD/` as
markdown, so a dead session never costs a morning's research.

The old per-campaign branch workflow is retired; everything now lives on `main`, and new work uses
`Campaign` = `daily-YYYY-MM` there. The old branches were **archived as tags before deletion**, so
their history is permanently recoverable on GitHub (`git checkout archive/<name>` to inspect one):

- `archive/round-1-middlebury-alumni` - round 1 Middlebury alumni cold campaign
- `archive/round-2-middlebury-alumni` - round 2 Middlebury alumni (103-contact list, 10 marked SENT)
- `archive/round-2-tech-entrepreneurs` - round 2 tech-entrepreneur outreach (14 marked SENT)

`round-3-ai-reactivation` and `updates-spring-semester-2026` were fully merged into `main`, so they
were deleted without a tag - their history already lives in `main`.

## Layout

```
.claude/skills/daily-outreach/SKILL.md   the morning routine
README.md                                full description of the system
variants/                                one file per email variant
apps-script/RowMover.gs                  mirrored from the sheet's Apps Script
daily/YYYY-MM-DD/                        each day's drafts and research
backups/                                 sheet snapshots (data only, not formatting)
credentials/                             service account key + .env, both gitignored
```

## Part 2, not built

`PART-2-FOLLOWUPS.md` scopes follow-up emails to people who never replied. Deliberately unbuilt
until real sends exist to learn from. Do not start it without asking Max.

## Cautions

- **Neither secret is in git and there is no other copy.** Losing this disk loses sheet access.
- **Drive API is disabled** on the Cloud project, so the spreadsheet cannot be duplicated
  programmatically. Backups in `backups/` are data only; a formatting-preserving backup needs
  File -> Make a copy by hand.
- **Hunter is a paid Data-platform plan** as of 2026-08-17: 10,000 searches and 11,000
  verifications a year, resetting 2027-08-17. No monthly quota to ration, no per-run cap.
- **`HUNTER_API_KEY` was replaced 2026-08-17.** The previous key was exposed on a since-deleted
  Vercel deployment; confirm at hunter.io that the old one is actually revoked, not just unused.

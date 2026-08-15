# Project_Contact

Max Friedlander's outreach system. Every morning it finds people worth knowing, researches each
one against primary sources, writes a personal email, drafts it in his Middlebury Outlook, and
files the person in a Google Sheet. He reads the drafts and sends the ones he likes.

It runs unattended at **8:04am US Eastern**, and needs no terminal, browser or window open.

---

## The shape of it

```
launchd, 8:04am EST
   │  (laptop asleep? runs the moment it wakes)
   ▼
scheduling/run-daily-outreach.sh          waits for network, loads secrets, disables OMC
   ▼
claude -p  →  .claude/skills/daily-outreach/SKILL.md
   │
   ├── reads BRIEF.md ................... who to find, how many, facts about Max
   ├── dedupes against ~286 people ...... Google Sheet + contacts-log.csv + last 5 daily/ folders
   ├── finds N candidates ............... main session decides who
   ├── dispatches one verifier each ..... subagents, in parallel, per named person
   ├── synthesises ...................... variant, angle, subject, per person
   ├── writes the emails ................ main session, from variants/
   ├── outlook_drafter.py --create ...... headless drafts + a machine-written receipt
   └── writes rows ...................... Google Sheet (top of To Contact) + contacts-log.csv
   ▼
verify_batch.py                           37 automated checks, exits non-zero on any failure
```

## New here? Read in this order

1. **This file**, to the end of "How the emails are written". That is the whole system.
2. **`BRIEF.md`**, which holds who Max is targeting today and the only facts about him that may appear in an
   email. This is the file he edits; everything else follows it.
3. **`variants/cold-midd-personal-10min.md`**, one email template in full, so the writing
   standard is concrete rather than described.
4. **`.claude/skills/daily-outreach/SKILL.md`**, only when you are about to run or change the
   routine. It is long because every rule in it was earned by a run getting something wrong.

**To see whether it is working**, run `verify_batch.py`. To see what it produced, open the newest
folder in `daily/`.

**The one thing to understand before changing anything:** this system is judged by whether Max
sends the emails without editing them. Not by how many people it finds. A batch of three he sends
beats a batch of ten he rewrites.

## Start here

| File | What it is |
|---|---|
| **`BRIEF.md`** | **Max edits this.** Target profile, daily count, his own facts, notes from past runs |
| `.claude/skills/daily-outreach/SKILL.md` | The morning routine |
| `.claude/skills/update-contacts/SKILL.md` | "I sent it", "we spoke", pasted meeting notes |
| `variants/` | The email templates, one file each |
| `CLAUDE.md` | Orientation for a coding agent working in this repo |

---

## The sheet is the database

**Middlebury Connection Tracker**, six tabs, one shared 20-column schema.

```
To Contact → Message Sent → Didn't Connect · Connected → In Touch → Friends
```

**The tab a person is in IS their status.** Column 2, `Status`, mirrors the tab as a coloured
label, and changing that dropdown moves the row. There is no second place to update, so nothing
can fall out of sync.

`apps-script/RowMover.gs` (installed in the sheet as "Sheet Mover") does the moving. **It copies
by column position**, so every tab must keep identical headers in identical order. Run its
`validateHeaders()` after any schema change and `repairStatusLabels()` if a label ever drifts.

New batches are inserted at **row 2**, not appended, so the morning's work is the first thing
visible above 232 rows of older backlog.

### The 20 columns

| # | Column | Filled by |
|---|---|---|
| 1 | Name | research |
| 2 | Status | you, via dropdown. Moves the row |
| 3 | Email | research, or deliberately blank |
| 4 | Email Confidence | `VERIFIED`/`HIGH`/`MEDIUM`/`LOW`/`GUESSED` |
| 5–7 | Company, Role, Industry | research |
| 8 | Phone | you |
| 9 | LinkedIn | research. Required, it is the route when there is no email |
| 10 | Source | the route that found them, free text |
| 11 | Campaign | `daily-YYYY-MM` |
| 12 | Email Variant | which template was used. The only link between a send and its outcome |
| 13 | Personalized Insert | the read, plus the question the email asked |
| 14–15 | Sent Date, Last Contacted | you |
| 16 | Meeting Notes | research writes what they do and why they matter; later, real notes |
| 17 | Ask Them About | you, after talking |
| 18–19 | What They Can Offer Me / I Can Offer Them | you, after talking |
| 20 | Notion Page | you |

Rows with no email grey out automatically, so `To Contact` sorts itself into ready and not-ready.

---

## How the emails are written

Every email belongs to a **variant**. Five are active, and three of them exist to answer one
question each against the control, so a win is attributable.

| id | When | Length |
|---|---|---|
| `cold-midd-personal-10min` | the control, default cold email | 90–95 |
| `elite-decision-10min` | research found a documented hard call | 90–95 |
| `elite-brevity-10min` | firehose inbox, read fits one sentence. Drops the credential | ~55 |
| `elite-builder-10min` | a builder who respects evidence of work | 90–100 |
| `referral-15min` | a real person offered the referral | 90–95 |

**The mechanic they share: the middle of the email is a judgment, not a fact.**

> "You founded Pinboard." (proves a headline was read)
> "Leaving a geology degree to wash kegs at Otter Creek, then betting a whole brewery on one hazy
> beer that bartenders kept saying would never sell, is conviction that took years to look
> correct." (proves a career was studied)

The best reads come from the **shape of a career**, not an achievement in it, which is why the
research demands the full trajectory in order rather than a list of accomplishments.

House rules: no em dashes, no availability windows, no "I came across" / "I noticed" / "your
remarkable" / "I would be honored" / "resonates with me". Every claim about Max comes from
`BRIEF.md` and nowhere else.

**The read must land a judgment, not stop at an observation.** Strip the final clause: if the
sentence still says the same thing, the judgment was never there.

**If a fact about Max was chosen because it overlaps them, make the overlap visible.** The reader
cannot see the research. Let both halves share a word, and never write "just like you" or "we
both".

### The subject line

It names the strongest true thing Max and the recipient share, drawn from the KB.

**Middlebury is fixed** and never varies: every alum gets `Middlebury Sophomore, Hungry to Learn`,
because it works and it is a real credential to them. Two alumni getting the same subject is the
system working.

**Everyone else gets one written from whichever KB fact matched them** - `YC Startup Intern,
Hungry to Learn` for a YC founder, `Cold Called My Way Through College` for a bootstrapper,
`Writing From Buenos Aires, Hungry to Learn` for anyone in Latin America. Five to nine words, and
**never a word claiming equivalence** - no "too", "also", "like you". State the fact and let them
draw the line.

### The conviction angle

The strongest thing in the brief, and the easiest to get wrong. Max turned down money for the
teaching assistant **because he did not have conviction in the idea**, and is still looking for the
one he will. Used as a flex it reads as a boast from someone with nothing at stake; used honestly
it earns a real answer, because every founder remembers when their own conviction arrived.

The question then works from either side: how did you know before the money? Was the conviction
there first, or did refusing create it? Did you still believe it when you sold?

**Never claim conviction he does not have.** The admission is the whole value.

---

## Finding email addresses

In order, cheapest and best first:

1. **Company team page** → `VERIFIED`
2. **Their own site** → `HIGH`
3. **Public commit or paper metadata** → `MEDIUM`, often a filtered alias
4. **`email_prober.py`** → catch-all control, then pattern probing
5. **Hunter email-finder** → last, and capped

### `email_prober.py`

A pattern guess is worthless because you cannot tell a real mailbox from a domain that accepts
everything. Control for that and the same guess becomes evidence.

```bash
./.venv/bin/python email_prober.py --domain calendly.com --first Tope --last Awotona
./.venv/bin/python email_prober.py --domain vercel.com --catchall-only
./.venv/bin/python email_prober.py --domain uala.com.ar --first X --last Y --known real@uala.com.ar
```

It probes a nonsense mailbox first. If the domain accepts it, the tool **refuses to guess** and
tells you to grade `GUESSED` with a blank cell. It uses Hunter's verifier at 0.5 credit rather
than the finder at 1, so it is cheaper as well as better evidence.

### Hunter budget

Free tier is 50 searches and 100 verifications a month. **Capped at 5 searches and 12
verifications per run**, dropping to no Hunter at all below 10 remaining. One run spent 10 and 20
before the cap existed, which would have emptied the month in five days.

**A guessed address is not an address, it is a bounce.** Blank plus a LinkedIn URL is worth more.

---

## Drafting into Outlook

`outlook_drafter.py` drives a headless browser using the saved profile in `.playwright_session/`.
No API keys, just cookies. **There is no send path anywhere in the file, deliberately.**

```bash
./.venv/bin/python outlook_drafter.py --check                     # session still alive?
./.venv/bin/python outlook_drafter.py --create daily/DATE/drafts.json
./.venv/bin/python outlook_drafter.py --login                     # visible window, re-auth
```

Cookies last roughly two to three months. When `--check` fails, `--login` opens a window, you sign
in once, and it is headless again.

**It writes a receipt.** After each draft it records `created: true` or `false` with the actual
error, from inside the loop that did the work. This exists because one run reported "5 of 5 drafts
created" when only 2 existed, and nothing could tell the difference between a run that created
drafts and a run that said it did. The receipt is written by the script, so a run cannot claim
work it did not do.

---

## Verifying a batch

```bash
./.venv/bin/python verify_batch.py                 # today
./.venv/bin/python verify_batch.py --date 2026-08-14
```

37 checks, non-zero exit on any failure. **Every check exists because a real run got it wrong at
least once**, grouped so a failure names the broken subsystem:

- **EMAIL COPY**, word count per variant band, em dashes, banned phrases, stale facts about Max,
  subject distinctness, Middlebury only where evidenced, variant spread
- **ARTIFACTS**, research notes, batch summary, `drafts.json`, real addresses only
- **OUTLOOK**, the drafter's receipt, and that every queued address has an entry
- **SHEET**, schema, duplicates, top-insertion, ten required fields, confidence validity, no
  Email-plus-`GUESSED` contradiction
- **LOCAL LOG**, sheet and CSV agree

---

## Scheduling

```bash
cp scheduling/com.maxfriedlander.daily-outreach.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.maxfriedlander.daily-outreach.plist
launchctl list | grep daily-outreach     # second column is the last exit status
```

`StartCalendarInterval` fires a **missed** job as soon as the machine wakes, so a closed laptop
runs the batch the moment it is opened. That is intended behaviour, not a fallback.

The wrapper sets three things a scheduled job does not inherit: `PATH`, the secrets in
`credentials/.env`, and a raised web-search budget. It also **waits for the network** before
starting, because launchd fires the instant the machine wakes and the first real run failed with
DNS errors before Wi-Fi had reconnected.

`DISABLE_OMC=1` is scoped to this script only. OMC's autopilot detection fires on the wrapper's
prompt and creates a state file every run. Interactive sessions are unaffected.

⚠️ **The clock is on UTC−3, not Eastern.** `Hour` is 9 for 8:04am EDT. **When US daylight saving
ends in November it must change to 10**, or the job fires an hour early.

---

## Secrets

Both live only on this machine and neither is in git.

| File | Holds |
|---|---|
| `credentials/google_sheets_key.json` | service account, edit rights on the sheet |
| `credentials/.env` | `HUNTER_API_KEY` |

Load with `set -a; . ./credentials/.env; set +a`. A scheduled run does **not** source your shell
profile, so never depend on it.

There is no backup. Losing this disk loses sheet access.

---

## Layout

```
BRIEF.md                                  Max edits: who, how many, his facts
.claude/skills/daily-outreach/SKILL.md    the morning routine
.claude/skills/update-contacts/SKILL.md   "I sent it" / "we spoke" / pasted notes
variants/                                 email templates, one per file
email_prober.py                           address finding without guessing
outlook_drafter.py                        headless drafts, no send path, writes receipts
verify_batch.py                           37 checks, grades a run without reading it
apps-script/RowMover.gs                   the sheet's row mover, mirrored from Apps Script
scheduling/                               launchd plist + wrapper + logs
daily/YYYY-MM-DD/                         each day's drafts, research and receipts
contacts-log.csv                          mirror of the sheet, in git
campaigns.xlsx                            frozen archive of the five 2026 campaigns
backups/                                  dated sheet snapshots (data, not formatting)
```

---

## Known limits

**Hunter free tier is 50 searches a month** and 5 people a day needs roughly 150. Most addresses
come from public sources and the prober; Hunter is a supplement.

**No reply tracking.** Nothing detects a bounce or an answer, so `Status` is moved by hand. This
means variant performance depends on you moving people between tabs.

**LinkedIn cannot be fetched.** It serves stripped pages to automated requests, so the URL is
usually all that can be confirmed. It is still the contact route for most people at this altitude.

**Reads at this altitude are hard to reach.** Senior people have staff between them and their
inbox. Deliverability across runs was 1/5, 3/5, 5/5, 5/5 as the address-finding improved.

**`contacts-log.csv` is a mirror, not an append-only history.** It is regenerated from the sheet,
so a row deleted there disappears from the log.

---

## History

Rebuilt on 2026-08-13/14 from a Python pipeline into a skill-driven system. The old
`email_drafter.py` / `insert_generator.py` / `email_finder.py` chain is gone; the five 2026
campaign branches are archived in `campaigns.xlsx`.

The skill was hardened over six unattended runs, each one graded and fixed. Defects found by
running it, not by reading it, included: pointing at a browser extension that does not exist
headless; a length rule contradicting itself between two files; three email variants invisible to
the step that chooses them; Hunter framed as a quota to conserve with no trigger to use it, so it
went unused while four people were shipped unreachable; a run reporting drafts it had not created;
and templates hardcoding a Middlebury opener for people with no connection to the school.

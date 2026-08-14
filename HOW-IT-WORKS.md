# How the outreach system works

Plain description of the whole thing, for reading rather than executing. The executable version
is `.claude/skills/daily-outreach/SKILL.md`.

## The shape of it

Every morning, Claude finds ten people worth knowing, researches each one, writes each a real
email, saves the drafts to this repo, and files the people in the Google Sheet under **To
Contact**. You read the drafts, send the ones you like from Outlook, and move people between
tabs as they respond.

Nothing runs on a pipeline. There is no script to maintain - Claude reads the skill file and
does the work directly, writing whatever code it needs at the time.

## The sheet is the database

**Middlebury Connection Tracker**, six tabs, one shared 20-column schema:

```
To Contact → Message Sent → Didn't Connect · Connected → In Touch → Friends
```

**The tab a person is in *is* their status.** There is no separate status field to keep in sync,
because there is nothing to disagree with. The `Status` column (col 2) mirrors the tab as a
colored label, and changing it moves the row - that is the one control you touch.

An Apps Script (`apps-script/RowMover.gs`, installed as "Sheet Mover") does the moving. It
copies the row to the destination tab, deletes the original, and re-sorts by `Last Contacted`.

**It copies by column position**, so every tab must keep identical headers in identical order.
`validateHeaders()` in the script checks this; run it after any schema change.

### The 20 columns

| # | Column | Filled by |
|---|---|---|
| 1 | Name | research |
| 2 | Status | you, via dropdown - moves the row |
| 3 | Email | research, or left blank |
| 4 | Email Confidence | research - `VERIFIED`/`HIGH`/`MEDIUM`/`LOW`/`GUESSED` |
| 5 | Company | research |
| 6 | Role | research |
| 7 | Industry | research |
| 8 | Phone | you, after talking |
| 9 | LinkedIn | research |
| 10 | Source | research - where the lead came from |
| 11 | Campaign | `daily-YYYY-MM` |
| 12 | Email Variant | which email was sent - the link to `variants/` |
| 13 | Personalized Insert | the read on them |
| 14 | Sent Date | you, when you send |
| 15 | Last Contacted | you |
| 16 | Meeting Notes | you, after talking |
| 17 | Ask Them About | you - the personal thing to raise next time |
| 18 | What They Can Offer Me | you, after the notes |
| 19 | What I Can Offer Them | you, after the notes |
| 20 | Notion Page | you - one page per person |

Rows with no email in column 3 grey out automatically, so `To Contact` sorts itself into "ready
to send" and "still needs an address" without you filtering anything.

## Measuring which emails work

Every email belongs to a **variant**, one file each in `variants/`, and its id goes in column 12.

Because the tab is the outcome, scoring is just counting: of everyone carrying
`cold-midd-personal-10min`, how many sit past `Message Sent`? That is the reply rate.

Two rules keep the numbers honest:

- **A sent variant is frozen.** Editing copy that is already in the wild corrupts the results,
  because the sheet still points at the old id. New copy, new id.
- **Column 12 accumulates.** Re-contacting someone appends
  (`cold-midd-personal-10min; referral-15min`) rather than overwriting, so the first attempt is
  not erased. Credit goes to the last id.

Current variants:

| id | when | ask |
|---|---|---|
| `cold-midd-personal-10min` | default cold email | 10 min |
| `referral-15min` | someone real offered to refer you | 15 min |
| `warm-all-update` | periodic update to people you know | none |
| `cold-all-15min` | retired - rounds 1 and 2 | 15 min |

## What makes the emails work

Both current variants are built from emails you actually wrote. The mechanic they share is that
the middle of the email contains **a judgment, not a fact**.

> "You founded Pinboard." (proves a headline was read)
> "Spending three decades at Goldman and then pivoting to lead research on the economics of AI
> infrastructure is strategic and smart." (proves a career was looked at and a view formed)

The ask is a real question, specific enough that the recipient has an opinion and would enjoy
giving it. The test applied to every line: *could this be sent to any of the other nine people
today?* If yes, it is not finished.

If no honest angle turns up, the person is dropped. Nine researched emails beat ten filler ones.

## Where things live

```
.claude/skills/daily-outreach/SKILL.md   the morning routine, executable
variants/                                one file per email variant
apps-script/RowMover.gs                  the sheet's row mover, mirrored from Apps Script
daily/YYYY-MM-DD/                        each day's drafts and research
backups/                                 sheet snapshots
credentials/google_sheets_key.json       service account, gitignored
.venv/                                   local Python, gitignored
```

## Known limits

**Drafts land in the repo, not Outlook.** The saved Outlook session expired in May 2026 and the
Python drafter is retired, so Claude writes markdown files and you paste them in.

**Both secrets live only on this machine, gitignored.** `credentials/google_sheets_key.json`
(sheet access) and `credentials/.env` (`HUNTER_API_KEY`). Neither is in git, so neither survives
a disk failure and neither is reachable from a cloud runner. Load the env file explicitly with
`set -a; . ./credentials/.env; set +a`; a cron-triggered run does not source your shell profile.

**`HUNTER_API_KEY` still needs rotating.** It was exposed on the deleted project-contact-build
Vercel deploy. The copy here works today but should be replaced at hunter.io.

**Hunter is 50 searches a month.** At ten people a day that is gone in five days, so most
addresses will come from other routes or stay blank.

**One person is still duplicated.** Bryan Goldberg is on both `To Contact` and `Didn't Connect`
- one of those is wrong and only you know which.

**Nothing schedules this yet.** The morning trigger is not set up; the skill runs when invoked.

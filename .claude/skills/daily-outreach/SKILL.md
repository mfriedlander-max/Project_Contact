---
name: daily-outreach
description: Use each morning at 8am EST, or when Max says "run outreach", "find 10 people", "do today's batch", or asks for new people to connect with. Also use when a batch of cold emails needs researching and drafting for Middlebury networking.
---

# Daily Outreach

Ten people a day. Every one researched properly, every email good enough that Max sends it
without editing.

**The output is not ten emails. The output is ten emails Max would be glad he sent.** A batch
that needs rewriting cost him more time than it saved.

## The Iron Rule

**No email without verified research first.**

If you have not confirmed a person is alive, currently in the role you name, and did the thing
you credit them with, you do not write their email. Not a draft, not a placeholder, not "will
verify later."

Violating the letter of this rule is violating the spirit of it.

## Red flags: stop if you catch yourself thinking any of these

- "This angle is probably close enough"
- "I'll verify the details after drafting"
- "Their bio says it, so it's true"
- "I need ten, and this is the tenth"
- "The pattern email format is obvious, so this address will work"
- "This is a well-known person, I already know their background"
- "Two sources said it, that's enough" (were they the same source twice?)

All of these mean: go back and research, or drop the person.

## Rationalizations, and why they are wrong

| Excuse | Reality |
|---|---|
| "Nine feels like failure" | Ten generic emails damage a list you cannot rebuild. Nine researched ones do not. |
| "The guessed email is probably right" | It is probably a bounce, and bounces train spam filters against your domain. Blank is better. |
| "I know who Demis Hassabis is" | You know his Wikipedia summary. That is not an angle, and he can tell. |
| "The company website is current" | Company sites go years without updates. Check LinkedIn and recent news. |
| "Close enough on the title" | Naming the wrong role in line one ends the email there. |
| "I'll note the uncertainty in research.md" | Max reads the draft, not the caveats. Uncertainty belongs in the confidence grade or nowhere. |
| "This person is famous, worth a shot" | Household names do not reply. Aim two to fifteen years ahead of Max. |

## Before starting

Read `variants/cold-midd-personal-10min.md` and `variants/referral-15min.md` in full. Do not
work from memory or paraphrase them; copy drifts every time it is summarised.

## Reaching the sheet

Sheet id is in `outlook_config.json` → `google_sheet_id`. Auth is the service account at
`credentials/google_sheets_key.json` (gitignored, edit rights). Interpreter with `gspread`
installed: `./.venv/bin/python`. Nothing is installed globally.

```python
import json, gspread
from google.oauth2.service_account import Credentials
cfg = json.load(open('outlook_config.json'))
creds = Credentials.from_service_account_file(
    'credentials/google_sheets_key.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets'])
sh = gspread.authorize(creds).open_by_key(cfg['google_sheet_id'])
```

Secrets: `set -a; . ./credentials/.env; set +a`. A cron-triggered run does **not** source the
shell profile, so never depend on it.

## Step 1 - Load who is already known

Read every tab of the sheet and `contacts-log.csv`. Everyone already there is disqualified, on
any tab, regardless of outcome.

Match on **name and on email domain plus surname**. "Mike Seibel" and "Michael Seibel" are one
person, and re-emailing someone who already said no is worse than not emailing at all.

Read the last five folders in `daily/`. Anyone proposed in the past week is not fresh, even if
they never reached the sheet.

## Step 2 - Find candidates

Target profile, in priority order:

1. **Middlebury alumni** in AI, software, finance, or venture. The school tie is the strongest
   opener available and nobody else can use it.
2. **Founders or researchers in AI for education** - adjacent to what Max is building.
3. **People whose path rhymes with Max's** - self-taught builders, humanities-to-code switchers,
   people who started something at 20.
4. **Operators two to fifteen years ahead.** A Series A founder replies. A household name does not.

Hard exclusions:

- **Anyone not verifiably alive and working.** An earlier list contained John Deere (d. 1886),
  A. Barton Hepburn (d. 1922), and Willard C. Butcher (d. 2012), at banks that no longer exist.
- Anyone at a company that no longer exists under that name.
- Anyone already in the sheet, the log, or a recent `daily/` folder.

Find more candidates than you need. Some will fail research, and you want to drop those without
being tempted to keep a weak one to hit ten.

## Step 3 - Research each person properly

This is most of the work. Budget for it.

For each person, gather from **at least two independent sources** (two pages quoting the same
press release is one source):

| Field | Must be |
|---|---|
| Name | as they write it, spelling verified |
| Company | current, confirmed within the last year |
| Role | current title, confirmed within the last year |
| Industry | |
| LinkedIn | real URL, opened and confirmed to be the right person |
| Email | verified, or blank |
| Email Confidence | `VERIFIED` / `HIGH` / `MEDIUM` / `LOW` / `GUESSED` |

Then go deeper, because the email depends on it. Look for:

- how they got where they are, especially anything non-linear
- what they have said recently in talks, interviews, posts, or papers
- what they seem to care about beyond their job title
- anything connecting them to Middlebury, education, or AI
- anything a stranger could not know from their LinkedIn headline

**Email honesty.** A guessed `first.last@company.com` is not an address, it is a bounce. Grade
it `GUESSED` and **leave the Email cell empty**. A blank email next to a verified LinkedIn URL
is more useful, because LinkedIn still reaches them.

Hunter has 50 searches/month on the free tier. Check remaining quota at
`https://api.hunter.io/v2/account?api_key=...` before spending any. At ten people a day it runs
out in five days, so spend it on people who are otherwise unreachable. If the key is missing,
say so; do not fall back to guessing.

## Step 4 - Find the angle

Two things per person:

- **The read** - what they did, plus what Max makes of it. A judgment, not a compliment.
- **The question** - specific, opinionated, and something they would enjoy answering.

The bar, from a real email:

> "Spending three decades at Goldman and then pivoting to lead research on the economics of AI
> infrastructure is strategic and smart."

That works because it describes a real career move and takes a position on it. "You're a
leader in AI" does not.

Apply both tests before writing:

1. **The swap test.** Could this sentence be sent to any of the other nine people today? If
   yes, it is not finished.
2. **The stranger test.** Could someone who read only their LinkedIn headline have written it?
   If yes, it is not finished.

If after genuine effort no honest angle exists, **drop the person and say so in the report.**

## Step 5 - Write the emails

Variant: real referral → `referral-15min`. Everything else → `cold-midd-personal-10min`.

Follow the reference email in the variant file exactly: structure, length, sign-off. Under 120
words. **No em dashes.** No availability windows. Never "I came across", "I noticed", "your
remarkable", "I would be honored", "resonates with me".

Read each finished email once as if you were the recipient. If the honest reaction is "this is
a form letter", it is not done.

## Step 6 - Put the drafts in Outlook

Max reviews and sends from his Middlebury Outlook, so the drafts go there.

Use Claude in Chrome against `https://outlook.office.com/mail/` (Middlebury account). For each
person: new message, fill To / Subject / body, close it so Outlook saves it to Drafts. **Do not
click Send.** Ever. Max sends them himself after reading.

If Outlook is not reachable - not logged in, or the browser is unavailable - **do not stop the
run.** Write the drafts to the repo and say clearly in the report that Outlook was skipped and
why.

Either way, always write the repo copy as the durable record:

```
daily/YYYY-MM-DD/
  01-firstname-lastname.md    to, subject, variant id, body
  batch.md                    all of them, to read in one pass
  research.md                 every claim, with the source behind it
```

`research.md` is not optional. It is how a claim gets checked before it goes to a stranger, and
it is what makes a wrong fact traceable afterwards.

## Step 7 - File them

Append to the **To Contact** tab and to `contacts-log.csv`. Six tabs share one 20-column schema
and the Apps Script row mover copies **by position**, so column order is not negotiable:

```
Name | Status | Email | Email Confidence | Company | Role | Industry | Phone | LinkedIn |
Source | Campaign | Email Variant | Personalized Insert | Sent Date | Last Contacted |
Meeting Notes | Ask Them About | What They Can Offer Me | What I Can Offer Them | Notion Page
```

- **Status** = `To Contact` exactly. The Apps Script reads this column; a wrong value breaks the mover.
- **Campaign** = `daily-YYYY-MM`.
- **Email Variant** = the id used. Never blank; it is the only link between a send and its
  result. On a re-contact, append rather than overwrite.
- **Personalized Insert** = the read from step 4.
- Leave `Sent Date`, `Meeting Notes`, `Ask Them About`, both offer columns, and `Notion Page` empty.

**Check before writing, and refuse the whole batch rather than half-writing it:**

- header row still matches the 20 columns above
- no name already in the sheet or the log, and none twice within the batch
- every `Email Confidence` is one of the five allowed values
- no row has both an Email and `GUESSED`
- every row has an Email Variant

## Step 8 - Report

State plainly:

- who was found, and one line on why each is worth knowing
- which have verified emails, which are LinkedIn-only
- **anyone dropped, and why** - a silent nine reads as a bug, not a judgment call
- whether the Outlook drafts were created or skipped
- Hunter searches used and remaining

## What good looks like

Ten people who are alive, currently in the role you named, not already known, each with a read
that could not be transplanted onto anyone else, and an email address that is either verified or
honestly blank. Drafts sitting in Outlook, ready to read and send.

Nine of those is a good day. Ten generic ones is a bad one.

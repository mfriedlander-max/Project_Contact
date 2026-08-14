---
name: update-contacts
description: Use when Max reports what happened with a contact - sent an email, got a reply, had a call, pasting in Notion meeting notes, someone went quiet, or asks to move people between tabs or correct their details in the Middlebury Connection Tracker.
---

# Update Contacts

Max says what happened in plain language. You work out which rows and columns that touches, in
both the Google Sheet and `contacts-log.csv`, and make the change.

There is no script. Read the sheet, write the sheet.

## The Iron Rule

**Never guess which person is meant.**

"I talked to Sarah" when two Sarahs exist is not a 50/50 guess, it is a question. Writing meeting
notes onto the wrong person corrupts a record Max relies on and he may not notice for months.

If the reference is ambiguous, list the candidates and ask. One question costs seconds.

## Red flags: stop if you catch yourself thinking any of these

- "It's probably the one from this week's batch"
- "Only one is on In Touch, so it must be them"
- "I'll put the notes on both to be safe"
- "The name is close enough"
- "I'll overwrite the old notes, the new ones are better"

## Reaching the sheet

```python
import json, gspread
from google.oauth2.service_account import Credentials
cfg = json.load(open('outlook_config.json'))
creds = Credentials.from_service_account_file(
    'credentials/google_sheets_key.json',
    scopes=['https://www.googleapis.com/auth/spreadsheets'])
sh = gspread.authorize(creds).open_by_key(cfg['google_sheet_id'])
```

Use `./.venv/bin/python`. Nothing is installed globally.

## The schema

Six tabs, one 20-column schema, identical order on every tab:

```
Name | Status | Email | Email Confidence | Company | Role | Industry | Phone | LinkedIn |
Source | Campaign | Email Variant | Personalized Insert | Sent Date | Last Contacted |
Meeting Notes | Ask Them About | What They Can Offer Me | What I Can Offer Them | Notion Page
```

**The tab a person is in is their status.** Column 2 mirrors it.

## Moving someone between tabs

The Apps Script `onEdit` trigger only fires on a human edit in the browser. **An API write to
the Status column does not move anything** - it just makes the label disagree with the tab,
which is exactly the corruption the mover exists to prevent.

So when a move is needed, do it fully yourself:

1. copy the whole 20-column row to the destination tab
2. set its Status to the destination tab name
3. delete the original row
4. verify: the person appears once, and every Status matches its tab

Never write a new Status value and leave the row where it is.

## What Max says, and what it means

| He says | Do |
|---|---|
| "sent the email to X" | `Sent Date` = today, `Last Contacted` = today. Move `To Contact` → `Message Sent`. |
| "X replied" / "we're talking" | Move → `Connected`. `Last Contacted` = today. |
| "had a call with X" | Move → `In Touch` if not already. `Last Contacted` = today. Then meeting notes, below. |
| "X never got back to me" | Move → `Didn't Connect`. |
| "X is a friend now" | Move → `Friends`. |
| "here are my notes on X" (Notion paste) | See below. |
| "X's email is actually ..." | Update `Email`, set `Email Confidence` = `VERIFIED`. |
| "X moved to Y" | Update `Company` and `Role`. Note the old one in `Meeting Notes` if useful. |

Dates are `YYYY-MM-DD`. If he says "yesterday" or "last Tuesday", resolve it and say which date
you used.

## Meeting notes

Max pastes notes from Notion. Do three things with them:

1. **`Meeting Notes`** - the notes themselves. **Append, never overwrite.** Prefix with the date
   and keep the previous entries below. Losing the record of an earlier conversation is not
   recoverable.
2. **`Ask Them About`** - the personal thing to open with next time. Their kid's college
   search, the trip they mentioned, the thing they were stuck on. This is the field that makes
   the next conversation feel like a continuation.
3. **`What They Can Offer Me`** and **`What I Can Offer Them`** - fill these in *from* the notes.
   They are conclusions drawn after talking, not guesses made before.

Read the notes for what was actually said. If nothing personal came up, leave `Ask Them About`
empty rather than inventing something; a fabricated detail is worse than a blank, because Max
will use it out loud.

## Adding someone Max met outside the system

New row on the tab matching reality (usually `Connected` or `In Touch`, not `To Contact`, since
contact already happened). Fill what is known, leave the rest blank. `Source` = how they met.
`Email Variant` stays empty - no variant was used, and putting one there would corrupt the
variant stats.

## Keep the local log in step

Every change to the sheet also goes to `contacts-log.csv`, the repo's own record of who was
contacted and when. It is the copy that survives losing sheet access.

## After every change

Confirm what changed, in one line per person: name, which tab they are now on, which fields were
written. Then verify no duplicates were created and every Status matches its tab.

If something looks wrong afterwards, `backups/` has dated snapshots.

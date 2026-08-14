---
id: warm-all-update
audience: people you have already spoken with (In Touch, Connected, Friends)
subject: "Middlebury Update - Max"
ask: none
status: active
first_used: 2026-05-28
campaigns: [updates-spring-semester-2026]
---

## What this is

The periodic update to warm contacts. Not outreach - it asks for nothing. The entire point is
staying in someone's memory between real conversations, so the only success condition is that
it does not feel like an imposition.

Sent by `send_semester_update.py`, reading the "In Touch" tab.

## Hypothesis

A no-ask update earns more goodwill than a check-in that requests time. It also gives the
recipient a low-cost opening to reply about whichever item they care about, which is a better
lead into a conversation than asking for one.

## Structure

```
Hey {first_name},

Hope you're doing well! Wanted to send another update now that the semester is wrapping up:

{updates - one line each, real HTML <div> blocks}

No need to reply to this, but if anything comes to mind, feel free to respond.

Best,
Max
```

The closing line is doing real work. It removes the obligation, which is what separates this
from a check-in that reads as a request.

## Formatting

Send as HTML with real block elements. The first run used plain-text dashes and Outlook mangled
the spacing into an unreadable block - `send_semester_update.py` was rewritten specifically to
fix this, and its docstring says so.

## Rules

- **Rewrite the update list every send.** It is the content, not a template.
- **Keep an exclusion list.** The script carries `EXCLUDE_NAMES` for people who should not get
  a bulk update. Check it before every send.
- **Do not measure this by tab movement.** A reply is a bonus; nobody moves from `In Touch` to
  `Friends` because of an update email. Scoring it like a cold variant will make a good email
  look like a failure.

---
id: cold-all-15min
audience: everyone (no segmentation)
subject: "College Sophomore - Hungry to Learn"
ask: 15 minutes
status: retired
first_used: 2026-01
superseded_by: [cold-tech-10min, cold-midd-10min]
campaigns: [round-1-middlebury-alumni, round-2-middlebury-alumni, round-2-tech-entrepreneur-contacts]
---

## What this is

The original cold email, sent to everyone regardless of who they were. Lives in
`outlook_config.json` as `template_cold`. Retired, kept here so rounds 1 and 2 stay
attributable.

## Why it was replaced

Three weaknesses the current variants were built to fix:

1. **Leads with credentials, not with them.** Two full sentences about Max before the reader
   sees anything about themselves. The current variants reach `{insert}` a sentence sooner.
2. **"interested in entrepreneurship, ambitious, and curious about the world"** is unfalsifiable
   and describes every cold email ever sent. It occupies the most valuable line in the message.
3. **Asks for 15 minutes** and offers no reason to say yes beyond wanting to learn.

## Body

```
Hello {name},

My name is Max Friedlander, I am 20 years old, and a current Sophomore at Middlebury. I am interested in entrepreneurship, ambitious, and curious about the world. {insert}

If you had 15 minutes to chat, I would love to learn from you. I promise I'll pay it forward.

Best,
Max
```

## Reading its results

Rounds 1 and 2 predate variant tracking, so nothing in the sheet carries this id yet. If you
want it as a baseline, backfill `cold-all-15min` onto rows whose **Campaign** is
`round-1-middlebury-alumni`, `round-2-middlebury-alumni`, or
`round-2-tech-entrepreneur-contacts`. That is 18 of the 84 rows.

Treat the resulting number as rough. Those rounds also differ in who was targeted and how good
the email addresses were, so the copy is not the only thing that changed.

# Part 2: follow-ups

**Not built. This is the scoped design, written while the first system was fresh.**

The first system finds people and writes the first email. This one writes the second, to people
who never replied. It reuses everything already built and adds one skill.

---

## The principle

**A follow-up is a second attempt at a person, not a second copy of an email.**

The failure mode is obvious and everywhere: "just bumping this to the top of your inbox", "wanted
to circle back", "following up on my note below". Those are all the sender's problem restated. They
give the recipient no new reason to reply, and they make the first email retroactively worse by
revealing it was a sequence.

The rule that avoids it: **the follow-up must be able to stand alone as a first email.** If it only
makes sense as a reply to the earlier one, it is not finished.

---

## What triggers it

A person is due a follow-up when **all** of these hold:

| Condition | Why |
|---|---|
| They sit in **`Message Sent`** | the tab is the status. Anyone who replied has already been moved out |
| `Sent Date` is **14 or more days** old | under two weeks is pestering; a busy person may simply not have got to it |
| `Email Variant` contains **fewer than 3 ids** | the column accumulates, so its length is the attempt count |
| The address is not `GUESSED` and not a generic queue | never follow up into a `hello@` or an address that probably bounced |

**Three attempts, then stop.** After the third id in `Email Variant`, they are done. Not moved to
`Didn't Connect`, which is Max's judgment to make, but excluded from future follow-up runs. A
fourth email is not persistence, it is noise, and it costs the relationship the first three were
trying to build.

**People in `Didn't Connect` are never followed up.** That tab means Max decided.

---

## The flow

```
follow-up run (weekly, not daily)
   │
   ├── read Message Sent, filter by the four conditions above
   ├── cap the batch at 3 people. Follow-ups are harder to write than first emails
   │
   ├── for each person, load their EXISTING row in full
   │      Personalized Insert  the read already used, so it is not repeated
   │      Email Variant        which variants are spent
   │      Meeting Notes        who they are
   │      Sent Date            how long ago, which sets the tone
   │
   ├── re-run research from scratch, looking for WHAT IS NEW since Sent Date
   ├── pick an unused variant
   ├── write the second email
   ├── outlook_drafter.py, with a receipt
   └── UPDATE the row in place. Never overwrite, never create a second row
```

Weekly, not daily. Follow-ups are a smaller, harder job and there is no reason to look every
morning.

---

## Finding the second angle

In order of strength. **Take the first one that genuinely exists.**

**1. Something new happened.** By far the best, and the only one that makes the timing self
evidently right. They shipped, raised, sold, moved, published, spoke, hired, or were written
about. Reference it directly, with a question about it, and the follow-up needs no apology for
existing because it is visibly prompted by the news rather than by a calendar.

**2. The same person, a different decision.** The research already surfaced more than one hard
call; the first email used one. Take another. This is why the research file keeps everything it
found rather than only what was used.

**3. The same decision, a different question.** Weaker but legitimate. The first email asked the
counterfactual; this one asks the mechanism, or the cost, or what they would tell someone facing
it now.

**4. Nothing new and nothing left.** **Do not send.** Leave them in `Message Sent`, note it in the
report, and let Max decide. A forced follow-up is worse than no follow-up, because it converts a
silent no into an irritated one.

That last row is the whole design. **Never manufacture a reason.**

---

## Choosing the variant

Never the one already used. The `Email Variant` column says which are spent.

| First email was | Try next | Why |
|---|---|---|
| `cold-midd-personal-10min` | `elite-brevity-10min` | if 90 words did not land, 55 is a different bet, not a louder one |
| `elite-decision-10min` | `elite-builder-10min` | asking about their decision failed, so show him building instead |
| `elite-builder-10min` | `elite-decision-10min` | the reverse |
| `elite-brevity-10min` | `cold-midd-personal-10min` | brevity may have read as thin. Give the read room |

This is also the only way the variant experiment learns anything about **sequence**, as opposed to
which single email works best.

---

## Tone, by how long it has been

| Gap | Tone |
|---|---|
| 14 to 30 days | do not mention the first email at all. Write as though this is the first |
| 30 to 90 days | one short clause of acknowledgement is allowed, at most: `I wrote in March about X` |
| over 90 days | treat as a fresh cold email. They do not remember |

**Never**: "just following up", "bumping this", "circling back", "in case you missed it", "I know
you're busy". All banned, in addition to the existing list.

---

## What it writes to the sheet

**It updates the existing row. It never creates a second row and never overwrites research.**

| Column | Action |
|---|---|
| `Email Variant` | **append**, semicolon separated: `cold-midd-personal-10min; elite-brevity-10min` |
| `Last Contacted` | today |
| `Personalized Insert` | **append** the new read after the old one, so both angles are visible |
| `Meeting Notes` | **append** anything new the research found, dated |
| `Sent Date` | leave alone. It records the first send |
| everything else | untouched |

The accumulating `Email Variant` column is what makes attribution work: the last id is the one that
moved them, and the sequence shows what it took.

---

## What it reuses

Almost everything, which is the point of scoping it this way.

| Reused as is | |
|---|---|
| `variants/` | same five, same rules, same length bands |
| `BRIEF.md` | same KB, same Middlebury rule, same subject rules |
| `outlook_drafter.py` | same headless drafting, same receipts |
| `email_prober.py` | only if the address is stale or was never verified |
| the 20-column schema | unchanged |
| `verify_batch.py` | extended, not replaced |

| New | |
|---|---|
| `.claude/skills/followup-outreach/SKILL.md` | the routine |
| a second launchd job, weekly | separate from the daily one |
| `daily/followups/YYYY-MM-DD/` | drafts, research, receipts |

---

## New verification checks

Added to `verify_batch.py`, in a `FOLLOWUP` group:

- every person was in `Message Sent` for 14+ days
- the variant used is not already in their `Email Variant`
- nobody has more than 3 ids after the run
- `Email Variant` and `Personalized Insert` were appended, not overwritten
- `Sent Date` unchanged
- no banned follow-up phrases: "following up", "bumping", "circling back", "in case you missed"
- **stands alone**: the email does not reference the earlier one when the gap is under 30 days
- no second row created for anyone

---

## Open questions for Max

1. **14 days, or longer?** Two weeks is the convention. At this altitude three or four might read
   better.
2. **Three attempts, or two?** Three is defensible for people who genuinely get hundreds of emails.
   Two is safer for the relationship.
3. **Should a follow-up ever change channel?** If the email address is `MEDIUM` and got no reply,
   the second attempt might be better as a LinkedIn message that Max sends by hand. That would need
   the skill to output a message rather than a draft.
4. **Does a follow-up move them out of `Message Sent`?** Currently no, and the tab keeps meaning
   "sent, no reply". An alternative is a `Followed Up` tab, at the cost of a seventh tab and a
   schema change.

---

## Why this is not built yet

The first system needs to accumulate sends before follow-ups mean anything. Right now nothing has
been sent, so there is nobody to follow up with, and the variant experiment has no data. Building
this now would be writing rules against imagined behaviour instead of observed behaviour, which is
exactly how the first eight defects got into the daily skill.

**Build it when 20 or so emails have gone out and some have gone quiet.** The design above should
survive contact with that, and the parts that do not will be obvious by then.

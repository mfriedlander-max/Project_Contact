---
id: cold-midd-10min
audience: Middlebury alumni
subject: "Middlebury Sophomore, Hungry to Learn"
ask: 10 minutes
status: active
first_used: 2026-03-25
campaigns: [round-3-ai-reactivation]
---

## What this is

Same skeleton as `cold-tech-10min`, but leads with the Middlebury tie because for this audience
the school *is* the reason they'll open it. Alumni answer students from their college.

## Hypothesis

Against `cold-tech-10min`: for alumni, shared-institution beats peer-founder framing. The
school does the work the founder credential does elsewhere.

This is the cleanest comparison in the set: one variable, same body, same ask, same sign-off.
The only difference is the clause after "I'm 20 years old and a".

## Body

```
Hi {first_name},

My name is Max. I'm 20 years old and a sophomore at Middlebury building an AI startup. {insert}

{curiosity_question} If you had 10 minutes to chat, I am hungry to learn. I promise I'll pay it forward!

Best,
Max
```

## Slots

Same as `cold-tech-10min`: `{insert}` and `{curiosity_question}`.

## Note

"sophomore" is hardcoded and goes stale every fall. It was already updated once, in the commit
`feat: update to sophomore`. Bump the id when the year changes (`cold-midd-10min-junior`)
rather than editing this file, or every send before the edit gets misattributed.

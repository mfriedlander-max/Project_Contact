# Email Variants

Each file here is one email variant. The `id` in a file's front matter is what goes in the
**Email Variant** column (col 12) of the Middlebury Connection Tracker.

That column is how a send gets matched back to the copy that produced it. Nothing else links
the sheet to this repo, so the id has to be exact.

## Convention

`id` is lowercase kebab-case, shaped `<temperature>-<audience>-<distinguisher>`:

| Part | Values |
|---|---|
| temperature | `cold` (never spoken) · `warm` (have spoken) |
| audience | `midd` (Middlebury alumni) · `tech` (founders/operators, no Midd tie) · `all` |
| distinguisher | whatever the variant is actually testing: `10min`, `15min`, `brevity` |

Once an id has been sent to anyone, **it is frozen**. Editing the copy of a variant that's
already in the wild silently corrupts your results, because the sheet still points at the old
id. Change the copy, change the id.

## Measuring

The tab a person sits in *is* the result, and the **Status** column (col 2) mirrors it. To score
a variant, count its rows per tab:

- `To Contact`: not emailed yet, so it scores nothing
- `Message Sent`: sent, nothing back yet
- `Didn't Connect`: no reply, or a no
- `Connected` / `In Touch` / `Friends`: it worked

Reply rate for a variant = (rows past `Message Sent`) ÷ (all rows carrying that id).

Because col 12 accumulates (`cold-midd-personal-10min; referral-15min`), credit goes to the
**last** id in the cell, which is the one that moved them.

## Adding a variant

Copy an existing file, change the id, and fill in `hypothesis`, meaning what you're actually testing
versus the variant you're comparing against. A variant without a hypothesis is just a different
email, and you won't learn anything from the result.

## Current variants

| id | audience | ask | status |
|---|---|---|---|
| `cold-midd-personal-10min` | default cold email, 90-95 words | 10 min | active |
| `referral-15min` | a real referral offered | 15 min | active |
| `elite-brevity-10min` | firehose inboxes, ~55 words, drops the credential | 10 min | active |
| `elite-decision-10min` | one documented hard call, asks the counterfactual | 10 min | active |
| `elite-builder-10min` | leads with what Max shipped, 90-100 words | 10 min | active |
| `warm-all-update` | already spoken | none | active |
| `cold-tech-10min` | founders/operators | 10 min | superseded |
| `cold-midd-10min` | Middlebury alumni | 10 min | superseded |
| `cold-all-15min` | anyone | 15 min | retired |

## The three elite variants are a designed experiment

They exist to answer one question each, against `cold-midd-personal-10min` as the control. Each
changes exactly one thing, so a win is attributable:

| Variant | What it removes or adds | What a win would prove |
|---|---|---|
| `elite-brevity-10min` | drops the credential, cuts to ~55 words | brevity reads as respect; the résumé was dead weight |
| `elite-decision-10min` | swaps career summary for one documented decision | a counterfactual beats a summary they already know |
| `elite-builder-10min` | leads with Max's shipped work | evidence of building beats "hungry to learn" |

**Spread them across a batch rather than assigning by mood.** Five people a day means roughly one
per variant plus two controls, and results only mean something once each id has 15-20 sends
behind it. Attribution is the `Email Variant` column, so it is never left blank.

## House rules

- **No em dashes.** Standing rule from `email_personalization_prompt.md`, and it applies to
  these files too, not just the emails.
- **No availability windows.** Do not offer time slots before someone has agreed to talk.
- The middle of the email carries **a judgment, not a fact**. See
  `cold-midd-personal-10min.md`.

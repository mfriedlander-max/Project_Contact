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

## The two ways a read fails

These apply to every variant. Both were found by reading a finished email, not by reasoning about
the rules, which is why the worked example matters more than the statement of them.

### 1. It stops at an observation

A counterintuitive fact about someone is not a read. The read is finished when it says **what Max
makes of it.** The recipient has heard the fact about themselves many times; they have not heard
the view.

**The strip test:** delete the final clause. If the sentence still says the same thing, there was
never a judgment in it.

### 2. The overlap is invisible

When a fact about Max is chosen *because* it rhymes with their history, the email has to show the
rhyme. **The reader cannot see the research.** If the connection lives only in `research.md`, the
opener reads as a non-sequitur.

Make both halves share a word. Never write "just like you", "we both", or "like you, I" - the
shared word does the work silently, and claiming the parallel out loud is worse than not drawing it.

### The worked example

Bill Shufelt, Athletic Brewing. The research established that he built Athletic's first
distribution by **cold-emailing race directors** and sponsoring 70 events in his first summer,
which is why the $30k cold-calling fact was chosen for him.

**Before, and wrong on both counts:**

> I'm Max, 20, a current Midd kid, and I made $30k cold calling small businesses to help pay for
> school. You quit drinking, then built the biggest non-alcoholic beer brand in America by aiming
> it at drinkers instead of at people who quit.

Strip the last clause and it says the same thing, so there is no judgment. And the cold-calling
opener has nothing to attach to: to Bill it reads as "I cold call" then "you quit drinking".

**After:**

> I'm Max, 20, a current Midd kid who made $30k cold calling small businesses to pay for school.
> Building the biggest non-alcoholic beer brand in America **off cold emails** to race directors,
> then aiming it at drinkers rather than people who quit, **is a bet that the bigger market is the
> harder sell.**

Same facts, same length band. `off cold emails` connects the two halves without announcing it, and
the final clause is now a claim he could disagree with.

A third, smaller fix in the same email: the question was "if you had let it stay a sobriety story",
which implies drift. It is now "if you had aimed it at the people who quit", which is the decision
he actually faced. **Counterfactuals should name the choice, not describe passivity.**

## House rules

- **No em dashes.** Standing rule from `email_personalization_prompt.md`, and it applies to
  these files too, not just the emails.
- **No availability windows.** Do not offer time slots before someone has agreed to talk.
- The middle of the email carries **a judgment, not a fact**. See
  `cold-midd-personal-10min.md`.

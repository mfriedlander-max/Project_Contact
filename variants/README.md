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

**Superseded as of 2026-08-16, and the table above is kept as history.** Rule 3 makes the posture
opener (`20, ambitious, hungry to learn about entrepreneurship`) the default for every variant, so
`elite-builder-10min` can no longer test it against `hungry to learn`. That comparison is closed
without a result.

What still varies between the three is worth keeping: brevity, a documented decision, and shipped
work as the lead. **Rewrite all three to sit on top of the posture opener rather than replace it**,
and treat what they change as the thing being tested. Sends made before this date were written to
the old copy, so their counts are not comparable to what comes after.

## Worked examples: how these emails fail

These apply to every variant. Each was found by reading a finished email, not by reasoning about
the rules, which is why the worked example matters more than the statement of them.

**Where a rule here conflicts with a variant file's own copy, the rule wins and the variant gets
rewritten to fit.** The variants are formats being tested; these are how the emails are written.

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

### 3. It leads with the credential instead of the posture

Open by saying what Max is and what he wants: **20, ambitious, hungry to learn about
entrepreneurship.** It costs a clause and tells the reader what kind of email this is before they
have to work it out. Leading with the credential makes them read to the end to find out what is
being asked.

`I'm Max, 20, a sophomore studying applied math` states a fact. `I'm Max, 20, hungry to learn about
entrepreneurship` sets an expectation. Prefer the second. The credential moves down to wherever it
carries the question, or comes out.

**Not a fixed string.** The posture is the point, not the wording. If two emails in a batch open
with the same sentence, both are unfinished.

### 4. It empties the whole inventory of Max facts

**One Max fact per email.** The AI teaching assistant, the $5K pitch win, the turned down money,
the $30k cold calling, applied math, loves selling: these are a menu, and the email picks one.
Reciting them reads as a résumé and crowds out the read, which is the only part that proves the
research happened.

Pick whichever fact the recipient's own history gives them a reason to care about. If two qualify,
choose between them rather than keeping both.

### 5. It fills the band instead of stopping when it is done

90-95 words was written when the failure mode was thin research. The failure mode now is stacking.
**The band is a ceiling, not a target.** If the read lands in 70 words, ship 70 words. Cutting
reaches the ask sooner, and the ask is the point. Never pad back up.

Every edit in the 2026-08-16 batch got shorter and none got longer: 92 to 85, 93 to 75, 92 to 65,
92 to 60.

### 6. It asks about the mechanism instead of the risk

Aim the question at **a moment they took a real risk.** Not at the machinery behind it, and not at
a distinction the email invented for them to introspect on.

`What the nagging felt like, and how you told it apart from mere interest` asks someone to do
philosophy for a stranger. `What led to your decision in 2018 to take a leap` is answerable in one
breath and is the thing they would enjoy answering.

"Leap" is not a magic word, it is just one way to say taking a risk. Phrase it however the specific
decision wants to be phrased. What matters is that the question points at the risk.

### 7. The detail is impressive but irrelevant

**Impressive facts are fine when they are relevant.** Depth of research is not the problem;
showboating it is. A fact earns its place by connecting to the question being asked, not by
demonstrating how hard it was to find.

The test: does this fact make the question make sense? If it is there to prove the research
happened, cut it. Commit dates, a marketing degree at Sundsvall, an internship reapplied for under a
middle name from a second email address: each is verifiable, and each was cut because the recipient
reads it as surveillance rather than interest.

### The examples

Each is a real email that went out or nearly did. **Read them; the rules above are short and the
examples are the part that transfers.**

---

#### Example 1: Bill Shufelt, Athletic Brewing

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

---

**Examples 2 and 3 are Max's own edits to drafts the system produced.** The "before" is what was
drafted, the "after" is what Max rewrote it to. Spelling normalized, nothing else touched.

---

#### Example 2: Bill Shufelt, Athletic Brewing, Max's edit

**This revises Example 1 above.** Same email, same facts, edited by Max after reading it.

> **Before, which is the "after" from Example 1.**
>
> "I'm Max, 20, a current Midd kid who made $30k cold calling small businesses to pay for school.
> Building the biggest non-alcoholic beer brand in America off cold emails to race directors, then
> aiming it at drinkers rather than people who quit, is a bet that the bigger market is the harder
> sell.
>
> I'm building an AI teaching assistant, and would love to know where the category would be if you
> had aimed it at the people who quit."

> **After.**
>
> "I'm Max, 20, a current Midd kid that's hungry to learn and ambitious. Building the biggest
> non-alcoholic beer brand in America off cold emails to race directors, then aiming it at drinkers
> rather than people who quit, is genius.
>
> My dad loves your beer, and if you're open to 10 minutes to chat so I could learn I'd love to
> talk, I promise I'll pay it forward."

92 words to roughly 65. What changed:

- **The opener states the posture instead of the credential.** `hungry to learn and ambitious` tells
  Bill what kind of email this is in the first line. The $30k cold-calling fact comes out.
- **`My dad loves your beer` replaces the researched question.** This is a personal touch Max adds
  himself when he has one. **Do not manufacture these.** A warm line that is actually true is worth
  a lot; an invented one is worth less than nothing, and there is no way to research your way to it.
- `is a bet that the bigger market is the harder sell` becomes `is genius`, which is shorter and
  admiring rather than contestable.

#### Example 3: Arvind Jain, Glean

The research found a real pair: he declined to join Rubrik in 2013 because no problem had nagged at
him, and left Google in 2018 when one had.

> **Before.**
>
> "I'm Max, 20, studying applied math. I built an AI teaching assistant and turned down money for
> it, because I did not have conviction, and I am still looking for the one I will. You said no to
> Rubrik in 2013 because no problem had nagged at you yet, then left in 2018 when one had.
>
> I'd love to know what the nagging felt like the second time, and how you told it apart from mere
> interest."

The question is finely machined, and it asks him to introspect on a distinction the email invented
for him. It is a good question that a stranger has not earned.

> **After.**
>
> "I'm Max, 20, and hungry to learn about entrepreneurship. I built an AI teaching assistant for
> colleges and turned down angel investors as I didn't feel convicted enough. You said no to Rubrik
> in 2013, then left in 2018 when something spoke to you.
>
> I'd love to know what led to your decision in 2018 to take a leap, if you're open to 10 minutes I
> promise I'll pay it forward."

93 words to roughly 75. What changed:

- **The posture leads.** `hungry to learn about entrepreneurship` before any credential.
- **The question aims at the leap, not the mechanism.** `what led to your decision in 2018 to take a
  leap` is answerable in one breath and is the thing he would enjoy answering. The taxonomy of
  nagging versus interest was doing work the recipient did not ask for.
- **The Max fact is compressed to one clause and made concrete.** `turned down angel investors`
  beats `turned down money`, and the trailing `still looking for the one I will` comes out.

One caution for reuse: `something spoke to you` is vaguer than the research supports. Keep the
shape, keep the 2018 specificity from `research.md`.

### Adding an example

**Add one whenever a finished email turns out to have a defect worth naming.** This section is the
memory of what has actually gone wrong, and it is more useful than any amount of rule-writing,
because a rule tells you what to avoid and an example shows you what it looked like when someone
failed to.

The bar, and it is a real bar:

| Add it if | Do not add it if |
|---|---|
| The email was actually written, and the defect was found by reading it | It is a hypothetical failure nobody has made |
| The fix is demonstrable as a before-and-after on the same facts | The "fix" is just a different email |
| The failure could plausibly recur | It was a one-off typo or a wrong fact |
| Naming it changes what a future writer does | It is a matter of taste |

The format, kept identical so they are scannable:

```markdown
#### Example N: {Person}, {Company}

{One or two lines of context: what the research found, and why the choice made sense at the time.
An example is only instructive if the mistake was reasonable.}

> **Before, and what is wrong with it.**
>
> "{the actual text}"

{Why it fails, in the reader's terms rather than the rules'. What does the recipient see?}

> **After.**
>
> "{the actual text, same facts, same length band}"

{What changed, one bolded fix per paragraph. Name the general rule it produced, if it produced one.}
```

Two things that keep this section honest:

- **Use the real text, not a cleaned-up version.** The point is what actually got written.
- **Keep the fix in the same length band and on the same facts.** If the "after" gets to be longer
  or use different research, it proves nothing.

When an example produces a rule general enough to apply every time, add the rule to the numbered
list at the top of this section and leave the example below it as the evidence.

## House rules

- **No em dashes.** Standing rule from `email_personalization_prompt.md`, and it applies to
  these files too, not just the emails.
- **No availability windows.** Do not offer time slots before someone has agreed to talk.
- The middle of the email carries **a judgment, not a fact**. See
  `cold-midd-personal-10min.md`.

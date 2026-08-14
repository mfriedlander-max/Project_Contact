---
name: daily-outreach
description: Use each morning at 8am EST, or when Max says "run outreach", "find 10 people", "do today's batch", or asks for new people to connect with. Also use when a batch of cold emails needs researching and drafting for Middlebury networking.
---

# Daily Outreach

A small batch every morning, the size set by `BRIEF.md`. Every person researched properly, every
email good enough that Max sends it without editing.

**The output is not N emails. It is N emails Max would be glad he sent.** A batch that needs
rewriting cost him more time than it saved.

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
- "I need one more to hit the number, and this is it"
- "The pattern email format is obvious, so this address will work"
- "This is a well-known person, I already know their background"
- "Two sources said it, that's enough" (were they the same source twice?)

All of these mean: go back and research, or drop the person.

## Rationalizations, and why they are wrong

| Excuse | Reality |
|---|---|
| "One short of the number feels like failure" | Generic emails damage a list you cannot rebuild. A short batch does not. |
| "The guessed email is probably right" | It is probably a bounce, and bounces train spam filters against your domain. Blank is better. |
| "I know who Demis Hassabis is" | You know his Wikipedia summary. That is not an angle, and he can tell. |
| "The company website is current" | Company sites go years without updates. Check LinkedIn and recent news. |
| "Close enough on the title" | Naming the wrong role in line one ends the email there. |
| "I'll note the uncertainty in research.md" | Max reads the draft, not the caveats. Uncertainty belongs in the confidence grade or nowhere. |
| "They're too senior to bother" | Not your call. `BRIEF.md` sets the altitude, and it currently aims high on purpose. |

## Step 0 - Read the brief. Max decides who and how many, not you.

**`BRIEF.md` is the first thing you read.** It holds the target profile, the daily count, notes
from previous runs, and current context about what Max is building. He edits it; you follow it.

- **Running interactively** (Max is here): ask whether the brief is still current, and what he
  wants today. If he names a different profile or count, follow that and offer to update
  `BRIEF.md` so tomorrow's unattended run inherits it.
- **Running unattended** (the morning trigger): `BRIEF.md` is the whole instruction. There is
  nobody to ask.

Never substitute your own idea of who is worth contacting. If the brief is unclear and nobody is
there to ask, do the smallest defensible thing and say in the report that the brief needs work.

## Then read the rules, in full

- `variants/cold-midd-personal-10min.md` and `variants/referral-15min.md` - the reference emails,
  the structure, the length budget.
- `email_personalization_prompt.md` - the full banned-AI-phrase list and writing rules.

Do not work from memory or paraphrase these. Copy drifts every time it is summarised, and the
banned-phrase list is the thing that keeps these emails from reading like everyone else's.

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

Read every tab of the sheet and `contacts-log.csv`. **This is a dedupe check and nothing else.**
Everyone already there is disqualified, on any tab, regardless of outcome.

Match on **name and on email domain plus surname**. "Mike Seibel" and "Michael Seibel" are one
person, and re-emailing someone who already said no is worse than not emailing at all.

Read the last five folders in `daily/`. Anyone proposed in the past week is not fresh, even if
they never reached the sheet.

## Step 2 - Find candidates

**The target profile and the count both come from `BRIEF.md`.** Do not invent your own and do
not fall back to a remembered profile; the brief is the only authority on who Max wants today.

What follows is how to execute against whatever the brief says.

Hard exclusions, which apply regardless of what the brief asks for:

- **Anyone not verifiably alive and working.** An earlier list contained John Deere (d. 1886),
  A. Barton Hepburn (d. 1922), and Willard C. Butcher (d. 2012), at banks that no longer exist.
- Anyone at a company that no longer exists under that name.
- Anyone already in the sheet, the log, or a recent `daily/` folder.

Find more candidates than you need. Some will fail research, and you want to drop those without
being tempted to keep a weak one to hit the number.

### Use web search only

**Do not use Firecrawl.** Max's instruction, and it is out of credits anyway. Research runs on
web search plus direct page fetches, and on cheap structured endpoints where they exist: the
GitHub API, arXiv, Maven Central, Google Scholar, company team pages, `middlebury.edu`.

### Search budget is finite, and it binds

On the first live run one researcher **exhausted its 200-call web search budget** mid-task. It
still delivered, but it could not run the broader sweep it wanted to.

A full batch at that depth will hit limits. Manage it:

- Do not give one agent an open-ended "find someone" brief when a narrower one will do. Naming a
  domain and a seniority band cuts the search space hard.
- If an agent reports budget exhaustion, treat its result as **provisional**, not wrong, and note
  in the report which checks it could not run.
- Prefer primary sources that are cheap to fetch: `middlebury.edu` pages, company team pages,
  arXiv PDFs, the GitHub API. LinkedIn and Facebook block automated fetch and burn calls for
  nothing.

### Running researchers in parallel

Dispatch one research subagent per person. They are isolated by design, which is what stops one
agent quietly inheriting another's assumptions, but it also means **they cannot see each other's
findings and will converge on the same obvious person.**

This is not hypothetical. On the first live run, the "AI founder" and "software founder" agents
independently returned Andy Rossmeissl, because he is the strongest match for both.

Prevent it:

- Give each agent a **distinct domain** (AI, edtech, venture, software, quant) *and* an explicit
  list of names already claimed this run.
- Assign domains that do not overlap. "AI founder" and "software founder" overlap heavily; "AI
  research" and "developer tooling" do not.
- When a collision happens anyway, **keep the better-researched result and re-dispatch for the
  empty slot** with the taken name added to the exclusions. Do not paper over it by shipping nine.

A collision is not wasted work. The second pass on Andy Rossmeissl found a better email
(`andy@continuousartifact.com`, published on his own site, versus a GitHub alias he likely
filters) and a stronger angle (self-taught, no CS degree). **When two agents return the same
person, merge their findings and take the strongest of each field** rather than discarding one.

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

Where a real address turns up, record *how it was published*, because that determines whether it
will actually be read:

| Kind | Grade | Note |
|---|---|---|
| Listed on the company's own team page | `VERIFIED` | best case, a real monitored mailbox |
| Published on their personal site | `HIGH` | usually read, but may be a side-project inbox |
| Author address on public commits | `MEDIUM` | often a tagged alias they filter |
| Generic `hello@` / `info@` | `LOW` | reaches a queue, not the person |
| Anything you constructed | `GUESSED` | leave the Email cell empty |

An address being published is not the same as it being monitored. Say which one you have.

**Primary sources only for load-bearing claims.** Middlebury affiliation, current role, and
anything that goes into the email must come from a page actually read, not a search-result
snippet. Aggregators such as RocketReach and ZoomInfo are not sources. On the first live run one
of them asserted a Middlebury "Architecture and Mathematics" degree that would have rhymed
perfectly with Max's applied math, and no primary source confirmed it. That claim stayed out of
the email. **A perfect-sounding fact you cannot trace is the most dangerous kind.**

**A page being institutional does not make it current.** Middlebury's own ELC video pages all
carry an identical `article:published_time` of 2026-06-18, which is a site-migration artifact
rather than a publication date. The companion page for one alum still lists her at a company she
left in May 2025. So a `middlebury.edu` page is excellent proof of *class year and affiliation*
and weak proof of *where someone works today*.

Split the two apart when verifying:

- **Class year, degree, past affiliation** - an institutional page is the best source available.
- **Current employer and title** - needs something the person controls and updates: a live
  LinkedIn page title, a GitHub profile with recent activity, a dated post they authored, a
  company team page that lists them today.

When the two disagree, the self-maintained source wins for currency and the institutional one
wins for history. Say which you relied on.

### Look for a published address first, always

**Order matters. Search for a real published address before touching Hunter.** A published
address is better evidence and costs no quota. In order:

1. **The company's own site** - team page, about page, contact page. Best case: a real monitored
   mailbox, graded `VERIFIED`.
2. **Their personal site or blog.** Often an About or Contact section. Graded `HIGH`. The first
   run found `simon@sirupsen.com` this way.
3. **Public artifacts they authored** - git commit metadata, arXiv PDFs, conference papers,
   published slides. Graded `MEDIUM`, since these are often tagged aliases they filter.
4. **Only then, Hunter.** See below.

Tell the research agents this ordering explicitly in their brief. An agent that jumps to Hunter
first burns quota on someone whose address was on their own homepage.

### Hunter is mandatory when no address is published

**If you cannot find a published address, you MUST run a Hunter search before recording "no
email". Not optional. Not "if it seems worth it".**

This is the single most valuable thing Hunter does, and the first live run got it exactly
backwards: four of five people had no published address, and it used **zero** searches because
the guidance here read as "conserve this". Two of those four were then found on the first try,
both verified valid:

```
Immad Akhund   / mercury.com      -> immad@mercury.com            score 84, valid
Patrick Dorton / rational360.com  -> patrickdorton@rational360.com score 98, valid
```

Conserving the quota to zero while shipping unreachable contacts is the worst possible outcome.
An unused search at month end is worth nothing; a found address is worth the entire batch.

**The procedure:**

```bash
set -a; . ./credentials/.env; set +a
curl -s "https://api.hunter.io/v2/email-finder?domain=COMPANY.com&first_name=FIRST&last_name=LAST&api_key=$HUNTER_API_KEY"
```

Then grade by what Hunter returns, not by hope:

| Hunter says | Record |
|---|---|
| `verification.status: valid`, score 80+ | `VERIFIED`, use the address |
| `verification.status: valid`, score 50-79 | `HIGH`, use the address |
| returns an address, not verified | `MEDIUM`, use it and say it is unverified |
| returns nothing | genuinely no email. `GUESSED`, leave the cell empty |

**Get the domain right first.** Hunter keys off the company domain, so a wrong domain returns
nothing and wastes a search. Confirm it from the company's own site before searching.

**Budget.** 50 searches a month, 100 verifications. At five people a day, expect to need three or
four searches per batch, which is roughly 100/month, so it will run out. Spend them on people
with no published address, never on someone whose address you already have. Report usage at the
end. If the key is missing, say so plainly and never fall back to guessing a pattern.

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

### Pick the variant, and spread them across the batch

`variants/` holds five active variants. **Do not send the whole batch on one id.** Three of them
exist to answer a specific question, and they only answer it once each has 15-20 sends behind it.

| Variant | Use when | Length |
|---|---|---|
| `referral-15min` | a real person offered the referral | 90-95 |
| `elite-decision-10min` | research documented a hard call they made | 90-95 |
| `elite-brevity-10min` | a firehose inbox, and the read fits in one short sentence | **~55** |
| `elite-builder-10min` | a builder who respects evidence of work over stated interest | 90-100 |
| `cold-midd-personal-10min` | the control. Everything else | 90-95 |

On a five-person batch, aim for roughly **two controls and three different experiments.** Assign
by fit first: a documented hard decision makes `elite-decision-10min` the obvious pick, an
institutional figure rules out `elite-builder-10min`. Where two fit equally, choose the one with
fewer sends so far.

**Record the id in the sheet's `Email Variant` column.** It is the only link between a send and
its outcome. A batch that is all one id teaches nothing.

### Length: 90-95 words

**That is the band. Not a cap, a band.** Count the body words and land inside it.

**Counting is a gate, not a note.** Count, and if the number is outside 90-95, revise and count
again *before* writing the file. Run 2 wrote emails at 88 and 97 and recorded the count next to
them, which means it measured and shipped anyway. Recording a violation is not the same as fixing
one.

Body words means `Hi {name},` through `Max` inclusive.

- Under 90 means something was cut that should not have been. Usually the read has lost the
  detail that proved the research.
- Over 95 means the read is carrying stacked clauses. Split it or cut it.

The one exception is `elite-brevity-10min`, which is deliberately ~55 words and tests whether
brevity beats the band. Its own file governs.

If the read runs past one sentence, it is not finished being edited.

### Everything else

Follow the reference email in the variant file exactly: structure, sign-off, ordering. **No em
dashes.** No availability windows. Never "I came across", "I noticed", "your remarkable", "I
would be honored", "resonates with me". The full banned list is in
`email_personalization_prompt.md`.

Read each finished email once as if you were the recipient. If the honest reaction is "this is a
form letter", it is not done.

## Step 6 - Put the drafts in Outlook

Max reviews and sends from his Middlebury Outlook, so the drafts go there.

**Use `outlook_drafter.py`. It is the only method that works unattended.** It drives a headless
browser using the saved profile in `.playwright_session/`, so it needs no Chrome, no extension and
nobody at the keyboard. There is no send path anywhere in that file, by design.

```bash
./.venv/bin/python outlook_drafter.py --check          # is the session still alive?
./.venv/bin/python outlook_drafter.py --create daily/YYYY-MM-DD/drafts.json
```

Write `drafts.json` alongside the markdown as a list of `{"to", "subject", "body"}` objects, and
include only people who have a real address.

If `--check` reports the session is dead, cookies have expired. **Do not try to work around it and
do not stop the run.** Write the drafts to the repo, and say in the report that Outlook was
skipped and that Max needs to run:

```bash
./.venv/bin/python outlook_drafter.py --login
```

**Claude in Chrome is the interactive fallback only.** If Max is present and the extension is
connected, driving `https://outlook.office.com/mail/` by hand also works. It is unavailable in a
scheduled run, so never depend on it. **Do not click Send.** Ever, by either route.

**People with no email cannot be drafted.** An Outlook draft needs a recipient. When research
finds no real address, write the draft to the repo only, put the LinkedIn URL at the top as the
route, and say so in the report. Do not invent an address to make the draft creatable. Expect this on a large share of any
batch aimed at this altitude, and only after Hunter has been tried.

**People with an unconfirmed employer cannot be sent.** If research cannot confirm where someone
currently works, write the draft but mark it clearly as needing confirmation, and keep the
employer's name out of the copy. Opening with the wrong company ends the email at line one. Lean
on published work instead, which stays true regardless of where they sit today.

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
- **Meeting Notes** = a short, concrete line on **what they do and why they are worth Max's
  time.** One or two sentences. This is required on every new row, not optional. Before a meeting
  happens it is the "who is this and why do I care" line Max reads when scanning the tab; after a
  meeting the `update-contacts` skill appends the real notes below it. The first live run left
  this blank on all five rows because this step used to say to leave it empty.
- Leave `Sent Date`, `Ask Them About`, both offer columns, and `Notion Page` empty. Those are
  filled after an actual conversation.

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

A full batch of people who are alive, currently in the role you named, not already known, each
with a read that could not be transplanted onto anyone else, and an email that is either real or
honestly blank. Drafts sitting in Outlook, ready to read and send.

One short of the number, all researched, is a good day. A full batch of generic ones is a bad one.

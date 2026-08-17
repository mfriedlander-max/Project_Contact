---
name: daily-outreach
description: Use each morning at 8am EST, or when Max says "run outreach", "do today's batch", "find people", or asks for new people to connect with. Also use when a batch of cold emails needs researching and drafting for Middlebury networking.
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

- `variants/README.md` - **the worked examples of how these emails fail.** Read this every run.
  The rules are short; the examples are the part that transfers. It grows: whenever a finished
  email turns out to have a defect worth naming, the before-and-after is added there, so it is the
  memory of what has actually gone wrong rather than a list of hypotheticals.
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

### The main session picks the people. Subagents verify them.

**Split the work this way, and only this way:**

| Who | Does |
|---|---|
| **This session** | decides *who* the batch is, assigns variants and which of Max's facts each person gets, writes every email |
| **Subagents** | verify one *named* person each, in parallel, and report facts with sources |

Never ask a subagent "find someone who fits the brief". Ask it "verify this person".

**Why the split falls here.** On run 1 two agents were each told to find the strongest match in
overlapping domains and both returned Andy Rossmeissl. That is not a defect in isolation, it is
what isolation does: same brief, same evidence, same answer. Naming the person first makes a
collision structurally impossible.

The decisions that must stay in one place are the ones made *across* the batch. Which variant each
person gets, which of Max's facts fits whom, whether the Middlebury wedge applies. An isolated
agent cannot know that four other people already took the school angle, or that the batch is about
to go out on one variant.

**What isolation is genuinely worth.** A verifier that only knows one person cannot let a fact
about someone else leak into its findings, and it cannot quietly inherit another agent's
assumption. That is worth keeping, and it is why verification is still farmed out.

**Hard cap: one verifier per person in the batch, and no more. Ever.**

A batch of one person gets one verifier. A batch of five gets five. Never dispatch a second agent
for the same person, never dispatch a spare to "check the checker", and never let a verifier spawn
agents of its own. If a report comes back thin, read it and decide yourself rather than spending
another agent on it.

Every agent burns its own web-search quota and its own tokens, and the parallel work that actually
matters is one-per-person. More than that is cost without information.

**Dispatching verifiers.** One per person, all in a single message so they run in parallel. Use
this prompt. It is not a summary to paraphrase; the detail is what makes the results usable.

```
Verify {NAME}, {ROLE} at {COMPANY}, for a cold email from Max, a 20-year-old Middlebury
sophomore studying applied math who is building an AI teaching assistant.

You are NOT choosing who to contact. This person is already chosen. Your job is to find out
whether the facts hold up and to surface the one thing worth writing about.

DO NOT SPAWN SUB-AGENTS. Do this research yourself. On 2026-08-15 a verifier spawned one anyway,
which made the batch cost six agents instead of five. Its findings were useful, which is exactly
why the rule needs stating here: the temptation is real and the cost is invisible from inside.

DO NOT CALL HUNTER. The main session owns that budget and spends it with the prober. Report the
addresses you find in public sources and grade them; the main session handles anything unreachable.

ACCURACY CONTRACT, absolute:
- Every factual claim must trace to a URL you actually fetched and read. Not a search snippet,
  not a summary, not an aggregator.
- RocketReach, ZoomInfo, getprog, theorg and Crunchbase summaries are NOT sources. If only an
  aggregator asserts something, exclude it and say so.
- Institutional pages (a university, a conference) prove history and class year but NOT current
  employment. For current role use something the person or company controls: a live company team
  page, a dated post they authored, an SEC filing, a GitHub profile with recent activity.
- If two sources disagree, say which you believe and why. Do not silently pick one.
- Never construct an email address. first@company.com is forbidden.
- A fact that would be perfect for the email and cannot be traced is the most dangerous kind.
  Leave it out and flag it explicitly.

FIND:
1. Current role and company, confirmed within the last 12 months, with a dated source.
2. Proof they are alive and active: something dated in the last year.
3. Any connection to Middlebury College, and say plainly if there is none. This decides whether
   the school can be used as the opener, so a wrong answer here ruins the email.
4. Email address, in this order of preference, and grade it:
   company team page (VERIFIED) > their own site (HIGH) > public commit or paper metadata
   (MEDIUM) > generic hello@ (LOW) > nothing found (GUESSED, and leave it blank).
   Do not run Hunter; the main session handles that with the prober.
5. LinkedIn URL. Note that LinkedIn blocks fetching, so the URL may be all you can confirm.
6. THE FULL CAREER TRAJECTORY, in order, with dates where you can get them. Not a list of
   achievements, the actual sequence: what they studied, what they did first, every move since,
   and what they do now. Include the unglamorous and early jobs, which are usually the most
   revealing part.
   This matters more than any single accomplishment. The strongest emails written from this
   research were built on the SHAPE of a career, not a fact from it: "brewing beer before law
   school, then leaving law for consulting and consulting for investing" and "no CS degree,
   taught himself to ship, then twenty-one years on one unglamorous bet without leaving
   Vermont." Neither is an achievement. Both are arcs, and an arc is what you can form a
   judgment about.
   Flag any move that looks like a step sideways or backwards. Those are the interesting ones.
7. Two to four specific, verifiable things they built, shipped, ran or decided, each with its
   source. Numbers and dates, not adjectives.
8. A DOCUMENTED HARD DECISION if one exists: a moment where the obvious choice and the taken
   choice diverged. Turning down money or an acquisition, leaving somewhere successful early,
   building the thing that undercut their own business, staying somewhere unfashionable,
   publishing something inconvenient for their own position. This is the single most valuable
   thing you can find. Say "none documented" rather than inferring one.
9. Anything genuinely shared with Max: a sport, a city (he lives in Buenos Aires and lived in
   Barcelona), a non-linear path, having started something young, selling before building.
10. What they have already been asked publicly. A question they have answered in three podcasts
   is the wrong question.

RETURN:
NAME / COMPANY / ROLE / INDUSTRY / LINKEDIN / EMAIL / EMAIL_CONFIDENCE
MIDDLEBURY: the connection with its source, or "none found"
CURRENT_ROLE_PROOF: dated source URL
CAREER_TRAJECTORY: the sequence in order, with dates and sources. Mark sideways or
  backwards moves.
WHAT_THEY_DID: each concrete fact with its URL
HARD_DECISION: with source, or "none documented"
SHARED_WITH_MAX: or "none"
ALREADY_ASKED_PUBLICLY: questions to avoid
SOURCES: every URL you actually read
COULD_NOT_VERIFY: everything you tried and failed to confirm. Be specific. A verifier that
reports no gaps has not looked hard enough.
```

Do not ask a verifier to write the email or pick the variant. Those are decisions across the
batch and belong to this session.

### When the verifiers come back

All five reports land before anything is written. Then, in this order:

**1. Triage each report before trusting any of it.**

Read `COULD_NOT_VERIFY` first, not last. It is the most informative section, and a report
claiming no gaps has usually not looked hard enough.

| Report says | Do |
|---|---|
| Current role unconfirmed, or sources disagree | **Drop the person.** An email that names the wrong employer ends at line one. Replace them or ship a shorter batch. |
| Not provably alive or active in the last year | **Drop.** No exceptions. |
| Middlebury connection "none found" | Fine. It just means the school cannot be used. Not a reason to drop. |
| No email found | Fine. Run the prober, then Hunter. If still nothing, repo-only with LinkedIn as the route. |
| A perfect-sounding fact with no traceable source | **Cut the fact, keep the person.** This is the most common failure and the most dangerous. |
| Budget exhausted mid-task | Treat as provisional. Either re-dispatch for the missing checks or say in the report which did not run. |

**2. Assign variants across the batch, not one at a time.**

Lay the five side by side and allocate roughly two controls and three experiments:

- A documented hard decision → `elite-decision-10min`. This is the strongest signal, so let it win.
- A builder who respects evidence of work → `elite-builder-10min`.
- A firehose inbox where the read compresses to one short sentence → `elite-brevity-10min`.
- A real referral → `referral-15min`.
- Everything else → `cold-midd-personal-10min`.

Where two fit equally, pick the id with fewer sends behind it. The experiment only pays off if
each variant accumulates volume.

**3. Cross-reference their history against Max's KB and find the real overlap.**

This is the step that makes an email land, and it is a matching problem, not an allocation one.
Put the verifier's `CAREER_TRAJECTORY` and `SHARED_WITH_MAX` next to the `About Max` table in
`BRIEF.md` and look for where the two genuinely touch.

| What the verifier found | What of Max's it resonates with |
|---|---|
| Sold before they built. Started in sales, carried a bag, cold called | **$30k cold-calling SMBs.** He has done the unglamorous version of their origin |
| Turned down money, refused an acquisition, stayed independent | **Turned down money for the teaching assistant.** The same decision at a hundredth the scale |
| Took the money, sold, or raised big | Same fact, opposite side. He made the other call and wants to understand theirs |
| Technical founder who had to learn to sell, or a seller who learned to build | **Loves math and technical work and loves sales.** The combination is rarer than either half |
| Built something in or for education | **AI teaching assistant, $5K, piloting in a school this fall** |
| Argentina, Spain, or Latin America | **Living in Buenos Aires now**, lived in Barcelona. Present tense, not a plan |
| Started something while still a student, or very young | He is 20 and mid-build. A real peer signal, not aspiration |
| Non-linear path, career switch, no formal credential | Applied math undergrad building software and selling it |
| Genuine tennis connection | Played a lot of tennis. Only with a real, sourced connection |
| An early unglamorous job in the trajectory | Whichever of the above rhymes with it |

**When nothing overlaps, do not fall back to generic. Fall back to interesting.**

A KB fact does not have to mirror their history to earn its place. It only has to be worth
reading. The opener's job is to make Max someone worth answering in the next four seconds, and a
concrete, specific, slightly unexpected fact does that on its own.

Compare, for the same person:

> **generic:** "I'm Max, 20, a sophomore studying applied math."
> **hook:** "I'm Max, 20, a sophomore studying applied math, and I made $30k cold calling small
> businesses to help pay for school."

Same person, same paragraph, no thematic connection to the recipient required. The second is
simply more interesting, and it costs eleven words.

So the order of preference is:

1. **A real overlap**, where their history and Max's genuinely touch. Strongest, use it whenever
   it exists.
2. **The most interesting KB fact that fits the audience**, used as a hook with no claimed
   connection. Perfectly good, and this is the normal case.
3. **Plain identity only**, if every fact would be jarring for this reader. Rare. An institutional
   figure like a museum director or bank chairman may be one.

**Never** write an opener that is only "I'm Max, 20, a sophomore" when a hook was available. That
is the actual failure, not the absence of a parallel.

What you are avoiding is five emails opening with the same sentence about Max. Two people can
share a fact when it is genuinely the best for both, but five identical openers means no choice
was made.

**4. Middlebury, per person.** Connection confirmed by the verifier means it leads the subject
line and the opener. `none found` means it appears in neither. This is a per-person decision, so
a batch can and should be mixed.

**5a and 5b. The two ways a read fails.**

A read that stops at an observation, and an overlap the reader cannot see. **Both are defined with
a worked before-and-after in `variants/README.md`, which is required reading for this step.**

The short form, for checking your own work:

- **Strip test.** Delete the final clause of the read. If the sentence still says the same thing,
  there was never a judgment in it.
- **Visible overlap.** If a fact about Max was chosen because it rhymes with their history, both
  halves must share a word. Never "just like you" or "we both".

**5c. Write the read from the trajectory, not from the achievements.**

The `CAREER_TRAJECTORY` section is where the read comes from. Look for the shape: the sideways
move, the early unglamorous job, the thing they left before they had to, the bet they kept making.
Then state it in one sentence with a judgment attached.

Achievements produce "you founded X and it grew to Y", which is a fact they already know about
themselves. Arcs produce "leaving law for consulting and consulting for investing is a career of
trading earned credentials away on purpose", which is a view they have not heard.

**6. Write the question from `ALREADY_ASKED_PUBLICLY`.**

That section exists to be subtracted. Whatever they have answered in interviews is off the table,
and what remains is usually the good question.

**7. Then write the emails.** Length band per variant, count before writing the file, and run
`verify_batch.py` when the batch is complete.

**Budget.** Each agent burns its own web-search quota, so `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION`
is raised to 600 in the wrapper. If a verifier reports exhaustion, treat its result as provisional
and say which checks did not run.

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

### SEC EDGAR is the strongest free source for anyone at a public company or a fund

Full-text search at `https://efts.sec.gov/LATEST/search-index?q=...` and filings under
`https://www.sec.gov/cgi-bin/browse-edgar`. Free, structured, no rate wall, and legally filed,
which makes it better evidence than anything a data vendor sells.

It produced the single strongest verification in this project. For Alex Finkelstein, a Flywire
DEF 14A stated his Middlebury degree **verbatim**, and his personally-filed Form 4 from nine days
earlier proved he was alive and in role. No aggregator comes close to that.

What to look for:

| Filing | Gives you |
|---|---|
| **DEF 14A** (proxy) | director and officer biographies, education, career history, board seats |
| **Form 4** | a filing the person is personally liable for. Excellent proof of life and current role |
| **8-K** | board elections, appointments, departures, with dates |
| **Form D** | fund closes and the executive officers named on them |

Use it for public-company executives, board members, and anyone at a fund that files. It does not
help for private startups, where the company's own site and public commits are better.

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

### Resolve the email with email_resolver.py

**First write `candidates.json`** into the day's `daily/YYYY-MM-DD/` folder from the verifier
reports: one object per person the batch keeps, `{name, first, last, domain, known, known_grade}`
(`known` is the published address research found, or `null`; `known_grade` is where it came from).
Then run the resolver on it — one command runs the whole waterfall and grades each person, writing
`emails.json` and `hunter-receipt.json` beside it:

```bash
# whole batch -> writes emails.json (drafts-ready) + hunter-receipt.json
./.venv/bin/python email_resolver.py --batch daily/YYYY-MM-DD/candidates.json

# one person, or with a known published address to verify first
./.venv/bin/python email_resolver.py --domain mercury.com --first Immad --last Akhund
./.venv/bin/python email_resolver.py --domain uala.com.ar --first X --last Y --known real@uala.com.ar

# preview the plan, spend nothing
./.venv/bin/python email_resolver.py --domain X --first F --last L --dry-run
```

`candidates.json` is a list of `{name, first, last, domain, known, known_grade}` (`known` = a
published address research already found, else null; `known_grade` = where it came from —
`VERIFIED` for a team page, `HIGH` for a personal site, `MEDIUM` for a commit/paper). The order
it runs, per person:

1. **known/published** -> verify once, grade. Never blanked; it came from a real source.
2. **Email Finder** -> keep ONLY if `source_type == "found"` with sources. A `generated` result is a
   blind guess, discarded. A sourced hit with a weak score (< 90) is confirmed with the verifier
   before it is trusted.
3. **prober** (`email_prober.py`) -> catch-all control + pattern probes, the fallback for anyone
   Finder could not source.
4. **nothing** -> `GUESSED`, blank email, LinkedIn is the route.

It refuses to guess. On an accept_all domain it stops and tells you to grade `GUESSED` and leave
the cell empty, because on such a domain every candidate verifies whether or not it exists. If you
already know one real address at the company, pass `--known` and it infers the format and tests a
single candidate.

Its grades map directly onto the Email Confidence column: `VERIFIED` at score 90+, `HIGH` at 70+,
`MEDIUM` below that, and nothing at all when the control test fails.

**One caution.** Hunter's `accept_all` flag is not stable over time. A run in this project recorded
`vercel.com` as a catch-all and a later probe reported it was not. Trust the control test you ran
today, and say in the notes which way it came out.

### The Finder step runs inside email_resolver.py (do not curl it by hand)

`email_resolver.py` runs Email Finder automatically as step 2. It keeps a result only when
`source_type == "found"`, trusts a strong or already-valid hit, verifies a weak one, and discards
a `generated` guess. Grades are the resolver's, not a hand table: **VERIFIED at score 90+ on a
normal domain, HIGH on a catch-all domain, MEDIUM/LOW below that, GUESSED when nothing is found.**

The rule it enforces: **never record "no email" without the Finder having run.** An unused search
is worth nothing; a found address is worth the batch. Two founders on the first live run were
reachable only because Finder ran (`immad@mercury.com`, `patrickdorton@rational360.com`).

**Get the domain right first.** The resolver keys off the company domain, so a wrong domain
returns nothing and wastes the search. Confirm it from the company's own site before running.

### Hunter budget: spend where a call can pay

Credits are bought in bulk, so there is no monthly quota to ration and no per-run cap.
`email_resolver.py` owns the spend order (published -> finder -> prober) and only makes a call
that can pay: it never probes a published address, never re-tests a domain already known
`accept_all`, and stops probing a person once the ranked patterns fail. Read actual usage back
from `hunter-receipt.json` at the end of the run.

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

### Resolve the email with email_resolver.py

**First write `candidates.json`** into the day's `daily/YYYY-MM-DD/` folder from the verifier
reports: one object per person the batch keeps, `{name, first, last, domain, known, known_grade}`
(`known` is the published address research found, or `null`; `known_grade` is where it came from).
Then run the resolver on it — one command runs the whole waterfall and grades each person, writing
`emails.json` and `hunter-receipt.json` beside it:

```bash
# whole batch -> writes emails.json (drafts-ready) + hunter-receipt.json
./.venv/bin/python email_resolver.py --batch daily/YYYY-MM-DD/candidates.json

# one person, or with a known published address to verify first
./.venv/bin/python email_resolver.py --domain mercury.com --first Immad --last Akhund
./.venv/bin/python email_resolver.py --domain uala.com.ar --first X --last Y --known real@uala.com.ar

# preview the plan, spend nothing
./.venv/bin/python email_resolver.py --domain X --first F --last L --dry-run
```

`candidates.json` is a list of `{name, first, last, domain, known, known_grade}` (`known` = a
published address research already found, else null; `known_grade` = where it came from —
`VERIFIED` for a team page, `HIGH` for a personal site, `MEDIUM` for a commit/paper). The order
it runs, per person:

1. **known/published** -> verify once, grade. Never blanked; it came from a real source.
2. **Email Finder** -> keep ONLY if `source_type == "found"` with sources. A `generated` result is a
   blind guess, discarded. A sourced hit with a weak score (< 90) is confirmed with the verifier
   before it is trusted.
3. **prober** (`email_prober.py`) -> catch-all control + pattern probes, the fallback for anyone
   Finder could not source.
4. **nothing** -> `GUESSED`, blank email, LinkedIn is the route.

It refuses to guess. On an accept_all domain it stops and tells you to grade `GUESSED` and leave
the cell empty, because on such a domain every candidate verifies whether or not it exists. If you
already know one real address at the company, pass `--known` and it infers the format and tests a
single candidate.

Its grades map directly onto the Email Confidence column: `VERIFIED` at score 90+, `HIGH` at 70+,
`MEDIUM` below that, and nothing at all when the control test fails.

**One caution.** Hunter's `accept_all` flag is not stable over time. A run in this project recorded
`vercel.com` as a catch-all and a later probe reported it was not. Trust the control test you ran
today, and say in the notes which way it came out.

### The Finder step runs inside email_resolver.py (do not curl it by hand)

`email_resolver.py` runs Email Finder automatically as step 2. It keeps a result only when
`source_type == "found"`, trusts a strong or already-valid hit, verifies a weak one, and discards
a `generated` guess. Grades are the resolver's, not a hand table: **VERIFIED at score 90+ on a
normal domain, HIGH on a catch-all domain, MEDIUM/LOW below that, GUESSED when nothing is found.**

The rule it enforces: **never record "no email" without the Finder having run.** An unused search
is worth nothing; a found address is worth the batch. Two founders on the first live run were
reachable only because Finder ran (`immad@mercury.com`, `patrickdorton@rational360.com`).

**Get the domain right first.** The resolver keys off the company domain, so a wrong domain
returns nothing and wastes the search. Confirm it from the company's own site before running.

### Hunter budget: spend where a call can pay

Credits are bought in bulk, so there is no monthly quota to ration and no per-run cap.
`email_resolver.py` owns the spend order (published -> finder -> prober) and only makes a call
that can pay: it never probes a published address, never re-tests a domain already known
`accept_all`, and stops probing a person once the ranked patterns fail. Read actual usage back
from `hunter-receipt.json` at the end of the run.

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

### Facts about Max come only from BRIEF.md

**Every claim about Max in an email must appear verbatim in `BRIEF.md`'s "About Max" table.** No
inference, no embellishment, no detail carried over from a previous run's draft.

Pick the one or two facts that actually connect to this person. The table says when each applies.
A founder gets the turned-down-money decision; someone sales-led gets the $30k cold-calling; a
technical founder who had to learn to sell gets the math-and-sales combination. Listing all of them
is a résumé, and a résumé reads as someone asking for a job.

**The Middlebury rule is in `BRIEF.md` and is not optional.** No confirmed connection to the
college means Middlebury never appears in the subject line and never leads the email.

### The subject line is chosen per person

Read the subject-line table in `BRIEF.md` and pick the one true thing most likely to make **this**
recipient open it. A batch where every subject is identical means no choice was made.

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

**A daily run does not delete anything.** `--delete` exists for replacing a batch after Max changes
the copy, it is a dry run without `--yes`, and it is his call to make, not the run's. See
`README.md`, "Deleting drafts".

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

## Scratch scripts do not go in daily/

Write throwaway code to a temp directory, never into `daily/YYYY-MM-DD/`. That folder holds things
Max reads: the drafts, the research, the receipt. The 2026-08-15 run left an 11KB `file_batch.py`
next to the emails, which is one stray script per day forever and makes the folder harder to scan.

```bash
mkdir -p /tmp/outreach && ./.venv/bin/python /tmp/outreach/whatever.py
```

The only files that belong in `daily/YYYY-MM-DD/` are `NN-firstname-lastname.md`, `batch.md`,
`research.md`, `drafts.json` and `drafts-receipt.json`.

## Step 7 - File them

**Insert today's batch at the TOP of `To Contact`, at row 2. Do not append to the bottom.**

`To Contact` carries 232 rows of unqualified backlog import. A batch appended underneath lands
around row 240 and is effectively invisible, which is exactly what happened on the first three
runs. The people Max is meant to act on this morning must be the first thing he sees when he
opens the tab.

```python
ws.insert_rows(rows, row=2, value_input_option='USER_ENTERED')
```

`contacts-log.csv` can keep append order; it is a log, not a worklist.

Six tabs share one 20-column schema and the Apps Script row mover copies **by position**, so
column order is not negotiable:

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
- **LinkedIn** = required on every row, without exception. It is the contact route for everyone
  who has no email, which at this altitude is most of them. Run 5 left it blank on all five rows,
  which made five researched people unreachable by any means. LinkedIn blocks automated fetching,
  so the URL is often all that can be confirmed. Record it anyway; the URL is the deliverable.
- **Meeting Notes** = a short, concrete line on **what they do and why they are worth Max's
  time.** One or two sentences. Required on every new row. Before a meeting it is the "who is this
  and why do I care" line Max reads when scanning the tab; after a meeting the `update-contacts`
  skill appends the real notes below it.

  **Where a connection exists, name it here explicitly and precisely.** "Middlebury '92, sitting
  Term Trustee" is the single most useful thing on the row and must not be left implicit. Same for
  a shared city, sport, or employer.

- **Source** = where the lead came from *and* the route that found them, so a productive vein can
  be mined again. "Middlebury Board of Trustees roster" is useful; "research" is not.
**`Source` is free text, never a dropdown.** It records the route that found someone, which is
open-ended by nature ("Middlebury Board of Trustees roster", "public commits on vercel/next.js").
A fixed dropdown was tried and flagged every researched row as invalid. If a dropdown ever
reappears on that column, remove it.
- The email's **question** goes at the end of `Personalized Insert`, after the read, separated by
  a space. When someone replies weeks later, the sheet alone has to show what Max asked. Do not
  make him open a research file to remember his own question.
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

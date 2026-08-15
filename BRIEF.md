# Outreach brief

**Max edits this file. The daily-outreach skill reads it before doing anything else.**

It exists because the 8am run has nobody to ask. Change it whenever your focus shifts and the
next morning follows the new brief. When the skill is run interactively, it asks whether this is
still current before starting.

---

## How many per day

**1**

TEMPORARY: set to 1 for test-loop iterations, so each run is fast and cheap to
grade. Set back to 5 when testing is finished.

Range is 5-10. Fewer, better-researched people beat more shallow ones. Ship fewer than this
number rather than pad the batch.

## Who I want

**People at the top.** Founders and executives with real power, reach and networks. The bar is
that they are genuinely in the upper echelon of what they do, not merely senior.

In priority order:

1. **Impressive Middlebury founders and executives** - software or any industry. The school tie is
   the strongest opener available and nobody else can use it, so a Midd alum at this level is the
   single best target.
   *Examples of the level: George Arison, Middlebury alum who took Shift public and now runs
   Grindr. Parker Harris, Salesforce co-founder and CTO.*

2. **Unicorn founders.** Middlebury connection not required. Anyone who founded a company at or
   near that scale.

3. **Founders and CEOs of AI companies.** The frontier labs, the serious application companies,
   the infrastructure layer.

4. **Senior Wall Street** - partners, MDs, heads of desks, people running capital at scale.

5. **Forbes 30 Under 30 founders** who are actually successful, not just listed. Closest to Max's
   age of anyone here, and the most likely to reply.

6. **Anyone else genuinely operating at that altitude** - people whose introductions open doors.

## Who I do not want

- Anyone already in the tracker, on any tab
- Anyone not verifiably alive and currently in the role
- Anyone at a company that no longer exists under that name
- People who are only impressive on paper. Title without substance is not the bar; what they
  actually built or run is.

## What this means for the email

Aiming this high changes the writing, it does not change the rules.

- **The read has to be sharper, not longer.** People at this level get flattery constantly, so a
  real judgment about a specific decision they made is the only thing that stands out. Generic
  admiration is instantly recognisable and instantly deleted.
- **The question must be one they have not answered in a podcast.** If a quick search turns up
  them answering it publicly, it is the wrong question.
- **Still 90-95 words.** Seniority is not a reason to write more. It is a reason to write less.
  `elite-brevity-10min` goes to ~55 and is often the right choice at this altitude.
- Everything in `variants/` still applies: no em dashes, no availability windows, no banned
  phrases, judgment not compliment.

## Notes from previous runs

**2026-08-13.** This brief replaced an earlier one that told the skill to avoid household names on
the theory that they do not reply. Max overruled it, and the tracker supports him: people at
exactly this level already sit in `In Touch`. The old guidance is gone. Do not reintroduce a
seniority ceiling.

**2026-08-13.** Three separate research passes found **no Middlebury undergraduate alum currently
working in AI-for-education**. A thin vein rather than a search failure. Do not spend a whole
batch there.

**2026-08-13 (run).** The Middlebury vein is close to mined out *by the current search method*.
Middlebury's Wikipedia business list is now almost entirely consumed by the 261-name log, and
three plausible-looking names turned out not to be Middlebury at all (Steve Hafner is Dartmouth,
Justin B. Smith is Georgetown, Elizabeth Cutler is Colorado). The one found this run came off the
**Board of Trustees roster**, which is a better source than Wikipedia. Next runs should try the
Crunchbase "Middlebury alumni founded companies" hub (403 during this run) or Middlebury Magazine
back issues. This is a source problem, not a "no alumni left" problem.

**2026-08-13 (run).** Aiming this high costs deliverability. Four of five people this run had no
personal address anywhere public, because people at this altitude have staff between them and
their inbox. That is worse than the skill's "roughly a third" expectation and should be expected
to continue. LinkedIn and X are the real channels for this tier.

**2026-08-13 (second run).** The **Board of Trustees roster is the good Middlebury source** and it
is not exhausted. Cross-checking the roster against the tracker surfaced nine names never
contacted, of whom Alex Finkelstein (co-founder of Spark Capital, led Cruise, Discord and Wayfair)
is exactly the target this brief describes. Jon Owsley '92 (Managing Partner, L Catterton) and
Xi-An "Andrew" Li '99 (MD and Head of Greater China, Advent International) are still unclaimed and
are the obvious next two. Wikipedia's alumni list is mined out; the roster is not.

**2026-08-13 (second run).** **Hunter's `sources` field is noise and should not be trusted.** It
claimed an address appeared on a page which, when actually fetched, contained no address at all.
What does work: SMTP verification, control-tested. Probe a nonsense mailbox at the same domain
first. If the junk address is rejected and `accept_all` is false, then a "valid" result means the
mailbox really exists. That method turned three otherwise unreachable people into deliverable
drafts in this run, against the brief's expectation that this tier has no public addresses.

**2026-08-13 (third run).** The trustee roster produced two more, Jon Owsley '92 and Xi-An
"Andrew" Li '99, exactly as the second run predicted. **Six trustees remain unclaimed**: Sandhya
Douglas '93, Lisa van Santen '00, Janine Hetherington '95, Jasmin Johnson '05, Bob Sideli '77 and
Om Gokhale '22. Take these before going back to general search. Note that Middlebury's own
`/about-middlebury/<name>-<year>` profile pages exist for individual trustees and are a good cheap
primary source for class year and board seats.

**2026-08-13 (third run).** Deliverability was 3 of 5, better than the second run, and the
difference was **checking public commit metadata via the GitHub API**. Guillermo Rauch's address
came off his own commits to `vercel/next.js` after `vercel.com` turned out to be a catch-all. Any
target who has ever pushed code to a public repo should get this check before being written off.

**2026-08-13 (third run).** The SMTP control test does not always run. `lcatterton.com` returned
Hunter error 222 on two separate nonsense probes while verifying the real address cleanly, so the
control could not be completed. Treat that as "graded on Hunter's catch-all flag alone", one notch
weaker, and say so rather than pretending the control passed.

**2026-08-13.** Younger alumni leave a much thinner public trail, so they are harder to verify.
That is a research difficulty, not a reason to avoid them, and it matters less under this brief.

**2026-08-14 (run).** **The trustee roster is now mined out at this altitude.** All six names the
third run left are checked and only Sandhya Douglas '93 (Partner and Head of Strategic
Partnerships, Wellington Management) clears the bar. Bob Sideli '77 retired from Columbia in 2019;
Janine Hetherington '95 is a development officer at Williams; Om Gokhale '22 is a designer a few
years out; Jasmin Johnson Glaeser '05 and Lisa van Santen Gillanders '00 have no traceable current
role at all. Of the nine names the roster surfaced, four were worth having and all four are now
contacted. **Do not budget another run on this source.** The Crunchbase alumni-founders hub and
Middlebury Magazine back issues are still untried.

**2026-08-14 (run).** Deliverability was **5 of 5**, against the brief's expectation that this tier
has no reachable addresses. The method that did it is the catch-all control test, used in both
directions. Probe a nonsense mailbox at the domain first, then:

- **Control rejected** (not a catch-all): SMTP results are meaningful, so Hunter's `valid` can be
  trusted, *and* pattern probing becomes legitimate rather than guessing. `calendly.com` returned a
  score-5 dead end from the finder, but probing four patterns gave one deliverable and three
  undeliverable, which is a real mailbox. That is a VERIFIED address Hunter alone would have missed.
- **Control accepted** (catch-all): the domain accepts anything, so a `valid` or score-85 result
  proves nothing. Grade MEDIUM and say the control failed. `wellington.com` and `uala.com.ar` both
  landed here.

The asymmetry is the useful part: the control test upgrades as often as it downgrades.

**2026-08-14 (run).** Facts about people at this altitude move fast, and search-result summaries
lag them. Two of five were wrong on first pass: Marcos Galperin has not been MercadoLibre's CEO
since 2026-01-01 (he is Executive Chairman), and the Cursor and SpaceX deal was not a rumour but
closed the morning of the run. Both would have been role errors in line one. **Confirm the current
title against a dated primary source even when the person is famous enough that you think you know.**

**2026-08-14 (second run).** **Middlebury Magazine and the `alumni-and-families` section reopened
the vein the trustee roster closed.** Both Middlebury names this run came from there: Rob Tod '91
(founder of Allagash, and one of the college's *2026* Alumni Achievement Award winners) and Bill
Phelps '78 (from the "Hot Business" page). The award announcements and the alumni-stories index are
current, name class years, and are not consumed by the 261-name log. Crunchbase's alumni-founders
hub **403'd again**, so it remains untried and is probably not worth another attempt.

**2026-08-14 (second run).** The stale-title warning from the earlier run fired **twice more**, and
both would have been line-one errors. Middlebury's own Hot Business page calls Bill Phelps CEO of
Dave's Hot Chicken; he became Executive Chairman on 2026-01-05. Jonathan Ross is still called "Groq
CEO" almost everywhere; NVIDIA took Groq's assets on 2025-12-24 and he went with them. **Assume the
title is stale until a dated primary source says otherwise, and prefer a source the person
controls.** Where the current title cannot be nailed down, write around it: Ross's email rests on
the deal, which three outlets report, and never states his NVIDIA title.

**2026-08-14 (second run).** **A verified mailbox is not the same as the right person's mailbox.**
`jonathan@nvidia.com` verifies at score 100 with a clean control test, and it is certainly not
Jonathan Ross, who arrived eight months ago at a 36,000-person company. Bare first-name aliases
belong to whoever got there first. Ask "is this name unique at this company?" before trusting a
pattern hit: `amjad@replit.com` and `eric@ramp.com` are safe because the founder owns the name,
`rob@allagash.com` is safe at a 150-person brewery he owns, `jross@nvidia.com` is not and was
graded MEDIUM for that reason rather than for any doubt about deliverability.

**2026-08-14 (second run).** Deliverability was 5 of 5 again, and the prober did four of them with
no email-finder search at all. Useful trick: **the invalid results are the evidence.** At nvidia.com
`jonathanross@` and `jonathan.ross@` both came back hard invalid while `jross@` verified, which is
what proves the domain discriminates and the hit is real rather than a catch-all artifact.

**2026-08-14 (second run).** Hunter's quota **resets on the 15th**. Credits unspent on the 14th are
lost, so a run landing near the reset should spend freely rather than conserve. This run finished
with 15.5 credits that expired the next day.

**2026-08-14 (third run).** The **Alumni Achievement Award recipients page** is the same vein as
Middlebury Magazine and it is deeper than one year. The second run took Rob Tod off the *2026* list;
the **2025** list was sitting right above it, unread, and gave Bill Shufelt '05 (founder and CEO of
Athletic Brewing, ~$800M, category leader in non-alcoholic beer). The page lists recipients going
back decades with class years attached. Work backwards through it a year at a time before spending a
run on general search. Crunchbase was not attempted again, per the second run's advice.

**2026-08-14 (third run).** The catch-all control keeps paying. `athleticbrewing.com` rejected the
nonsense probe, which made pattern probing legitimate, and `bill@athleticbrewing.com` verified at
score 100 on the **first** candidate. Total cost 3 verifier calls and **zero** email-finder searches,
for a company that publishes only `press@`. The name-uniqueness test from the second run resolved
cleanly in the other direction this time: a bare first name is safe when the person **founded** the
company and was employee number one, which is the `rob@allagash.com` case, not the
`jross@nvidia.com` case. State which case you are in rather than just asserting the grade.

**2026-08-14 (third run).** For a heavily-interviewed founder, `ALREADY_ASKED_PUBLICLY` is worth more
than the whole rest of the report. Shufelt's famous fact, leaving a Steve Cohen hedge fund to brew
beer, is the most-asked question in his public life and would have made the email indistinguishable
from every other one he gets. The email was built instead on a decision **he raised himself and the
interviewer skipped past**: he quit drinking, then refused to market non-alcoholic beer to people who
quit drinking. Look for the thing the host moved on from too quickly. That is reliably the open space.

**2026-08-14 (third run), minor tooling note.** `verify_batch.py` globs `drafts*.json`, which now also
matches the `drafts-N-receipt.json` files the drafter writes, so receipt addresses get counted as
queued drafts and inflate the subject-collision and receipt checks. Harmless but noisy. Worth a
one-line exclusion at some point.

## About Max - the only facts you may use

**Everything an email says about Max comes from this list. Nothing else.** Do not infer, embellish,
or carry a detail over from a previous run. If it is not written here, it does not go in an email.

| Fact | Use it when |
|---|---|
| 20, Middlebury sophomore, studies **Applied Math** | identity. See the Middlebury rule below |
| Built an **AI teaching assistant**, won **$5K** in a pitch competition, piloting live in a school this fall | any education, AI, or product angle. The strongest single asset |
| **Turned down money for it** despite having the opportunity | talking to founders and investors about conviction. The best asset in this list, because it is a decision rather than an achievement |
| Made **$30k cold-calling SMBs** for his own business, which helps pay for school | sales, grit, going direct, anyone who started by selling |
| Working at a **YC startup, S26** | YC people, early-stage founders, anyone who values that signal |
| Loves math and technical work **and** loves sales | the combination is rarer than either half. Use with technical founders who had to learn to sell, or vice versa |
| Looking for his next idea; curious how founders had their **"hell yes" moment** | founders. Makes an excellent closing question |
| Played a lot of **tennis** | only if they have a real, sourced tennis connection |
| Lived in **Barcelona**; **living in Buenos Aires now** | anyone with a Spain, Argentina, or Latin America connection. He is there *now*, not going later |

### The Middlebury rule

**Middlebury is a wedge, and a wedge only works on someone it fits.**

- **Confirmed Middlebury connection** (alum, trustee, parent, faculty, gave a talk there): lead with
  it. Subject line and opening clause both. It is the strongest opener available and nobody else can
  use it.
- **No Middlebury connection**: do not lead with it, and **never put it in the subject line.** To a
  Snowflake CEO with no tie to the school, "Middlebury Sophomore" is a meaningless credential
  burning the most valuable line in the email. Mentioning he is a sophomore studying applied math is
  fine as plain identity; selling the school is not.

The first live run got this wrong: three of five subject lines were "Middlebury Sophomore, Hungry to
Learn", including one to Sridhar Ramaswamy, who has no connection to the college at all.

### Subject lines

**The subject is chosen per person, not defaulted.** Pick the one true thing most likely to make
*this* recipient open it:

| Situation | Subject |
|---|---|
| Confirmed Middlebury connection | `Middlebury Sophomore, Hungry to Learn` |
| Referral | `{Referrer} suggested I reach out` |
| Builder or technical founder | `20 Year Old Building an AI Teaching Assistant` |
| Sales-led or SMB background | `20 Year Old Who Cold Called His Way Through College` |
| Anyone else | write one from the strongest fact above that fits them |

**No two subjects in a batch may be identical, ever.** Not even when the same hook is genuinely
best for both. Run 5 sent "Middlebury Sophomore, Hungry to Learn" to two different Middlebury
alumni; the hook was right for each, the identical wording was not.

Vary the phrasing while keeping the hook:

> `Middlebury Sophomore, Hungry to Learn`
> `Midd Sophomore Building an AI Teaching Assistant`
> `Applied Math Sophomore at Middlebury`

If Max ever appears in both inboxes, or the two forward to each other, identical subject lines are
what make it look automated.

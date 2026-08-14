# Outreach brief

**Max edits this file. The daily-outreach skill reads it before doing anything else.**

It exists because the 8am run has nobody to ask. Change it whenever your focus shifts and the
next morning follows the new brief. When the skill is run interactively, it asks whether this is
still current before starting.

---

## How many per day

**5**

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
- **Still 85 words.** Seniority is not a reason to write more. It is a reason to write less.
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

## Current context about me

- 20, Middlebury sophomore, applied math (multivariable calculus, differential equations)
- Building an AI teaching assistant for Middlebury STEM courses
- Won $5K at MiddChallenge with a co-founder
- Interviewing with Entrepreneur First
- Running AI integration work for SMBs through MotionTech
- Heading to Buenos Aires next fall to study at UBA

Keep this current. It is what makes the "what I am building" line in each email true.

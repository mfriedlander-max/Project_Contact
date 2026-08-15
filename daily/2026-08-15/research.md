# Research, 2026-08-15

Every claim that reached an email, with the source behind it. One verifier per person, dispatched
in parallel, each told the person was already chosen.

**Middlebury: none of the five.** Checked individually, and in two cases checked hard enough to be
worth recording. Nobody in this batch gets the school in a subject line or an opening clause.

---

## Sourcing note on candidate selection

The brief's priority 1 is impressive Middlebury founders and executives. Five searches and four
direct page fetches against the sources the brief's own notes recommend produced **nothing new at
this altitude**:

- `alumni-and-families/stories` index, page 1: nine stories, and the only two at this level are Rob
  Tod '91 and Robynne Maii '96, both contacted on 2026-08-14.
- `alumni-and-families/innovative-startup-profiles`: names exactly two people, Brett Perlmutter '23
  and Sam Segal '23, both already in the tracker.
- `innovation-hub/middlebury-entrepreneurs`: names one person, Craig Wilson, a Collaborative Fund
  venture partner who teaches the course. No class year given, no evidence he is an alum.
- `ways-engage/alumni-businesses` 301-redirects to `midd2midd.middlebury.edu`, which is the
  PeopleGrove directory and is behind authentication.
- Crunchbase alumni-founders hub: not attempted, per the second run's advice after two 403s.

So this batch is drawn from the brief's priorities 2 through 6. That is a source problem, not an
absence of alumni, and it is now the third consecutive run to hit it.

---

## 1. Christina Cacioppo, co-founder and CEO, Vanta

**Current role, dated primary:** Vanta's own newsroom, 2026-04-29, titles her CEO and founder and
quotes her: https://www.vanta.com/resources/vanta-crosses-300m-in-arr-as-growth-accelerates .
Corroborated by Fortune the same day, and by an hour-long interview in her own voice on 2026-03-31
(https://cheekypint.substack.com/p/compliance-at-scale-and-why-tam-is).

**Proof of life:** commit on `christinac/dotfiles`, branch `main`, authored 2026-02-16 (GitHub API).

**Middlebury:** none. Stanford BA Economics and MS Management Science and Engineering, stated by her
in her own 2010 Union Square Ventures introduction post
(https://www.usv.com/blog/a-new-member-of-the-usv-team). Ohio native.

**The claim in the email:** she did not raise a real round until Vanta reached $10M ARR, ten times
the conventional threshold. Source: https://review.firstround.com/vantas-path-to-product-market-fit/
("deliberately waiting until 10x the conventional $1 million threshold"). YC seed spring 2018; the
$50M Sequoia Series A closed May 2021.

**Precision that matters.** This was **not** literal bootstrapping. A YC seed existed. The email says
"waiting until $10M ARR to raise," which is the accurate framing, and does not say bootstrapped.

**Why the question is unasked.** She has told the Vanta origin story on at least eight recorded
shows. What nobody asks about is TeachAPCS, an open AP Computer Science curriculum she built and
published (repo `christinac/teachapcs`, created 2014-09-08, CC BY-NC-SA) and then walked away from,
before betting a company on a market she had herself sized at roughly zero dollars ("The market for
startups getting SOC 2 in 2018 was zero dollars. Truly zero," Cheeky Pint, 2026-03-31). The email
asks the conviction counterfactual rather than the market-sizing one, because the conviction
question is the one that rhymes with Max's own turned-down money.

**Cut, deliberately:** a Bridgewater Associates stint. It appears in no primary source. The verifier
traced it to a different person of a similar name in Bridgewater, New Jersey. It is not in the email.
Also cut: any year for the Hoot sale (sources conflict) and any Dropbox start date (her own site says
"c 2015-16," third parties say 2014).

**Email.** `c@christinacacioppo.com`, graded **HIGH**. Published on her own site behind Cloudflare
email obfuscation, decoded from the `data-cfemail` payload, and independently the git author address
on her own repos 2012-2016. The prober's catch-all control on `christinacacioppo.com` **passed** (the
domain rejected a nonsense mailbox) and four other patterns came back hard invalid, which is what
proves the domain discriminates. The `c@` address itself was not directly probed: the prober did not
recognise a single-letter local part as a known pattern and fell back to ranked candidates. Cost 5
verifier calls, the most expensive probe of the run and the least productive.

---

## 2. Clément "Clem" Delangue, co-founder and CEO, Hugging Face

**Current role, dated primary:** his own GitHub profile, https://api.github.com/users/clmnt , bio
"Co-founder & CEO @huggingface", `updated_at` 2026-03-17. Corroborated by CBS "Face the Nation"
2026-08-02 and CNBC 2026-08-03.

**Proof of life:** commit authored to `huggingface/ml-intern` on 2026-04-25 (GitHub API).

**Middlebury:** none. Educated entirely in France, ESCP Business School, Paris.

**The claims in the email.** UniShared was a collaborative note-taking platform for students, covered
by Forbes on 2012-09-17 when he was 23 and named as founder
(https://www.forbes.com/sites/ricardogeromel/2012/09/17/unishared-revolution-in-online-education-beyond-coursera-edx-and-udacity/).
The employee years come from the bio **he submitted to Congress himself** on 2023-06-22: "Clement
started his career in product at Moodstocks, a machine learning startup for computer vision
(acquired by Google in 2016)"
(https://www.congress.gov/118/meeting/house/116078/witnesses/HHRG-118-SY00-Bio-DelangueC-20230622.pdf).
Hugging Face was co-founded in 2016.

**Deliberately imprecise.** The email says "four years of product jobs at other people's companies"
and names no employer beyond that and no title. The second employer, Mention, and the titles attached
to it trace only to a podcast episode summary, so the shape is usable and the specifics are not.

**Why the question is unasked.** Open versus closed source, China, the AI bubble, the chatbot origin
story and the OpenAI agent breach are all saturated, several of them within the last fortnight. The
four years he spent working for other people between his own two founding attempts appear in his own
congressional bio as a single clause and are, as far as three passes could find, never asked about.

**Cut:** any valuation (the $4.5B figure is from 2023 and the 2026 numbers are aggregator-only), any
headcount (he says ~200, aggregators say 769, unresolved), and any city (his GitHub says New York,
Sequoia describes him in North Miami Beach).

**Email.** `clementdelangue@gmail.com`, graded **MEDIUM**. It is the only address across 100 sampled
commits of 6,582, and it is still current: it authored the 2026-04-25 commit. The prober verified the
mailbox live at score 92 with the catch-all control passed. The grade stays MEDIUM because the
provenance is commit metadata on a personal Gmail, which he may well filter, not a mailbox anyone
published as his. Deliverable is not the same as read, and this is the deliverable case.

---

## 3. Eric Simons, co-founder and CEO, StackBlitz (Bolt.new)

**Current role, dated primary:** https://bolt.new/blog/security-audit-on-publish , 2026-07-30,
authored by "Eric Simons, CEO of Bolt.new" on the company's own domain. Corroborated by his bylined
Fortune op-ed of 2026-01-02, whose author bio names him CEO and co-founder of StackBlitz.

**Checked and cleared:** no acquisition, merger or rename. StackBlitz, Inc. is still the entity;
both stackblitz.com and bolt.new carry 2026 StackBlitz copyright.

**Middlebury:** none, and stronger than none. He skipped college on purpose and wrote the Fortune
piece about it: "Fifteen years ago, at 18, I made what many considered a bold bet: I skipped college."
Leading with a liberal arts college would have been the worst available opener. The email names Max
as a sophomore studying applied math, which is plain identity, and sells the school nowhere.

**The claims in the email.** Lesson plans for teachers: ClassConnect, later Claco, "GitHub for
teachers," TechCrunch 2012-09-26
(https://techcrunch.com/2012/09/26/after-2-months-of-squatting-at-aol-eric-simons-launches-claco-the-github-for-teachers).
Teaching people to code: Thinkster.io, confirmed in his own Medium post of 2019-01-09 handing it to
Joe Eames. Handing them the machine: StackBlitz, founded 2017, and WebContainers, announced
2021-05-20 under his byline on the company blog.

**Why the question is unasked.** The AOL office story and the $0-to-$20M ARR story are the two things
he is asked in every appearance, including the title of a February 2026 podcast episode. Both are off
the table. Nobody asks why ClassConnect failed or what it taught him about teachers as a customer,
which is the exact problem Max meets this autumn.

**Cut:** every runway and layoff specific (the "$80K ARR, seven people, 90 days" version traces only
to secondary retellings, and the only primary is Fortune's "our runway was tightening"), and every
revenue or valuation number, because no current one exists publicly.

**Email.** `eric@esft.com`, graded **VERIFIED**. Provenance is his own personal domain, listed in the
`blog` field of his GitHub profile, and it is his git author identity on stackblitz repos as recently
as 2024-10-02. The prober's catch-all control on `esft.com` **passed** and the address verified valid
at score 90 on the first candidate, for 2 verifier calls. The name-uniqueness test from the
2026-08-14 runs resolves cleanly: this is the `rob@allagash.com` case, not the `jross@nvidia.com`
case, because he owns the domain personally. Note `eric@stackblitz.com` appears in no commit metadata
and was not used.

---

## 4. Martín Migoya, co-founder, Chairman and CEO, Globant

**Current role, dated primary:** SEC 6-K EX-99.1, Q2 2026 earnings release, **2026-08-13**, two days
ago: "explained Martín Migoya, Globant's CEO and co-founder"
(https://www.sec.gov/Archives/edgar/data/1557860/000110465926095916/tm2623064d1_ex99-1.htm). Also his
**personally filed Form 3** of 2026-03-18, relationship self-declared "Chairman & CEO"
(https://www.sec.gov/Archives/edgar/data/1856986/000162828026019466/wk-form3_1773867309.xml), and a
Section 302 certification he signed on the FY2025 20-F.

**A false alarm, chased and cleared.** Search results surfaced a claim that a "Jeff Smith" had been
promoted to CEO. The underlying SEC filing shows the real event: COO Patricia Pomies resigned
effective 2025-07-31 and was not replaced. No CEO change. This is exactly the stale-title trap the
brief has now recorded four times, arriving from the opposite direction.

**Middlebury:** none, confirmed two ways. Middlebury's own site search returns zero results for both
"Migoya" and "Globant" against an index proven live by a control query, and EDGAR full-text search
across every Globant filing returns zero hits for "Middlebury" despite those filings carrying full
bios for every director and officer.

**The claims in the email.** 27,000-person company: 27,411 Globers per the 6-K of 2026-08-13 (the
20-F says 28,773 at 2025-12-31; marketing copy says "more than 28,500," and the SEC figures win).
Glob.AI priced per output rather than per hour: opened to the whole market 2026-08-06, priced "per
output or per consumption, never per seat or per hour" (investors.globant.com). Dismantling the
economics that built it, at the moment defending them would be easier: Time and Materials revenue
**fell in absolute dollars**, $1,714.1M in 2024 to $1,638.5M in 2025, FY2026 revenue guided at -1.1%
to +0.3%, and the shares were around $38.50 in May 2026, down 39% year to date against a peak above
$350 (20-F FY2025; 6-K 2026-08-13; Bloomberg Línea 2026-05-15). The judgment is that he is undercutting
his own billable hour while the market punishes him for it, which is a position, not a compliment.

Trainee at Repsol-YPF: stated in Globant's own SEC-filed bio, which appeared in 24 filings from the
2013 draft registration statement through the 20-F filed 2020-02-28, and in none since. The email
asks about the job. It does not assert why the sentence stopped appearing, because that motive is not
documented.

**Why the question is unasked.** The four friends in a bar in 2003, the 2014 NYSE IPO, whether AI
replaces engineers, and the AI Pods pitch are all exhausted. The decade before 2003 is not: the
trainee job, Origin BV, Tallion, and the unexplained two-year gap between founding in 2003 and
becoming CEO in 2005, which 13 years of filings state identically and none explain.

**Email: none.** `globant.com` is a confirmed catch-all: the prober's control probe was accepted, so
every candidate would verify whether or not it exists. Graded **GUESSED**, Email cell blank. The
routes are LinkedIn (`linkedin.com/in/migoya`, confirmed from two independently fetched third-party
pages carrying the link) and X (`@migoya`, loaded live, 61.4K followers, posting as recently as
2026-08-06). Cost 1 verifier call.

**Process note.** The verifier assigned to Migoya spawned a sub-agent of its own, which the skill
forbids. Its output corroborated rather than contradicted the parent report, so nothing was
discarded, but the batch consumed six agents rather than the five the cap allows.

---

## 5. Boaz Weinstein, founder and CIO, Saba Capital Management

**Current role, dated primary:** Form ADV filed 2026-05-29, Schedule A direct owners: "WEINSTEIN,
BOAZ, RONALD, CIO, PARTNER, FOUNDER (SABA CAPITAL)," ownership code E, control person yes
(https://reports.adviserinfo.sec.gov/reports/ADV/154362/PDF/154362.pdf). Also a Schedule 13D filed
2026-08-03 naming him a reporting person, and a 2026 DEF 14A giving his date of birth and his role as
President of the Saba Capital Income and Opportunities Fund.

**Proof of life:** 13F-HR filed 2026-08-14, ten 13G/A filings 2026-08-13.

**Middlebury:** none. Stuyvesant High School 1991 and the University of Michigan, BA Philosophy.

**The claim in the email.** The 2008 loss was not a directional blow-up. He was running negative-basis
trades, long corporate bonds hedged with CDS, and after Lehman the bonds fell while the CDS market
seized. He wanted to buy **more** protection, telling traders "the primary objective is to get as flat
as possible to the market." Deutsche Bank's risk managers, in what the Wall Street Journal called
contentious conference calls, told him to scale back or sell; he pleaded for more freedom and was
refused. And then: "Some positions the bank held onto rebounded by about $600 million in January."
Source, read in full facsimile, WSJ 2009-02-06:
https://utstat.utoronto.ca/sharp/Files/Press%20srticles%20and%20other%20stuff%202009/WSJ%2020090209/Weinstein,%20Wang,%20Ackerman%20at%20Deutsche%202009%20v01.pdf

So the email's judgment, that he lost an argument rather than a trade, is a reading of the reported
sequence and not an invention.

**Why the question is unasked, and why the email is 64 words.** The London Whale is the standard
opener and was used verbatim by Fox Business on 2026-03-23. It is not mentioned. More importantly, when
Institutional Investor profiled him in 2020 he asked the reporter to stay off his family, personal
matters, career history and outside interests. He is guarded about exactly the biography a flattering
cold email reaches for, so the middle of this email is a decision rather than a life story, and
`elite-brevity-10min` is the right variant for a man who does not want to be admired at length.

**Corroborated after the fact.** A second report, from a sub-agent the Weinstein verifier spawned
against the skill's cap, arrived after this batch was already filed. It independently reached the same
WSJ passage, the same $600 million, and the same conclusion: across eight dated interviews read in
full, **the 2008 loss is never once asked about**, and Barry Ritholtz's two-hour biographical
interview walks up to it and steps around it. So the email's angle is confirmed rather than merely
plausible.

That report also carried one fact the first verifier missed entirely, now added to his sheet row:
**on 2026-06-11 he lost at the US Supreme Court**, 6-3, in *FS Credit Opportunities Corp. v. Saba
Capital Master Fund*, No. 24-345, which held that the Investment Company Act creates no private right
of action (https://www.supremecourt.gov/opinions/25pdf/24-345_i42k.pdf). He had won every lower court
on the merits and then lost the enforcement mechanism, and dropped his ECAT suit six weeks later. It
is the largest fact in his current career and it is not in the email, because the email was written
before the report landed.

**Walked back after the fact.** Meeting Notes originally stated his 2012 gift to Stuyvesant as $1M.
The first verifier sourced the named library to an alumni newsletter of December 2018; the second
explicitly could not verify the dollar figure from any primary page. The row now says "a major gift"
and warns against repeating the number. It was never in the email.

**Cut:** the chess-got-him-the-Merrill-job story (his own account contradicts it: a flyer posted at
Stuyvesant by Janine Crane), the MIT blackjack team (he joined colleagues who had been on it, he was
not on it), the Newsday contest detail, and any single AUM figure, because the three available 2026
numbers, $6.1bn firm-stated, $18.3bn regulatory, and $3.9bn of 13(f) securities, measure three
different things.

**Email: none.** `sabacapital.com` is a confirmed catch-all. Its published addresses, `ir@`, `press@`,
`hr.jobs@`, `brw@` and `saba@`, are all generic and none reach him. Note `brw@` matches his initials
but is far more likely the ticker of the Saba Capital Income and Opportunities Fund, sitting as it
does beside `ir@` on a contact page. Graded **GUESSED**, Email cell blank. Route is X,
`@boazweinstein`, where he posts campaign letters himself. Cost 1 verifier call.

---

## Hunter spend

Opened the run at **8 email-finder searches** and 17 verifications remaining. The skill's table puts
anything under 10 searches at "no Hunter at all, public sources and the prober only," so **zero
email-finder searches were used**, exactly as on the fifth run of 2026-08-14.

Verifier calls, 11 of the 12 allowed:

| Domain | Calls | Outcome |
|---|---|---|
| esft.com | 2 | control passed, `eric@esft.com` valid at 90, VERIFIED |
| gmail.com | 2 | control passed, `clementdelangue@gmail.com` valid at 92 |
| christinacacioppo.com | 5 | control passed, 4 candidates hard invalid, `c@` not directly tested |
| globant.com | 1 | accept_all, stopped |
| sabacapital.com | 1 | accept_all, stopped |

That leaves **8 searches and roughly 6 verifications** for the rest of the month.

The christinacacioppo.com probe is the one to learn from. Her address was already published on her own
site, and the skill says never to spend a call on someone whose address is already published. Spending
five to test four patterns that were never going to be right was the wrong call, and the control
result it did buy, that the domain discriminates, was worth one call, not five.

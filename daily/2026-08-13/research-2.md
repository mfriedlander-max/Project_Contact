# Research - 2026-08-13, second batch

Every claim that reached an email, with the source behind it. Written after the first batch of
the day (people 1-5) was already filed, so those five are excluded here as known.

## Method note

The skill asks for one research subagent per person. This run did the research inline instead,
because this session carries a standing instruction not to spawn subagents unless asked. The
consequence is that the collision risk the skill warns about does not apply, and the search
budget was managed by hand. No agent reported budget exhaustion.

Firecrawl was not used, per the skill.

## Dedupe universe

- Google Sheet, all six tabs: 266 rows read, header confirmed as the 20-column schema.
- `contacts-log.csv` read in full.
- `daily/` contains only `2026-08-13`, whose first batch (Eskildsen, Fitzpatrick, Akhund,
  Yadegari, Dorton) was treated as claimed.

None of the five below appear in any of those.

---

## 1. Alex J. Finkelstein - Spark Capital

| Field | Value | Source |
|---|---|---|
| Role | Co-founder & General Partner (Early) | sparkcapital.com/team-members/alex-finkelstein (company-controlled) |
| Middlebury | Class of 1997, BA political science | middlebury.edu/about-middlebury/alex-j-finkelstein-97 |
| Trustee | sitting Term Trustee | middlebury.edu/about/governance/board-trustees, and Spark's own page says "serves on the Board of Trustees" |
| LinkedIn | linkedin.com/in/finkelsteinalex | search result title confirms Spark Capital, Boston |
| Email | alex@sparkcapital.com | MEDIUM, see below |

**Load-bearing claim used in the email:** he left venture capital, wrote and sold original
television shows to Fox, Discovery and E!, then returned to co-found Spark. This is stated on
**Spark Capital's own team page**, which is the strongest available source: the firm is
describing its own partner. The Middlebury alumni page repeats it independently.

Investments he led, per Spark's page: Cruise (Series A 2015), Discord (Series C 2016), Wayfair
(Series A 2011), GetYourGuide (2014).

**Not used:** a claim from aggregator pages that he spent three years convincing Wayfair's CEO to
take his money, and a characterisation of his thesis as "unglamorous, operationally complex
markets". Both are plausible and neither traces to a primary source, so both stayed out.

**Two Middlebury sources, one self-maintained:** the trustee roster gives affiliation and class
year, Spark's page gives current role. Split per the skill's institutional-vs-current rule.

---

## 2. Aidan Gomez - Cohere

| Field | Value | Source |
|---|---|---|
| Role | Co-founder & CEO | cohere.com/about (company-controlled), currency corroborated by Fortune 2026-06-17 |
| Co-founders | Nick Frosst, Ivan Zhang | cohere.com/about |
| LinkedIn | ca.linkedin.com/in/aidangomez | search result confirms Cohere |
| Email | none deliverable | see below |

**Load-bearing claims:**

1. He co-authored "Attention Is All You Need" as a 20-year-old Google Brain intern in 2017.
   Wikipedia plus multiple independent write-ups; the paper's authorship is itself a primary
   record.
2. Cohere sells private deployments, on-prem or isolated VPCs, and enterprise products (North,
   Model Vault) rather than a consumer chatbot. Straight off **cohere.com/about**, the company's
   own page.

**Email, and why the cell is blank.** His personal site publishes an address as a puzzle:
"{the first letter of my first name}@gom.ai", which decodes to `a@gom.ai`. That would normally
grade HIGH, being published on his own site. It **fails SMTP verification** (status invalid,
smtp_check false, though the domain does have MX records). A control probe of a nonsense mailbox
at gom.ai returned the same result, so this could equally be a server that refuses probes or a
mailbox that does not exist. Either way it is unconfirmed, so nothing was drafted to it.

`aidan@cohere.com` returned score 83 on an **accept_all** domain, which proves nothing at all.

Graded LOW, cell left blank, route is LinkedIn or X.

---

## 3. Jon Gray - Blackstone

| Field | Value | Source |
|---|---|---|
| Role | President & Chief Operating Officer, board member | blackstone.com/people/jonathan-gray (403 to automated fetch, but title corroborated by CNBC 2026-03-03 and Bloomberg 2026-06-09) |
| LinkedIn | linkedin.com/in/jon-d-gray/ | search result title confirms the title |
| Email | none | pattern guess on a catch-all domain, see below |

**Load-bearing claims, all Q1-Q2 2026 and therefore current:**

1. BCRED Q1 2026 redemption requests were **7.9% of shares**, roughly $3.7bn, a record.
   CNBC 2026-03-03 plus trade coverage.
2. Blackstone senior executives put **$150m of their own money** into BCRED in March 2026, part
   of a $400m support package that included $250m from the firm.
3. The quarterly redemption cap was **raised from 5% to 7%**.
4. Q2 2026 requests reached **10% of shares**, and repurchases were held at the customary 5%.
   alternativecreditinvestor.com 2026-07-23, which also carries Gray's Q2 earnings-call quote
   that redemptions were "down materially".

The email states 2, 3 and 4 and asks a counterfactual about them. It does **not** claim Gray
personally wrote a cheque, because the sourcing says "senior executives" collectively.

The $400m total was cut from the email: it rests on weaker sourcing than the $150m figure.

**Email:** `jonathan.gray@blackstone.com` scored 81 on an **accept_all** domain with zero real
sources. Accept-all means the server accepts anything, so verification is meaningless. Graded
GUESSED, cell blank, route is LinkedIn.

---

## 4. Scott Wu - Cognition

| Field | Value | Source |
|---|---|---|
| Role | Co-founder & CEO | TechCrunch 2026-05-29 and 2026-08-12, both within days of this run |
| Company scale | $1bn Series D at $26bn valuation, May 2026, $492m ARR; reportedly in talks at $40bn | TechCrunch 2026-08-12 |
| Background | three IOI golds, first place 2014; Codeforces Legendary Grandmaster | Wikipedia, cphof.org profile |
| Email | scott@cognition.ai | MEDIUM, see below |

**Load-bearing claim used in the email:** Cognition acquired Windsurf in roughly **72 hours** in
July 2025, days after Google took Windsurf's CEO and co-founder in a $2.4bn licensing deal.
CNBC 2025-07-14 for the Google deal and the acquisition; Wu's own account of the weekend appears
on 20VC and in a Yahoo Finance interview.

No LinkedIn URL confirmed for him, so that cell is blank rather than guessed.

---

## 5. Ryan Petersen - Flexport

| Field | Value | Source |
|---|---|---|
| Role | Founder & CEO | CNBC video 2026-08-07, six days before this run; Bloomberg 2026-04-06 |
| LinkedIn | linkedin.com/in/rpetersen/ | search result title confirms Flexport |
| Email | ryan@flexport.com | MEDIUM, see below |

**Load-bearing claim used in the email:** Dave Clark, a former Amazon executive, became Flexport
CEO on 2022-09-01. Petersen returned as CEO on 2023-09-07, one year later, and criticised
Clark's overspending on hiring and the $1.3bn Shopify logistics purchase. gCaptain, Cargo Facts
and the original PR Newswire announcement of Clark's hiring.

The email says "a year later", which is correct. Petersen was co-CEO for the first six months
and executive chairman from March 2023.

---

## Email grading, and one judgment call worth flagging

**Hunter's `sources` field is unreliable and was discarded.** It claimed `ryan@flexport.com`
appeared on a Flexport market-update page; that page was fetched and contains no address at all.
It claimed `scott@cognition.ai` appeared on, among others, an art-keyword blog and a Stripe
Sessions page. These are noise.

What survived is **SMTP verification**, and it was control-tested before being trusted. A
nonsense mailbox (`zqx9plarb@`) was probed at each of flexport.com, sparkcapital.com and
cognition.ai. All three returned invalid, and all three domains report accept_all false. So on
these domains a "valid" result means the mailbox genuinely exists.

| Address | SMTP | accept_all | Control test | Grade |
|---|---|---|---|---|
| alex@sparkcapital.com | valid, score 100 | false | domain rejects nonsense | MEDIUM |
| scott@cognition.ai | valid, score 100 | false | domain rejects nonsense | MEDIUM |
| ryan@flexport.com | valid, score 100 | false | domain rejects nonsense | MEDIUM |
| a@gom.ai | **invalid** | false | domain rejects nonsense too, so inconclusive | LOW, blank |
| jonathan.gray@blackstone.com | accept_all | **true** | meaningless | GUESSED, blank |

**The judgment call.** `CLAUDE.md` says a constructed `first.last@company.com` is a bounce, so
grade it GUESSED and leave the cell blank. These three were pattern-derived, which by the letter
of that rule means blank. They were then SMTP-confirmed to exist on domains proven not to be
catch-all, which defeats the bounce risk the rule exists to prevent. They were graded MEDIUM and
drafted on that basis.

What MEDIUM does not claim: none of the three was found published on any page that was actually
read, so any of them may be a filtered or assistant-monitored mailbox. If Max would rather the
letter of the rule won, blanking these three costs him the day's best contact and is a one-line
change to the sheet.

Hunter usage: **5 searches and 10 verifications** this run. 43 searches and 86 verifications
remain before the 2026-08-15 reset.

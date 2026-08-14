# Research, 2026-08-14

Batch of 5, per `BRIEF.md`. Dedupe run against all six sheet tabs (276 names), `contacts-log.csv`
(278 rows) and `daily/2026-08-13/`. None of the five below appear in any of them.

**Method note.** Research was done in this session directly rather than by dispatching one
subagent per person as Step 2 describes. Session instructions for this run prohibited calling the
Agent tool unless the user asked for it, and the user's instruction was to follow the skill, not
to spawn agents. Practical effect: no cross-agent collision risk this run, and no agent hit a
search budget wall. Every source below was fetched or searched in-session.

---

## 1. Sandhya S. Douglas '93 - Wellington Management

| Field | Value |
|---|---|
| Role | Partner, Senior Managing Director & Head of Strategic Partnerships |
| Email | `sdouglas@wellington.com` |
| Confidence | **MEDIUM** (see below, control test failed) |
| LinkedIn | https://www.linkedin.com/in/sandhya-s-douglas/ |

**Sources.**
- `middlebury.edu/about-middlebury/sandhya-douglas-93` (fetched). Primary. Class of 1993, P'25.
  Partner, Senior Managing Director, Head of Strategic Partnerships at Wellington, there since
  2006. Prior: SVP at Brown Brothers Harriman, VP at SunTrust Capital Markets. Boards: Boston
  After School & Beyond (treasurer), City Year Greater Boston, Berklee Amplify Gala co-chair,
  Newburyport DEI Alliance. Previously board president of Troubadour and UTEC. Born in India,
  raised in Singapore.
- `middlebury.edu/about/governance/board-trustees` (fetched). Primary. Confirms she is a current
  **Term Trustee**.
- LinkedIn profile title (search result, not opened): "Sandhya S Douglas, CFA (she/her/hers) -
  Newburyport, Massachusetts". Newburyport matches the DEI Alliance detail in the Middlebury bio,
  so it is the same person.

**Currency split, per the skill.** Class year and trustee seat come from Middlebury's own pages,
which is the right source for those. Current employer is corroborated by the self-maintained
LinkedIn profile plus the location match. I did not open LinkedIn directly.

**Email.** Hunter finder returned `sdouglas@wellington.com`, score 85, but `accept_all: true`.
Control test: `qzx7nonsense4421@wellington.com` came back `accept_all / risky / smtp_check true`,
i.e. the domain accepts anything. **The control failed, so the mailbox is not confirmed to
exist.** Graded MEDIUM and used, not VERIFIED. This is Hunter's pattern confidence only.

**The read.** Twenty years compounding at one firm into the strategic partnerships seat, while
the outside hours go to out-of-school learning rather than to more finance. Stated as a
deliberate pairing, which is a judgment, not a compliment.

**Question.** What she has seen actually change outcomes for a kid outside class hours. Not
answered anywhere public that I found; she has no podcast footprint.

---

## 2. Tope Awotona - Calendly

| Field | Value |
|---|---|
| Role | Founder & CEO |
| Email | `tope@calendly.com` |
| Confidence | **VERIFIED** (SMTP, control-tested and discriminating) |
| LinkedIn | https://www.linkedin.com/in/bawotona/ |

**Sources.**
- `en.wikipedia.org/wiki/Tope_Awotona` and `en.wikipedia.org/wiki/Calendly` (search). Born Lagos,
  immigrated as a teenager, MIS degree University of Georgia 2002, sales career at Dell, IBM, EMC,
  Perceptive Software.
- TechCrunch, "Timing your bootstrap with Calendly's Tope Awotona" (2021-03-19). Independent of
  Wikipedia. Bootstrapping thesis in his own words.
- Multiple 2026 sources (Forbes profile, Clay dossier updated Jan 2026, April 2026 listing) show
  him still Founder & CEO. No report of a transition.

**Load-bearing facts used in the email.** ~$200K of his own savings including a 401k withdrawal,
launched 2013, no outside capital for eight years until the $350M round in Jan 2021 at $3B
(OpenView and Iconiq), retained a majority stake. Prior ventures (projectors, garden tools)
failed. All of this appears across Wikipedia, TechCrunch and Forbes independently.

**Email.** Hunter's finder was useless here: `tope.awotona@calendly.com`, score 5, unverified.
But `calendly.com` is **not** a catch-all: the nonsense control was rejected as undeliverable.
That makes SMTP probing meaningful, so I probed four patterns:

```
tope@calendly.com          valid / deliverable / score 100
tawotona@calendly.com      invalid / undeliverable
topeawotona@calendly.com   invalid / undeliverable
tope@calend.ly             invalid / undeliverable
```

Three siblings rejected and the nonsense control rejected, one accepted. The check discriminates,
so `tope@calendly.com` is a real mailbox. **VERIFIED.**

**The read.** A decade selling other people's software, then $200K of his own in and eight years
refusing capital, which is the reason he still owns most of it. The causal claim is the judgment.

**Question.** When he first knew Calendly could sell without him in the room. A sales question
from someone who sells, which is the point of pairing it with Max's $30k.

---

## 3. Michael Truell - Cursor (Anysphere)

| Field | Value |
|---|---|
| Role | Co-founder & CEO |
| Email | `michael@cursor.com` |
| Confidence | **VERIFIED** (Hunter valid, score 81, control-tested) |
| Contact route | https://x.com/mntruell |

**Time-sensitive. The SpaceX acquisition closed today, 2026-08-14.** I verified this rather than
trusting it, because the first search hits were low-quality aggregators.

**Sources.**
- `en.wikipedia.org/wiki/Cursor_(company)` (fetched). Deal closed **August 14, 2026**. Anysphere
  shares converted into 389,289,254 SpaceX Class A shares, implied equity value $60B. Cursor is
  now a wholly owned SpaceX subsidiary being integrated into SpaceXAI. Truell remains CEO.
- `en.wikipedia.org/wiki/Michael_Truell` (fetched). Born September 2000, so 25. Left MIT without
  graduating. Google intern on language models. Co-created the Halite AI competition in 2016.
  Founded Anysphere in 2022 with Sualeh Asif, Aman Sanger, Arvid Lunnemark. **April 2026: SpaceX
  secured an option to acquire Cursor for $60B, or pay $10B to collaborate instead.** Option
  exercised June 2026, all-stock.
- Truell's own X post (`x.com/mntruell/status/2088276379712528745`): "Cursor has officially joined
  SpaceX." His own account, so this is primary confirmation of the close.

**Deliberately not claimed in the email:** that he chose the sale unilaterally. The option was
SpaceX's to exercise. The email says "a structure where the alternative to selling was a $10
billion partnership", which is what the record supports.

**Email.** Hunter finder: `michael@cursor.com`, score 81, `verification.status: valid`. Control:
`qzx7nonsense4421@cursor.com` rejected as undeliverable, so the domain is not a catch-all and the
valid result means the mailbox exists. **VERIFIED.** GitHub was checked first per the run-3 note:
`github.com/mntruell` exists but has a null profile email and no public events or repos exposing
commit metadata, so that route produced nothing.

**The read.** Taking the $60B sale over the $10B partnership as a bet that the binding constraint
was compute rather than distribution or talent. A position, and one he has not publicly answered.

**Timing caveat for Max.** His inbox today is going to be a firehose of congratulations. The email
deliberately does not congratulate him, which is the only way it stands out today. If Max would
rather wait a week, that is a reasonable call and the draft does not go stale.

---

## 4. Marcos Galperin - MercadoLibre

| Field | Value |
|---|---|
| Role | Founder & **Executive Chairman** (no longer CEO) |
| Email | `marcos.galperin@mercadolibre.com` |
| Confidence | **VERIFIED** (Hunter valid, score 82, control-tested) |
| Reference | https://en.wikipedia.org/wiki/Marcos_Galperin |

**Sources.**
- Buenos Aires Herald, "Galperin steps aside as Mercado Libre CEO in 'generational change'"
  (fetched). Announced 2025-05-22; Ariel Szarfsztejn became CEO 2026-01-01; Galperin became
  Executive Chairman. His stated focus: "strategy, product evolution, culture, capital assignment
  decisions, some specific projects, and on how we will continue to apply artificial intelligence
  to transform our business." Direct quote: "I have seen technology companies struggle in that
  process. That's why I decided to lead it with plenty of time, on our own terms."
- Bloomberg (2025-05-21) and Yahoo Finance, same transition, independent of the Herald.
- SEC Form DEF 14A FY2026 for MercadoLibre Inc (CIK 0001099590) appears in results, which is the
  primary filing confirming the board role.

**Correction caught during research.** The first search framed him as CEO. He is not, as of
2026-01-01. Naming the wrong role in line one would have ended the email there, so the draft says
"handing over the CEO seat", which is accurate for an Executive Chairman.

**Email.** Hunter finder: `marcos.galperin@mercadolibre.com`, score 82, valid. Control:
`qzx7nonsense4421@mercadolibre.com` rejected as undeliverable, so not a catch-all. **VERIFIED.**
Whether a founder-chairman of a $100B+ company monitors it is a separate question; it is a real
mailbox, not necessarily a read one.

**The read.** He handed over everything except the AI transformation, which leaves the riskiest
work with the founder. That is a specific, sourced observation about how he drew the line.

**Question.** Why he kept that one and handed over the rest. The public quotes explain *why he
handed over*, not *why he kept AI*, so this is not something he has answered.

---

## 5. Pierpaolo Barbieri - Ualá

| Field | Value |
|---|---|
| Role | Founder & CEO |
| Email | `pierpaolo.barbieri@uala.com.ar` |
| Confidence | **MEDIUM** (catch-all domain, control failed) |
| LinkedIn | https://www.linkedin.com/in/pierpaolobarbieri/ |

**Sources.**
- `uala.com.ar/nosotros` (fetched). Company's own site. Names him as the person who "creó y lanzó
  Ualá en octubre de 2017". HQ at Cnel. Marcelino E. Freyre 3650, Buenos Aires.
- `belfercenter.org/person/pierpaolo-barbieri` (fetched). Harvard AB magna cum laude, Cambridge
  MPhil in Economic and Social History, Gates Cambridge Scholar, Ernest May Fellow 2011-2013,
  author of *Hitler's Shadow Empire: The Nazis and the Spanish Civil War* (Harvard University
  Press). Executive Director of Greenmantle. Argentine.
- `gmantle.com/people` (fetched). Greenmantle's own site confirms Executive Director.
- 2026 funding coverage (fintechfutures, Retail Banker International): $195M led by Allianz X at a
  **$3.2B post-money**, with Tencent, Soros Fund Management, D1 Capital and Stone Ridge
  participating. 11M+ customers, banking licences in Argentina, Mexico and Colombia.

**One claim I cut.** The Belfer page also says he "heads strategy for Brevan Howard Argentina."
That is likely stale given Ualá, and I could not date it, so it stays out of the email entirely.
I also cut an earlier draft line calling Argentina "the country whose monetary history you
studied" - his MPhil and his book are on Spanish Civil War economics, not Argentine monetary
history. That was an inference dressed as a fact, exactly the kind the skill warns about.

**Email.** Hunter finder: `pierpaolo.barbieri@uala.com.ar`, score 83, but `accept_all: true`, and
the control `qzx7nonsense4421@uala.com.ar` was accepted. **Control failed, so MEDIUM, not
VERIFIED.** Note that ContactOut lists the same address, but aggregators are not sources and this
does not upgrade the grade. No published address on `uala.com.ar` or `gmantle.com`.

**The read.** Economic historian running a macro advisory, then starting a bank in Argentina, with
11 million customers as the evidence the odd path was coherent.

**Question.** Which piece of the macro work actually changed a product decision inside Ualá.
Specific to him and not answerable by anyone else in this batch.

---

## Dropped, and why

The brief's third-run note listed six unclaimed Middlebury trustees and said to take them before
returning to general search. I checked all six against the roster and the brief's altitude bar.
**Only one of the six clears it.**

| Person | Verified as | Dropped because |
|---|---|---|
| Sandhya Douglas '93 | Wellington Partner, Head of Strategic Partnerships | **Kept.** |
| Robert V. "Bob" Sideli '77 | Former CIO, Columbia University Medical Center | **Retired in 2019.** The brief excludes anyone not currently in the role. |
| Janine Hetherington '95 | Senior development officer and director of women's philanthropy, Williams College | Accomplished, but not "founders and executives with real power, reach and networks". A development officer at a peer college is not this brief's altitude. |
| Om Gokhale '22 | Interdisciplinary designer, Cambridge MA; Recent Graduate Trustee | Class of 2022, working as a designer. Nothing near the bar yet. |
| Jasmin Johnson Glaeser '05 | Alumni Trustee | No primary source found for any current employer or role. Cannot verify, so cannot write. |
| Lisa C. van Santen Gillanders '00 | Term Trustee | Same. Her `middlebury.edu/about-middlebury/` profile 404s and no professional record surfaced. |

**This is the finding of the run.** The second and third runs treated the trustee roster as the
good, unmined Middlebury vein. It is now mined out *at this brief's altitude*: of the nine names
that roster surfaced, the three worth having (Finkelstein, Owsley, Li) went in previous runs and
Douglas goes today. The remaining five are trustees because they are devoted alumni, not because
they run things at scale. Next runs should not budget time here.

No candidate was dropped for a failed fact-check this run, and none was dropped for a missing
email.

## Hunter usage

Started the run at 18/50 searches used, 36/100 verifications used. Quota resets **2026-08-15**,
so spending was not constrained.

- **5 searches** (one per person): 18 -> 23 used, **27 remaining**.
- **9 verifications**: 5 nonsense controls, one per domain, plus 4 Calendly pattern probes.
  36 -> 45 used, **55 remaining**.

The control test paid for itself twice. It downgraded Wellington and Ualá from apparently-valid to
MEDIUM, and it upgraded Calendly from a score-5 dead end to a VERIFIED address, because knowing
the domain was not a catch-all is what made pattern probing legitimate rather than guessing.

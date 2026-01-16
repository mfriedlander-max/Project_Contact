# Middlebury Alumni Outreach System

This project helps find contact information for Middlebury alumni and generate personalized cold outreach emails.

---

## Branch Workflow (IMPORTANT - DO THIS FIRST)

**Each new outreach round gets its own branch.** This keeps contact lists and results organized.

### Existing Branches
- `main` - Base system files (scripts, prompts, templates)
- `round-1-middlebury-alumni` - First batch of 50 Middlebury alumni contacts

### Starting a New Round

When the user wants to work on a new set of contacts:

```bash
# 1. Create a new branch from main
git checkout main
git checkout -b round-X-descriptive-name

# 2. Add/update the contact CSV
# 3. Run email finder
# 4. Generate personalized emails
# 5. Commit results to this branch
git add -A
git commit -m "Round X: [description of contacts]"
```

### Branch Naming Convention
- `round-1-middlebury-alumni` - First round
- `round-2-tech-founders` - Second round (example)
- `round-3-vc-partners` - Third round (example)

### Switching Between Rounds
```bash
# View all rounds
git branch -a

# Switch to a specific round
git checkout round-1-middlebury-alumni

# Return to main for new round
git checkout main
```

---

## Conversation Starter

When starting a new session, ask the user:

```
I can help you with the Middlebury Alumni Outreach System. What would you like to do?

1. **Start a new round** - Create a new branch and find emails for new contacts
2. **Continue existing round** - Work on contacts from a previous round
3. **Write personalized emails** - Generate custom email inserts for outreach
4. **Review results** - Look at previously found contacts and emails

Before we start, I'll need a few things from you:
- Your contact list (CSV file location or paste the contacts)
- Hunter.io API key (for email finding)
- A name for this round (e.g., "tech-founders", "finance-execs")
```

---

## PHASE 1: Contact Discovery

### Required Inputs

1. **Contact CSV file** with columns:
   - Name, Company, Title / Role, Industry, LinkedIn URL
   - File location: `middlebury_contacts.csv`

2. **Hunter.io API Key**
   - Get free key at: https://hunter.io/users/sign_up
   - Free tier: 25 searches/month
   - Set as environment variable: `HUNTER_API_KEY`

3. **Optional API Keys** (for better results):
   - Apollo.io: `APOLLO_API_KEY` (50 free/month)
   - RocketReach: `ROCKETREACH_API_KEY` (5 free/month)
   - Clearbit: `CLEARBIT_API_KEY`

### Step-by-Step Process

#### Step 1: Prepare the Contact List
```bash
# Ensure CSV has proper header row (no empty first row)
# Required columns: Name, Company, Title / Role, Industry, LinkedIn URL
```

#### Step 2: Install Dependencies
```bash
cd /Users/maxfriedlander/code/Project_Contact
python3 -m pip install -r requirements.txt
```

Dependencies:
- requests>=2.28.0
- beautifulsoup4>=4.11.0
- dnspython>=2.3.0

#### Step 3: Run Email Finder
```bash
# Set API key and run
HUNTER_API_KEY='your_key_here' python3 email_finder.py -i contacts.csv -o results.csv

# Test with first 10 contacts
HUNTER_API_KEY='your_key_here' python3 email_finder.py -i contacts.csv -o results.csv --limit 10

# With SMTP verification (slower but more accurate)
HUNTER_API_KEY='your_key_here' python3 email_finder.py -i contacts.csv -o results.csv --verify
```

#### Step 4: Review Results

Output file `results.csv` contains:
- Name, Company, Title, Industry, LinkedIn URL
- Email 1, Email 1 Source, Email 1 Confidence
- Email 2, Email 2 Source, Email 2 Confidence
- Email 3, Email 3 Source, Email 3 Confidence
- All Emails (semicolon-separated)

**Confidence Levels:**
| Level | Source | Action |
|-------|--------|--------|
| HIGH | Hunter.io verified | Safe to use |
| MEDIUM | Partial match | Verify before important outreach |
| LOW | Pattern guess | Test with low-stakes email first |

### Email Pattern Generation

For contacts without verified emails, the script generates 8 pattern guesses:
1. `first.last@domain.com`
2. `firstlast@domain.com`
3. `flast@domain.com` (first initial + last)
4. `first_last@domain.com`
5. `first@domain.com`
6. `last.first@domain.com`
7. `f.last@domain.com`
8. `firstl@domain.com` (first + last initial)

---

## PHASE 2: Email Personalization

### Required Input
- Contact list with: Name, Company, Title/Role
- System prompt file: `email_personalization_prompt.md`

### The Email Template
```
Hello [Name],

My name is Max Friedlander, I am 20 years old, and a current Freshman at Middlebury. I am interested in entrepreneurship, ambitious, and curious about the world. [YOUR INSERT HERE]

I understand that you're very busy, but if you had 15 minutes to chat with me, I would love to introduce myself, and learn from you.

Best,
Max
```

### Process
1. Read `email_personalization_prompt.md` for the full system prompt
2. For each contact, generate ONE personalized sentence (15-25 words)
3. Follow all tone guidelines and avoid banned AI patterns

### Output Format
```
**[Name]** - [Company], [Title]
Insert: "[personalized sentence]"
Word count: [X]
```

---

## PHASE 3: Email Sending (Future)

### Gmail Integration Options
1. **Gmail API** - Most robust, requires OAuth setup
2. **SMTP** - Simpler, requires app password
3. **Manual** - Copy/paste generated emails

---

## Quick Reference Commands

```bash
# Full run
HUNTER_API_KEY='your_key' python3 email_finder.py -i contacts.csv -o results.csv

# Test run (first 10)
HUNTER_API_KEY='your_key' python3 email_finder.py -i contacts.csv -o results.csv --limit 10

# With verification
HUNTER_API_KEY='your_key' python3 email_finder.py -i contacts.csv -o results.csv --verify

# View branches
git branch -a

# Switch to round
git checkout round-X-name

# Create new round
git checkout main && git checkout -b round-X-name
```

---

## Files in This Project

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file - instructions for Claude |
| `email_finder.py` | Main email discovery script |
| `email_personalization_prompt.md` | System prompt for writing email inserts |
| `linkedin_scraper.py` | Optional LinkedIn automation |
| `quick_start.py` | Interactive guided setup |
| `middlebury_contacts.csv` | Input contact list |
| `results.csv` | Email search results |
| `contact_results_summary.md` | Organized results with all pattern guesses |
| `requirements.txt` | Python dependencies |

---

## Important Notes

- **Always create a new branch for each round** before adding contacts
- Always use the system prompt in `email_personalization_prompt.md` when generating emails
- Email inserts must be 15-25 words, no exceptions
- Avoid all banned AI patterns listed in the system prompt
- Start with HIGH confidence emails before trying pattern guesses
- The Middlebury connection is the hook - always lead with that
- Commit results to the round branch when done

---

## Round 1 Results Summary

Branch: `round-1-middlebury-alumni`

- **Total contacts:** 50
- **HIGH confidence emails:** 20
- **MEDIUM confidence:** 2
- **Pattern guesses only:** 28
- **Success rate:** 44%

See `contact_results_summary.md` for full details and all pattern guesses.

# Middlebury Alumni Outreach System

This project helps find contact information for Middlebury alumni and generate personalized cold outreach emails.

## What This System Does

1. **Phase 1: Contact Discovery** - Find email addresses using Hunter.io API
2. **Phase 2: Email Personalization** - Generate personalized email inserts using the system prompt
3. **Phase 3: Email Sending** - Send emails via Gmail (future)

---

## Before Starting: Gather Required Information

When a user wants to use this system, you need to collect the following information first.

### Ask the user for:

1. **Contact List**
   - Do they have a CSV file with contacts? If so, where is it located?
   - Required columns: Name, Company, Title/Role, Industry
   - Optional but helpful: LinkedIn URL

2. **Hunter.io API Key**
   - Ask: "Do you have a Hunter.io API key? If not, you can get a free one at https://hunter.io/users/sign_up (25 searches/month free)"

3. **Which phase they want to run:**
   - Phase 1: Find emails for contacts
   - Phase 2: Generate personalized email inserts
   - Phase 3: Send emails (requires Gmail setup)

---

## Phase 1: Contact Discovery

### Prerequisites
- Contact CSV file
- Hunter.io API key

### Commands to Run
```bash
# Install dependencies (first time only)
python3 -m pip install -r requirements.txt

# Run email finder
HUNTER_API_KEY='their_key' python3 email_finder.py -i their_contacts.csv -o results.csv

# Test with first 10 contacts
HUNTER_API_KEY='their_key' python3 email_finder.py -i their_contacts.csv -o results.csv --limit 10
```

### Output
- `results.csv` with found emails and confidence levels
- HIGH confidence = verified by Hunter.io
- MEDIUM confidence = partial match
- LOW confidence = pattern guess

---

## Phase 2: Email Personalization

### Prerequisites
- Contact list with Name, Company, Title/Role
- Load the system prompt from `email_personalization_prompt.md`

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

## Phase 3: Email Sending (Future)

Gmail integration options:
- Gmail API with OAuth
- SMTP with app password
- Manual copy/paste

---

## Key Files

| File | Purpose |
|------|---------|
| `email_finder.py` | Find emails using Hunter.io API |
| `email_personalization_prompt.md` | System prompt for writing email inserts |
| `contact_results_summary.md` | Results from previous runs |
| `results.csv` | Email search output |
| `middlebury_contacts.csv` | Example contact list |

---

## Conversation Starter

When starting a new session, ask the user:

```
I can help you with the Middlebury Alumni Outreach System. What would you like to do?

1. **Find emails** - I'll search for email addresses for your contacts
2. **Write personalized emails** - I'll generate custom email inserts for outreach
3. **Review results** - Look at previously found contacts and emails

Before we start, I'll need a few things from you:
- Your contact list (CSV file location or paste the contacts)
- Your Hunter.io API key (for email finding)
- Which contacts you want to prioritize
```

---

## Important Notes

- Always use the system prompt in `email_personalization_prompt.md` when generating emails
- Email inserts must be 15-25 words, no exceptions
- Avoid all banned AI patterns listed in the system prompt
- Start with HIGH confidence emails before trying pattern guesses
- The Middlebury connection is the hook - always lead with that

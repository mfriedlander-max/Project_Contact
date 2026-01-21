# Middlebury Alumni Outreach System

## Quick Start (Read This First)

This project automates cold email outreach to Middlebury alumni. **Read this file completely before doing anything.**

### The Complete Workflow

1. **User uploads contacts** (CSV with name, company, role - emails optional)
2. **Claude confirms and finds emails** using `email_finder.py`
3. **Claude shows results** with confidence levels (HIGH/MEDIUM/LOW)
4. **User approves contacts** to proceed with
5. **Claude writes personalized inserts** (15-25 words each)
6. **Claude adds contacts to Google Sheet** with inserts
7. **Claude creates drafts** via `email_drafter.py --create-drafts`
8. **User reviews & sends** from Outlook Drafts folder
9. **User tells Claude which were sent** → Claude updates sheet

---

## Branch-Based Workflow

**Main = source of truth** for docs, code, and template. Feature branches have their own campaign-specific settings.

### Branch Structure

```
main                              ← Source of truth (docs, code, template)
├── round-1-middlebury-alumni     ← Own config: subject, availability, contacts
├── round-2-middlebury-alumni     ← Own config: subject, availability, contacts
└── round-2-tech-entrepreneur-contacts ← Own config: subject, availability, contacts
```

### Starting a New Campaign

When starting a new outreach round, user provides **3 required inputs**:

| Input | Example | Stored In |
|-------|---------|-----------|
| **Subject line** | "Middlebury Freshman - Hungry to Learn" | `outlook_config.json` |
| **Availability** | Tuesday 10am-1pm, Wed 1:30-4pm, Fri 9am-3pm | `outlook_config.json` |
| **Contacts** | CSV or list | Google Sheet |

```bash
# Create new branch from main
git checkout main && git pull
git checkout -b round-3-new-contacts

# Set campaign-specific config
python3 email_drafter.py --set-subject "Your Subject Line"
python3 email_drafter.py --set-availability \
  --window1 "Tuesday 10am-1pm EST" \
  --window2 "Wednesday 1:30-4pm EST" \
  --window3 "Friday 9am-3pm EST"
```

### Key Principle: No Branch Merging

- **Main stays clean** - only docs, code, template updates
- **Feature branches stay separate** - each has its own config
- **Reference main for workflow** - when in doubt, check main's CLAUDE.md
- **Don't merge branches** - they have different configs that will conflict

### Progress Tracking (Resume Without Repeating Work)

Each branch tracks progress in its CSV and Google Sheet. When resuming a campaign:

**CSV columns to track:**
| Column | Values | Purpose |
|--------|--------|---------|
| `Email` | address or blank | Skip email finding if already found |
| `Email Status` | blank → `drafted` → `sent` | Skip drafting if already drafted |
| `Email Confidence` | HIGH/MEDIUM/LOW | Know which emails are verified |

**Resuming a campaign:**
```bash
git checkout round-1-middlebury-alumni

# Check current progress
# - Contacts with Email Status = blank → need drafts
# - Contacts with Email Status = drafted → ready to send
# - Contacts with Email Status = sent → done

# Only creates drafts for contacts where Email Status is blank
python3 email_drafter.py --create-drafts
```

**What gets skipped automatically:**
- `email_finder.py` → skips rows that already have an Email
- `email_drafter.py --create-drafts` → skips rows with Email Status = "drafted" or "sent"
- Google Sheet stays in sync with CSV via the drafting process

**Commit progress to branch:**
```bash
git add contacts.csv
git commit -m "Updated 5 contacts to drafted status"
```

### Switching Campaigns

```bash
# Switch to existing campaign
git checkout round-1-middlebury-alumni

# Config already has that campaign's subject + availability
# CSV already has progress (who's drafted, who's sent)
python3 email_drafter.py --create-drafts  # only processes remaining contacts
```

---

## Phase 1: Finding Emails

### Input Format

User provides:
- **Contacts**: CSV or list with Name, Company, Title/Role
- **Availability Windows**: 3 time slots for the week (e.g., "Tuesday 10am-1pm EST")

Contact CSV fields:
- Name (required)
- Company (required)
- Title/Role (optional but helpful)
- LinkedIn URL (optional but helpful)
- Email (optional - if missing, we'll find it)

### Running the Email Finder

```bash
# Set your Hunter.io API key (free tier: 25 searches/month)
export HUNTER_API_KEY='your_key_here'

# Run email finder
python3 email_finder.py -i contacts.csv -o results.csv

# Test with first 10 contacts
python3 email_finder.py -i contacts.csv -o results.csv --limit 10

# With SMTP verification (slower but more accurate)
python3 email_finder.py -i contacts.csv -o results.csv --verify
```

### API Keys (Optional - More Sources)

| API | Free Tier | Env Variable |
|-----|-----------|--------------|
| Hunter.io | 25/month | `HUNTER_API_KEY` |
| Apollo.io | 50/month | `APOLLO_API_KEY` |
| RocketReach | 5/month | `ROCKETREACH_API_KEY` |
| Clearbit | Limited | `CLEARBIT_API_KEY` |

### Understanding Results

The finder returns confidence levels:

| Confidence | Source | What It Means |
|------------|--------|---------------|
| **HIGH** | Hunter verified, Apollo, RocketReach | Safe to use - verified email |
| **MEDIUM** | Google scrape, GitHub, partial match | Likely correct - test with one email first |
| **LOW** | Pattern guess | Generated from common formats - verify before bulk use |

### Email Pattern Generation

When APIs don't find emails, the script generates 8 pattern guesses:
1. `first.last@company.com`
2. `firstlast@company.com`
3. `flast@company.com`
4. `first_last@company.com`
5. `first@company.com`
6. `last.first@company.com`
7. `f.last@company.com`
8. `firstl@company.com`

**Recommendation:** Use HIGH confidence emails first. Test MEDIUM with one email. Use LOW/patterns only for high-value contacts worth the risk of bounce.

---

## Phase 2: Personalized Inserts

### Writing Rules

**Hard rules:**
- 15-25 words exactly
- Must flow naturally after "...curious about the world."
- Sound like a real 20-year-old, not AI

**Good starters:**
- "Lately I've been..."
- "I've been trying to learn more about..."
- "As someone trying to build something myself..."
- "I've been thinking a lot about..."

**Banned (never use):**
- "I came across..." / "I noticed..."
- "Your remarkable/impressive/incredible..."
- "I would be honored..."
- "resonates with me" / "aligns with my interests"
- Em dashes (use "and" instead)
- Anything that sounds like LinkedIn

**Examples:**
```
Chris Hench - Amazon/Alexa, ML Scientist
Insert: "Lately I've been building voice agents and I'd love to pick your brain on what problems in conversational AI are actually worth solving."
Word count: 22

Dan Schulman - PayPal, CEO
Insert: "I've been thinking a lot about fintech and PayPal's push on financial inclusion stands out. I'm curious what made you bet on that."
Word count: 23
```

For full rules see `email_personalization_prompt.md`

---

## Phase 3: Creating Drafts

### Current Settings

**Subject line:** `Middlebury Freshman - Hungry to Learn`
**Sheet ID:** `1wX-FLA28wLFegn7pwBJvD3VKZkABMhC9VDGKbLzQXuE`

### Commands

```bash
# Set subject line (persists to config)
python3 email_drafter.py --set-subject "New Subject Here"

# Set availability windows (persists to config)
python3 email_drafter.py --set-availability \
  --window1 "Tuesday 10am-1pm EST" \
  --window2 "Wednesday 1:30-4pm EST" \
  --window3 "Friday 9am-3pm EST"

# Create drafts (uses saved subject + availability from config)
python3 email_drafter.py --create-drafts

# Override availability for one run (doesn't change config)
python3 email_drafter.py --create-drafts --window1 "Monday 9am" --window2 "Tuesday 10am" --window3 "Wednesday 11am"

# If session expires, USER runs this in their terminal:
python3 email_drafter.py --login
```

### The Email Template

```
Hello {first_name},

My name is Max Friedlander, I am 20 years old, and a current Freshman at
Middlebury. I am interested in entrepreneurship, ambitious, and curious
about the world. {personalized_insert}

I understand that you're very busy, but if you had 15 minutes to chat
with me, I would love to introduce myself, and learn from you.

I have a few windows open this week and the weeks ahead:
- {window1}
- {window2}
- {window3}

Feel free to let me know what works best.

Best,
Max
```

---

## Phase 4: Tracking Status

### Google Sheet Structure

| Column | Purpose |
|--------|---------|
| Name | Full name |
| Email | Email address |
| Company | Their company |
| Email Confidence | HIGH/MEDIUM/LOW |
| Personalized Insert | The custom sentence |
| Email Status | blank → "drafted" → "sent" |
| Draft Created | Auto-filled timestamp |
| Sent Date | Fill when user confirms sent |

### Adding Contacts to Sheet

```python
from email_drafter import load_config, get_google_sheet

config = load_config()
ws = get_google_sheet(config)

# Find next empty row
records = ws.get_all_records()
next_row = len(records) + 2

# Add contact
ws.update_cell(next_row, 1, "John Smith")
ws.update_cell(next_row, 2, "john@acme.com")
ws.update_cell(next_row, 3, "Acme Corp")

# Add personalized insert
headers = ws.row_values(1)
insert_col = headers.index("Personalized Insert") + 1
ws.update_cell(next_row, insert_col, "Your personalized insert here")
```

### Updating Sent Status

**User says:** "I sent the email to Marc Baghadjian" / "I sent all of them"

**Claude does:**
```python
from email_drafter import load_config, get_google_sheet
from datetime import datetime

config = load_config()
ws = get_google_sheet(config)

records = ws.get_all_records()
for i, row in enumerate(records, start=2):
    if "Marc Baghadjian" in row.get("Name", ""):
        headers = ws.row_values(1)
        status_col = headers.index("Email Status") + 1
        sent_col = headers.index("Sent Date") + 1
        ws.update_cell(i, status_col, "sent")
        ws.update_cell(i, sent_col, datetime.now().strftime("%Y-%m-%d"))
        print(f"Marked {row['Name']} as sent")
        break
```

---

## Example Full Session

**User:** Here are my contacts and availability:

Contacts:
```csv
Name,Company,Title
Marc Baghadjian,HyperCard,CEO
Sumanyu Sharma,Hamming,CEO
```

Availability:
- Tuesday 10am-1pm EST
- Wednesday 1:30-4pm EST
- Friday 9am-3pm EST

**Claude:**
1. "I'll search for emails. Running email finder..."
2. Runs: `python3 email_finder.py -i contacts.csv -o results.csv`
3. Reports results:
   ```
   Marc Baghadjian - marc@hypercard.com (HIGH confidence)
   Sumanyu Sharma - sumanyu@hamming.ai (HIGH confidence)
   ```
4. "Both have verified emails. Want me to write personalized inserts and create drafts with your availability?"

**User:** "Yes"

**Claude:**
1. Saves availability: `python3 email_drafter.py --set-availability --window1 "Tuesday 10am-1pm EST" --window2 "Wednesday 1:30-4pm EST" --window3 "Friday 9am-3pm EST"`
2. Writes personalized inserts for each
3. Adds them to Google Sheet
4. Runs `python3 email_drafter.py --create-drafts`
5. Reports: "Created 2 drafts in Outlook with your availability windows. Review them in your Drafts folder."

**User:** (reviews and sends from Outlook)

**User:** "I sent both"

**Claude:** Updates sheet status to "sent" for both contacts.

---

## Troubleshooting

**"Session expired" error:**
User runs in their terminal (not Claude):
```bash
python3 email_drafter.py --login
```
Then log into Middlebury Outlook and press Enter.

**No emails found / all LOW confidence:**
- Check company domain is correct
- Try adding LinkedIn URL to CSV
- Consider using pattern guesses for high-value contacts

**Contact needs changes after drafted:**
1. Clear their Email Status (make it blank)
2. Update their Personalized Insert
3. Delete old draft from Outlook manually
4. Run `--create-drafts` again

---

## Files Reference

| File | Purpose |
|------|---------|
| `email_finder.py` | Find emails from name/company |
| `email_drafter.py` | Create Outlook drafts |
| `email_personalization_prompt.md` | Full rules for writing inserts |
| `outlook_config.json` | Email template and settings |
| `credentials/google_sheets_key.json` | Google API credentials |
| `.playwright_session/` | Saved Outlook login |
| `results.csv` | Email finder output |
| `middlebury_contacts.csv` | Input contact list |

---

## About Max (For Writing Inserts)

- 20 years old, Middlebury freshman
- Runs a voice agent company
- Into AI, startups, finance, investing
- Wants to learn how people made big decisions
- The Middlebury connection is the hook

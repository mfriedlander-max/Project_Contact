# Middlebury Alumni Outreach System

## Quick Start (Read This First)

This project automates cold email outreach to Middlebury alumni. **Read this file completely before doing anything.**

### The Complete Workflow

**User provides:**
- Contacts (CSV with name, company, title - email optional)
- Subject line
- Availability windows (3 time slots)

**Steps:**
1. **Set subject + availability** via `email_drafter.py --set-subject` and `--set-availability`
2. **Run `email_finder.py`** to find emails (if not provided)
3. **Run `insert_generator.py`** to research + generate inserts (AUTOMATED)
4. **Run `email_drafter.py --create-drafts`** to create Outlook drafts
5. **User reviews drafts** (check LOW confidence inserts marked with "LOW - ")
6. **User sends from Outlook**
7. **Run `email_drafter.py --sync-sent`** to update tracking

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

**One Google Sheet, Multiple Campaigns:**
All campaigns share one Google Sheet. They're differentiated by the **Campaign** column, which is automatically set to the git branch name. Scripts filter by the current branch.

**CSV/Sheet columns:**
| Column | Set By | Purpose |
|--------|--------|---------|
| `Campaign` | insert_generator.py | Filter contacts by campaign (= branch name) |
| `Name` | Input CSV | Contact name |
| `Email` | email_finder.py | Found email address |
| `Email Confidence` | email_finder.py | HIGH/MEDIUM/LOW for email |
| `Company` | Input CSV | Company name |
| `Title` | Input CSV | Role/title |
| `Personalized Insert` | insert_generator.py | The 15-25 word insert |
| `Insert Confidence` | insert_generator.py | HIGH/MEDIUM/LOW for insert |
| `Sources` | insert_generator.py | Where facts came from |
| `Email Status` | email_drafter.py | blank → "drafted" → "sent" |
| `Draft Created` | email_drafter.py | Timestamp |
| `Sent Date` | --sync-sent | Date sent |

**Resuming a campaign:**
```bash
git checkout round-1-middlebury-alumni

# Check current progress
# - Contacts with Email Status = blank → need drafts
# - Contacts with Email Status = drafted → ready to send
# - Contacts with Email Status = sent → done

# Only creates drafts for contacts where Email Status is blank AND Campaign matches current branch
python3 email_drafter.py --create-drafts
```

**What gets skipped automatically:**
- `email_finder.py` → skips rows that already have an Email
- `insert_generator.py` → skips rows that already have Personalized Insert (by email match)
- `email_drafter.py --create-drafts` → skips rows where Email Status ≠ blank, AND filters by Campaign = current branch
- `email_drafter.py --sync-sent` → only checks contacts where Campaign = current branch AND Email Status = "drafted"

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

## Phase 2: Generating Inserts (Automated)

### Running the Insert Generator

```bash
# Set your Anthropic API key
export ANTHROPIC_API_KEY='your_key_here'

# Run insert generator (outputs to CSV + Google Sheet)
python3 insert_generator.py -i with_emails.csv -o with_inserts.csv

# Use different model
python3 insert_generator.py -i with_emails.csv -o with_inserts.csv --model haiku  # faster, cheaper
python3 insert_generator.py -i with_emails.csv -o with_inserts.csv --model opus   # best quality

# Slower rate limiting if hitting API limits
python3 insert_generator.py -i with_emails.csv -o with_inserts.csv --delay 2.0
```

### What It Does

1. Researches each contact using Claude API with web search
2. Generates a 15-25 word personalized insert following rules in `email_personalization_prompt.md`
3. Assigns confidence: HIGH (verified facts) / MEDIUM (single source) / LOW (generic fallback)
4. Outputs to CSV file + Google Sheet
5. Logs all actions to `insert_generator.log`

### Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| **HIGH** | Facts from 2+ sources | Use as-is |
| **MEDIUM** | Facts from 1 source | Quick review |
| **LOW** | Minimal info found | Must edit - marked with "LOW - " in draft |

### Checkpointing

If the script fails mid-run, re-run the same command. It automatically skips already-processed contacts (matches by email).

### Writing Rules Reference

**Hard rules:**
- 15-25 words exactly
- Must flow naturally after "...curious about the world."
- Sound like a real 20-year-old, not AI

**Banned (never use):**
- "I came across..." / "I noticed..."
- "Your remarkable/impressive/incredible..."
- "I would be honored..."
- "resonates with me" / "aligns with my interests"
- Em dashes (use "and" instead)

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
# Only processes contacts where Campaign = current branch
python3 email_drafter.py --create-drafts

# Override availability for one run (doesn't change config)
python3 email_drafter.py --create-drafts --window1 "Monday 9am" --window2 "Tuesday 10am" --window3 "Wednesday 11am"

# If session expires, USER runs this in their terminal:
python3 email_drafter.py --login
```

### LOW Confidence Inserts

When creating drafts, contacts with LOW confidence inserts will have "LOW - " prepended to their insert in the draft body:

> My name is Max Friedlander... curious about the world. LOW - I've been thinking a lot about fintech and would love to learn from your experience building Stripe.

**Edit these drafts before sending** to improve the personalization or remove the "LOW - " prefix.

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

### Check Campaign Status

**User says:** "What's the status?" / "Show me progress" / "How many drafted?"

**Claude runs:**
```python
from email_drafter import load_config, get_google_sheet

config = load_config()
ws = get_google_sheet(config)
records = ws.get_all_records()

# Count by status
blank = [r for r in records if not r.get("Email Status") and r.get("Email")]
drafted = [r for r in records if r.get("Email Status") == "drafted"]
sent = [r for r in records if r.get("Email Status") == "sent"]

print(f"📊 Campaign Status:")
print(f"   - Ready to draft: {len(blank)}")
print(f"   - Drafted (in Outlook): {len(drafted)}")
print(f"   - Sent: {len(sent)}")
print(f"   - Total: {len(records)}")

if drafted:
    print(f"\n📝 Drafted (waiting to send):")
    for r in drafted:
        print(f"   - {r.get('Name')} ({r.get('Email')})")
```

### Mark as Sent (Automated)

After sending emails from Outlook, run this to automatically update the Google Sheet:

```bash
python3 email_drafter.py --sync-sent
```

This scans your Outlook Sent folder and marks matching contacts as "sent" with today's date. Only checks contacts in the current campaign (branch).

### Mark as Sent (Manual)

**User says any of:**
- "I sent the email to Marc Baghadjian"
- "I sent Marc's email"
- "Sent: Marc Baghadjian, Sarah Johnson"
- "Mark Marc as sent"

**Claude updates the sheet:**
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
        print(f"✓ Marked {row['Name']} as sent")
        break
```

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

---

## Example Full Session

**User:** Here are my contacts: [uploads contacts.csv]
```csv
Name,Company,Title,Email
Marc Baghadjian,HyperCard,CEO,marc@hypercard.com
Sumanyu Sharma,Hamming,CEO,sumanyu@hamming.ai
```

Availability: Tue 10am-1pm, Wed 1:30-4pm, Fri 9am-3pm

**Steps:**

```bash
# 1. Set availability
python3 email_drafter.py --set-availability \
  --window1 "Tuesday 10am-1pm EST" \
  --window2 "Wednesday 1:30-4pm EST" \
  --window3 "Friday 9am-3pm EST"

# 2. Generate inserts (researches contacts + writes inserts)
python3 insert_generator.py -i contacts.csv -o with_inserts.csv

# 3. Create drafts in Outlook
python3 email_drafter.py --create-drafts
```

**User:** (reviews drafts in Outlook, edits any LOW confidence ones, sends)

```bash
# 4. Sync sent status
python3 email_drafter.py --sync-sent
```

**Output:**
```
Campaign: main
Connecting to Google Sheet...
Checking 2 drafted contacts...
Connected to Outlook Sent folder.
  Marked as sent: marc@hypercard.com
  Marked as sent: sumanyu@hamming.ai
Done! Found 2 sent emails.
```

---

## Troubleshooting

**"ANTHROPIC_API_KEY not set" error:**
```bash
export ANTHROPIC_API_KEY='your_key_here'
```

**insert_generator.py rate limited:**
```bash
# Use slower rate limiting
python3 insert_generator.py -i input.csv -o output.csv --delay 2.0
```

**Want to regenerate an insert:**
1. Delete that row from output CSV
2. Re-run insert_generator.py (it will regenerate just that contact)

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
| `insert_generator.py` | Research + generate personalized inserts |
| `email_drafter.py` | Create Outlook drafts, sync sent status |
| `email_personalization_prompt.md` | Full rules for writing inserts |
| `outlook_config.json` | Email template and settings |
| `credentials/google_sheets_key.json` | Google API credentials |
| `.playwright_session/` | Saved Outlook login |
| `insert_generator.log` | Log of insert generation actions |
| `results.csv` | Email finder output |
| `with_inserts.csv` | Insert generator output |

---

## About Max (For Writing Inserts)

- 20 years old, Middlebury freshman
- Runs a voice agent company
- Into AI, startups, finance, investing
- Wants to learn how people made big decisions
- The Middlebury connection is the hook

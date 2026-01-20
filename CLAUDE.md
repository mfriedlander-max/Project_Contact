# Middlebury Alumni Outreach System

## Quick Start (Read This First)

This project automates cold email outreach to Middlebury alumni. **Read this file completely before doing anything.**

### The Workflow

1. **User gives contacts** (name, company, role, email)
2. **You write personalized inserts** (15-25 words each, following rules below)
3. **You add contacts to Google Sheet** with their inserts
4. **You run `python3 email_drafter.py --create-drafts`** to create drafts in Outlook
5. **User reviews & sends** from Outlook Drafts folder
6. **User tells you which they sent** and you update the sheet manually

---

## Current Settings

**Subject line:** `Middlebury Freshman - Hungry to Learn`
**Sheet ID:** `1wX-FLA28wLFegn7pwBJvD3VKZkABMhC9VDGKbLzQXuE`

---

## Commands

```bash
# Create drafts from Google Sheet (main command)
python3 email_drafter.py --create-drafts

# Change subject line
python3 email_drafter.py --set-subject "New Subject Here"

# If session expires, USER must run this in their terminal (not Claude):
python3 email_drafter.py --login
```

---

## Adding Contacts to Google Sheet

Use Python to add contacts:

```python
from email_drafter import load_config, get_google_sheet

config = load_config()
ws = get_google_sheet(config)

# Find next empty row
records = ws.get_all_records()
next_row = len(records) + 2

# Add contact (columns: Name=1, Email=2, Company=3)
ws.update_cell(next_row, 1, "John Smith")
ws.update_cell(next_row, 2, "john@acme.com")
ws.update_cell(next_row, 3, "Acme Corp")

# Find Personalized Insert column and add insert
headers = ws.row_values(1)
insert_col = headers.index("Personalized Insert") + 1
ws.update_cell(next_row, insert_col, "Your personalized insert here")
```

---

## The Email Template

```
Hello {first_name},

My name is Max Friedlander, I am 20 years old, and a current Freshman at
Middlebury. I am interested in entrepreneurship, ambitious, and curious
about the world. {personalized_insert}

I understand that you're very busy, but if you had 15 minutes to chat
with me, I would love to introduce myself, and learn from you.

Best,
Max
```

---

## Writing Personalized Inserts

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

## Google Sheet Structure

| Column | Purpose |
|--------|---------|
| Name | Full name |
| Email | Email address |
| Company | Their company |
| Personalized Insert | The custom sentence (you write this) |
| Email Status | blank = needs draft, "drafted" = in Outlook, "sent" = user sent it |
| Draft Created | Auto-filled timestamp |
| Sent Date | Fill when user confirms sent |

**Important:** The script only drafts contacts where Email Status is blank.

---

## Updating Sent Status

**What user says:**
- "I sent the email to Marc Baghadjian"
- "I sent all of them"
- "Mark John Smith as sent"

**What you do:**
1. Look up the contact's row number in the sheet
2. Update their Email Status to "sent" and add today's date

```python
from email_drafter import load_config, get_google_sheet
from datetime import datetime

config = load_config()
ws = get_google_sheet(config)

# First, find the contact by name
records = ws.get_all_records()
for i, row in enumerate(records, start=2):
    if "Marc Baghadjian" in row.get("Name", ""):  # Change name as needed
        headers = ws.row_values(1)
        status_col = headers.index("Email Status") + 1
        sent_col = headers.index("Sent Date") + 1
        ws.update_cell(i, status_col, "sent")
        ws.update_cell(i, sent_col, datetime.now().strftime("%Y-%m-%d"))
        print(f"Marked {row['Name']} as sent")
        break
```

---

## Troubleshooting

**"Session expired" error:**
User needs to run in their terminal (not through Claude):
```bash
python3 email_drafter.py --login
```
Then log into Middlebury Outlook and press Enter.

**Contact already drafted but needs changes:**
1. Clear their Email Status in the sheet (make it blank)
2. Update their Personalized Insert
3. Delete the old draft from Outlook manually
4. Run `--create-drafts` again

---

## Files

| File | Purpose |
|------|---------|
| `email_drafter.py` | Main automation script |
| `outlook_config.json` | Email template and settings |
| `email_personalization_prompt.md` | Full rules for writing inserts |
| `credentials/google_sheets_key.json` | Google API credentials |
| `.playwright_session/` | Saved Outlook login |

---

## Example Session

**User:** Here are my contacts:
```
Marc Baghadjian | HyperCard | CEO | marc@hypercard.com
Sumanyu Sharma | Hamming | CEO | sumanyu@hamming.ai
```

**Claude:**
1. Writes personalized inserts for each
2. Adds them to Google Sheet with inserts
3. Runs `python3 email_drafter.py --create-drafts`
4. Reports: "Created 2 drafts. Check your Outlook Drafts folder."

**User:** (reviews drafts in Outlook, sends them)

**User:** "I sent both"

**Claude:** Updates sheet status to "sent" for both contacts.

---

## About Max (For Writing Inserts)

- 20 years old, Middlebury freshman
- Runs a voice agent company
- Into AI, startups, finance, investing
- Wants to learn how people made big decisions
- The Middlebury connection is the hook

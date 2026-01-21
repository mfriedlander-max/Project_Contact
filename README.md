# Middlebury Alumni Outreach System

Automated cold email outreach to Middlebury alumni. Find emails, write personalized messages, create Outlook drafts, and track who you've contacted.

## How It Works

```
1. You provide contacts (name, company, title)
2. System finds their email addresses
3. Claude writes personalized one-liners for each
4. System creates drafts in your Outlook
5. You review and send
6. System tracks who's been contacted
```

## Quick Start

### First Time Setup

```bash
# Install dependencies
pip install -r requirements.txt
playwright install chromium

# Set up API keys for email finding (optional but recommended)
export HUNTER_API_KEY='your_key'  # https://hunter.io - 25 free/month

# Login to Outlook (saves your session)
python3 email_drafter.py --login
```

### Running a Campaign

```bash
# 1. Switch to your campaign branch (or create new one)
git checkout round-2-middlebury-alumni

# 2. Check current progress
# (Claude will show you who's drafted, sent, remaining)

# 3. Create drafts for remaining contacts
python3 email_drafter.py --create-drafts

# 4. Review drafts in Outlook, send the ones you like

# 5. Tell Claude who you sent to - it updates the tracker
```

## Campaign Branches

Each outreach campaign lives in its own branch with its own settings:

| Branch | Contacts | Template |
|--------|----------|----------|
| `round-1-middlebury-alumni` | 50 Middlebury alumni | Middlebury freshman |
| `round-2-middlebury-alumni` | 102 Middlebury alumni | Middlebury freshman |
| `round-2-tech-entrepreneur-contacts` | 104 tech founders | College freshman (no Middlebury mention) |

### Starting a New Campaign

```bash
# Branch from main
git checkout main && git pull
git checkout -b round-3-new-contacts

# Set your subject line
python3 email_drafter.py --set-subject "Your Subject Line Here"

# Set your availability windows
python3 email_drafter.py --set-availability \
  --window1 "Tuesday 10am-1pm EST" \
  --window2 "Wednesday 1:30-4pm EST" \
  --window3 "Friday 9am-3pm EST"
```

## The Email Template

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

The `{personalized_insert}` is a custom 15-25 word sentence written for each contact.

## Commands Reference

| Command | What it does |
|---------|-------------|
| `python3 email_drafter.py --login` | Save your Outlook login (run once) |
| `python3 email_drafter.py --create-drafts` | Create drafts for all pending contacts |
| `python3 email_drafter.py --set-subject "..."` | Change the email subject line |
| `python3 email_drafter.py --set-availability --window1 "..." --window2 "..." --window3 "..."` | Set your availability windows |
| `python3 email_finder.py -i contacts.csv -o results.csv` | Find emails for a list of contacts |

## Status Tracking

The Google Sheet tracks each contact's status:

| Status | Meaning |
|--------|---------|
| (blank) | Ready to draft |
| `drafted` | Draft created in Outlook |
| `sent` | You've sent the email |

When you tell Claude "I sent the email to John Smith", it updates the sheet automatically.

## Files

| File | Purpose |
|------|---------|
| `email_drafter.py` | Creates Outlook drafts, tracks status |
| `email_finder.py` | Finds email addresses |
| `outlook_config.json` | Campaign settings (subject, availability, template) |
| `CLAUDE.md` | Instructions for Claude (the AI) |
| `email_personalization_prompt.md` | Rules for writing personalized inserts |

## Tips

1. **Review drafts before sending** - The system creates drafts, not sent emails
2. **Update availability weekly** - Run `--set-availability` when your schedule changes
3. **One campaign at a time** - Switch branches to work on different contact lists
4. **Session expires** - If drafts fail, run `--login` again

## Finding Emails

```bash
# Basic usage
python3 email_finder.py -i contacts.csv -o results.csv

# With SMTP verification (slower but more accurate)
python3 email_finder.py -i contacts.csv -o results.csv --verify

# Test with first 10 contacts
python3 email_finder.py -i contacts.csv -o results.csv --limit 10
```

### Email Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| HIGH | Verified by API | Safe to use |
| MEDIUM | Found via search | Probably good, test one first |
| LOW | Pattern guess | May bounce, use carefully |

### API Keys (Optional)

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| Hunter.io | 25/month | https://hunter.io/users/sign_up |
| Apollo.io | 50/month | https://app.apollo.io/#/signup |

## Troubleshooting

**"Session expired" error**
```bash
python3 email_drafter.py --login
# Log into Middlebury Outlook, press Enter when done
```

**Drafts not appearing**
- Check you're logged into the right Outlook account
- Run `--login` again if needed

**Wrong availability in emails**
```bash
python3 email_drafter.py --set-availability \
  --window1 "Your new window 1" \
  --window2 "Your new window 2" \
  --window3 "Your new window 3"
```

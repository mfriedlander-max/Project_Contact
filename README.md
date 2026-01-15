# Middlebury Contacts Email Finder

A multi-source email finder that searches Hunter.io, Apollo.io, RocketReach, Clearbit, Google, and GitHub to find professional email addresses.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set your API keys (get free keys at the URLs below)
export HUNTER_API_KEY='your_key'      # https://hunter.io/api-keys (25 free/month)
export APOLLO_API_KEY='your_key'      # https://app.apollo.io (50 free/month)

# 3. Run the finder
python email_finder.py -i middlebury_contacts.csv -o results.csv
```

## Files Included

| File | Purpose |
|------|---------|
| `email_finder.py` | Main script - searches multiple sources for emails |
| `linkedin_scraper.py` | Browser automation for LinkedIn (requires Playwright) |
| `quick_start.py` | Interactive guided setup |
| `middlebury_contacts.csv` | Your contact list |
| `requirements.txt` | Python dependencies |
| `setup.sh` | Setup helper script |

## Data Sources

### API Sources (Best Results)
1. **Hunter.io** - Best for professional emails, pattern detection
2. **Apollo.io** - Massive B2B database, often has direct emails
3. **RocketReach** - Good for executives
4. **Clearbit** - Company/person enrichment

### Free Sources
5. **Google Search** - Scrapes publicly available emails
6. **GitHub** - Developer email addresses (for tech folks)
7. **Pattern Generation** - Guesses likely email formats

### Browser-Based (Advanced)
8. **LinkedIn Scraper** - Requires login, higher risk of account restrictions

## Getting API Keys

| Service | Free Tier | Sign Up |
|---------|-----------|---------|
| Hunter.io | 25 searches/mo | https://hunter.io/users/sign_up |
| Apollo.io | 50 credits/mo | https://app.apollo.io/#/signup |
| RocketReach | 5 lookups/mo | https://rocketreach.co/signup |
| Clearbit | Limited | https://dashboard.clearbit.com/signup |

## Usage Examples

```bash
# Basic usage
python email_finder.py -i middlebury_contacts.csv -o results.csv

# With SMTP verification (slower, more accurate)
python email_finder.py -i middlebury_contacts.csv -o results.csv --verify

# Process only first 10 contacts (for testing)
python email_finder.py -i middlebury_contacts.csv -o results.csv --limit 10

# Interactive mode
python quick_start.py
```

## Output Format

The results CSV includes:
- Original contact info
- Up to 3 emails found (sorted by confidence)
- Source of each email
- Confidence level (high/medium/low)
- All emails found (semicolon-separated)

## Confidence Levels

| Level | Meaning | Action |
|-------|---------|--------|
| High | Verified by API or found in public records | Safe to use |
| Medium | Found via search or partial match | Verify before important outreach |
| Low | Pattern guess based on company format | Test with low-stakes email first |

## LinkedIn Scraper (Advanced)

For LinkedIn scraping, you'll need:

```bash
# Install Playwright
pip install playwright
playwright install chromium

# Run with manual login
python linkedin_scraper.py -i middlebury_contacts.csv -o linkedin_results.csv
```

⚠️ **Warning**: LinkedIn actively blocks scraping. Use sparingly to avoid account restrictions.

## Priority Contacts for Max

Based on your voice agent work and Hamming AI internship, prioritize:

### Tier 1 - Directly Relevant
- Chris Hench (Amazon/Alexa ML/NLP)
- Nicole Fazio (Amazon Alexa PM)
- Jonathan Reiber (OpenAI Strategy)
- Rachel Kang / Jeremy Schreiner (OpenAI)

### Tier 2 - Tech/Startup
- Bill Maris (GV founder)
- George Arison (Shift founder)
- Bryan Goldberg (Bleacher Report founder)

### Tier 3 - High Profile
- Dan Schulman (PayPal)
- Ted Pick (Morgan Stanley)

## Tips for Outreach

1. **Lead with Middlebury connection** - Instant credibility
2. **Keep ask specific** - "15-minute call" or "one question about X"
3. **Reference their work** - Show you've done homework
4. **Offer value** - What can you give back?

## Legal Note

This tool is for professional networking and should be used responsibly. Always comply with:
- Company ToS for each data source
- CAN-SPAM and GDPR if sending marketing emails
- LinkedIn's terms of service

"""One-off: draft the end-of-spring-2026 update email to warm contacts on the In Touch tab.

Reuses the saved Outlook Playwright session. Does NOT touch the Google Sheet.

Inserts the body as proper HTML (real <ul><li> bullets) so Outlook renders
uniform spacing and real bullet points — avoiding the plain-text dash mangling
seen on the first run.
"""
import argparse
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
from email_drafter import load_config

SUBJECT = "Middlebury Update - Max"

EXCLUDE_NAMES = {"Curt Futch", "Brian Fox", "Alice Roberts", "Adam King"}

UPDATES = [
    "Won $5K at MiddChallenge with my co-founder for our AI tutoring platform for college STEM courses. We are potentially having pilots with professors as part of building it out.",
    "Interviewing with Entrepreneur First (EF), one of the most competitive talent investor programs in the world. Multiple rounds in so far, will update if I get in.",
    "Got really curious about AI research this semester. Did some work on gradient descent and gradient flow, and ended up loving a lot of the concepts in multivariable calculus and differential equations that related to ML.",
    "Been collaborating with SMBs through MotionTech on AI integration and automation work, contracts are reaching higher values of $8k+, and becoming more complex. Good learning experience working with clients on a more professional scale.",
    "Pitched to a VC firm and to the Middlebury president, and have been doing a lot of cold outreach to founders and investors, and have been meeting some really inspirational and interesting people. Way more knowledgeable and interested in entrepreneurship than I was even a semester ago.",
    "Heading to Buenos Aires next fall to study at UBA — excited to plug into the AI/ML research scene there if possible and immerse myself in Spanish.",
]


def build_html_body(first_name: str) -> str:
    update_lines = "".join(f"<div>{u}</div>" for u in UPDATES)
    return (
        f"<div>Hey {first_name},</div>"
        f"<div><br></div>"
        f"<div>Hope you're doing well! Wanted to send another update now that the semester is wrapping up:</div>"
        f"<div><br></div>"
        f"{update_lines}"
        f"<div>Looking forward to seeing where everything goes next. No need to reply, but happy to chat if anything comes to mind!</div>"
        f"<div><br></div>"
        f"<div>Best,</div>"
        f"<div>Max</div>"
    )


def collect_recipients(config):
    import gspread
    from google.oauth2.service_account import Credentials
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_file("credentials/google_sheets_key.json", scopes=scope)
    client = gspread.authorize(creds)
    sh = client.open_by_key(config["google_sheet_id"])
    ws = sh.worksheet("In Touch")
    rows = ws.get_all_values()
    headers = rows[0]
    out = []
    for r in rows[1:]:
        d = dict(zip(headers, r))
        name = d.get("Name", "").strip()
        email = d.get("Email", "").strip()
        if not name or not email or "@" not in email:
            continue
        if name in EXCLUDE_NAMES:
            continue
        out.append({"name": name, "first": name.split()[0], "email": email})
    return out


def draft_one(page, recipient, screenshot_path=None):
    page.locator('button:has-text("New mail")').first.click()
    page.wait_for_selector('div[aria-label="To"]', timeout=10000)
    page.wait_for_timeout(500)

    # To
    page.locator('div[aria-label="To"]').click()
    page.keyboard.type(recipient["email"])
    page.wait_for_timeout(300)

    # Subject
    subj = page.locator('input[placeholder="Add a subject"]')
    if subj.count() == 0:
        subj = page.locator('input[aria-label="Add a subject"]')
    subj.fill(SUBJECT)
    page.wait_for_timeout(300)

    # Body via execCommand('insertHTML') on the focused contenteditable
    body_field = page.locator('div[aria-label="Message body"]')
    body_field.click()
    page.wait_for_timeout(300)
    html = build_html_body(recipient["first"])
    page.evaluate(
        """(html) => {
            const body = document.querySelector('div[aria-label="Message body"]');
            body.focus();
            // Clear existing content first
            const range = document.createRange();
            range.selectNodeContents(body);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            document.execCommand('delete', false);
            // Insert our HTML
            document.execCommand('insertHTML', false, html);
        }""",
        html,
    )
    page.wait_for_timeout(800)

    if screenshot_path:
        page.screenshot(path=screenshot_path, full_page=False)

    # Save draft
    page.keyboard.press("Control+s")
    page.wait_for_timeout(2500)

    # Cycle through drafts to confirm save
    page.goto("https://outlook.office.com/mail/drafts")
    page.wait_for_timeout(2000)
    page.goto("https://outlook.office.com/mail/")
    page.wait_for_selector('button:has-text("New mail")', timeout=15000)


def _dismiss_overlays(page):
    """Best-effort: close any modal/onboarding dialog covering the page."""
    for _ in range(3):
        page.keyboard.press("Escape")
        page.wait_for_timeout(300)


def clear_existing_drafts(page, subject: str) -> int:
    """Delete any drafts in the Drafts folder whose subject matches `subject`."""
    page.goto("https://outlook.office.com/mail/drafts")
    page.wait_for_timeout(3000)
    _dismiss_overlays(page)
    deleted = 0
    while deleted < 50:
        rows = page.locator(f'div[role="option"]:has-text("{subject}")')
        if rows.count() == 0:
            break
        try:
            rows.first.click(timeout=8000)
        except Exception:
            _dismiss_overlays(page)
            try:
                rows.first.click(force=True, timeout=8000)
            except Exception as e:
                print(f"  (could not click draft row: {e})")
                break
        page.wait_for_timeout(800)
        page.keyboard.press("Delete")
        page.wait_for_timeout(1500)
        _dismiss_overlays(page)
        deleted += 1
    return deleted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Only draft for the first N recipients")
    parser.add_argument("--only", type=str, default=None, help="Comma-separated names to draft for (substring match)")
    parser.add_argument("--exclude", type=str, default=None, help="Comma-separated names to skip (substring match)")
    parser.add_argument("--screenshot", action="store_true", help="Save a screenshot of each compose window before saving")
    parser.add_argument("--clear-existing", action="store_true", help="Delete any existing drafts with the target subject before creating new ones")
    args = parser.parse_args()

    config = load_config()
    session_dir = Path(config["session_dir"])
    if not session_dir.exists():
        print("ERROR: no session. Run `python3 email_drafter.py --login` first.")
        sys.exit(1)

    recipients = collect_recipients(config)

    if args.only:
        wanted = [s.strip().lower() for s in args.only.split(",")]
        recipients = [r for r in recipients if any(w in r["name"].lower() for w in wanted)]

    if args.exclude:
        skip = [s.strip().lower() for s in args.exclude.split(",")]
        recipients = [r for r in recipients if not any(s in r["name"].lower() for s in skip)]

    if args.limit:
        recipients = recipients[: args.limit]

    print(f"Recipients ({len(recipients)}):")
    for r in recipients:
        print(f"  - {r['name']} <{r['email']}>")
    print()

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=str(session_dir),
            headless=True,
            viewport={"width": 1280, "height": 800},
            slow_mo=100,
        )
        page = browser.pages[0] if browser.pages else browser.new_page()
        page.set_default_timeout(30000)

        print("Loading Outlook...")
        page.goto("https://outlook.office.com/mail/")
        try:
            page.wait_for_selector('button:has-text("New mail")', timeout=30000)
        except Exception:
            if "login" in page.url.lower() or "signin" in page.url.lower():
                print("ERROR: session expired. Re-run --login.")
                browser.close()
                sys.exit(1)
            print(f"ERROR: couldn't load Outlook. URL={page.url}")
            browser.close()
            sys.exit(1)
        print("Connected to Outlook.\n")

        if args.clear_existing:
            print(f"Clearing existing drafts with subject '{SUBJECT}'...")
            n = clear_existing_drafts(page, SUBJECT)
            print(f"Deleted {n} existing draft(s).\n")
            page.goto("https://outlook.office.com/mail/")
            page.wait_for_selector('button:has-text("New mail")', timeout=15000)

        ok, fail = [], []
        for i, r in enumerate(recipients, 1):
            print(f"[{i}/{len(recipients)}] {r['name']} <{r['email']}> ...", flush=True)
            shot = f".draft_preview_{i:02d}_{r['first'].lower()}.png" if args.screenshot else None
            try:
                draft_one(page, r, screenshot_path=shot)
                if shot:
                    print(f"   drafted (screenshot: {shot})")
                else:
                    print(f"   drafted")
                ok.append(r["name"])
            except Exception as e:
                print(f"   FAILED: {e}")
                fail.append((r["name"], str(e)))
                try:
                    page.goto("https://outlook.office.com/mail/")
                    page.wait_for_selector('button:has-text("New mail")', timeout=15000)
                except Exception:
                    pass

        browser.close()

    print()
    print(f"Done. Drafted: {len(ok)}/{len(recipients)}")
    if fail:
        print("Failures:")
        for n, e in fail:
            print(f"  - {n}: {e}")


if __name__ == "__main__":
    main()

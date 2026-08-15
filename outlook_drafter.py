"""Create Outlook drafts headlessly, using the saved browser profile.

This is deliberately the only script left in the project. Research and judgment
live in the skills; this does one mechanical thing: put text into a draft.

It reuses the Chromium profile in .playwright_session/ that was authenticated by
hand. No token, no API key - just cookies. When they expire, re-run --login once
with a visible window and log in.

    ./.venv/bin/python outlook_drafter.py --check
    ./.venv/bin/python outlook_drafter.py --create daily/2026-08-13/drafts.json
    ./.venv/bin/python outlook_drafter.py --login          # visible, to re-auth

drafts.json is a list of {"to", "subject", "body"} objects.

NEVER sends. There is no send path in this file, on purpose.
"""
import argparse
import json
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

ROOT = Path(__file__).resolve().parent
SESSION = ROOT / ".playwright_session"
MAILBOX = "https://outlook.office.com/mail/"


def open_context(p, headless=True):
    if not SESSION.exists():
        sys.exit("ERROR: %s does not exist. Run --login first." % SESSION)
    return p.chromium.launch_persistent_context(
        user_data_dir=str(SESSION),
        headless=headless,
        args=["--disable-blink-features=AutomationControlled"],
    )


def signed_in(page):
    """The New mail button only renders for an authenticated mailbox."""
    page.goto(MAILBOX, wait_until="domcontentloaded")
    try:
        page.wait_for_selector('button:has-text("New mail")', timeout=45000)
        return True
    except PWTimeout:
        return False


def cmd_check(args):
    with sync_playwright() as p:
        ctx = open_context(p, headless=not args.headed)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        ok = signed_in(page)
        if ok:
            print("SESSION VALID - the saved profile is still authenticated.")
            print("url: %s" % page.url)
        else:
            print("SESSION DEAD - not signed in.")
            print("url: %s" % page.url)
            print("Re-authenticate with: ./.venv/bin/python outlook_drafter.py --login")
        ctx.close()
        return 0 if ok else 1


def cmd_login(args):
    """Visible window so a human can sign in once; cookies persist afterwards.

    Polls for the mailbox instead of waiting on stdin, so it works when launched
    by an agent that cannot press Enter.
    """
    minutes = args.wait
    with sync_playwright() as p:
        ctx = open_context(p, headless=False)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(MAILBOX)
        print("A browser window is open. Sign in to Middlebury Outlook.")
        print("Waiting up to %d minutes for the inbox to load. No need to press anything." % minutes)

        deadline = minutes * 60
        waited = 0
        while waited < deadline:
            try:
                page.wait_for_selector('button:has-text("New mail")', timeout=10000)
                print("\nSIGNED IN. Session saved to %s" % SESSION.name)
                print("Drafting can now run headless. Re-run --login when cookies next expire.")
                ctx.close()
                return 0
            except PWTimeout:
                waited += 10
                if waited % 30 == 0:
                    print("  still waiting... (%ds)" % waited)
        print("\nTimed out after %d minutes without a signed-in mailbox." % minutes)
        ctx.close()
        return 1


def create_draft(page, to, subject, body):
    """One draft. Closing the compose window is what makes Outlook save it."""
    page.goto(MAILBOX, wait_until="domcontentloaded")
    page.wait_for_selector('button:has-text("New mail")', timeout=45000)
    page.click('button:has-text("New mail")')

    page.wait_for_selector('div[aria-label="To"]', timeout=20000)
    page.click('div[aria-label="To"]')
    page.keyboard.type(to)
    page.keyboard.press("Escape")          # dismiss the contact autocomplete

    # Outlook moved "Add a subject" from aria-label to placeholder; match either.
    subject_field = page.locator(
        'input[aria-label="Subject"], input[placeholder="Add a subject"], '
        'input[aria-label="Add a subject"]'
    ).first
    subject_field.click()
    subject_field.fill(subject)

    body_field = page.locator('div[aria-label="Message body"]')
    body_field.click()
    # Type line by line: a raw \n in Outlook's editor can submit rather than break.
    for i, line in enumerate(body.split("\n")):
        if i:
            page.keyboard.press("Enter")
        if line:
            page.keyboard.type(line)

    # Ctrl/Cmd+S saves to Drafts without sending, then close the composer.
    page.keyboard.press("Meta+s")
    page.wait_for_timeout(1500)
    page.goto(MAILBOX, wait_until="domcontentloaded")
    page.wait_for_timeout(1000)


def cmd_create(args):
    path = Path(args.create)
    if not path.exists():
        sys.exit("ERROR: no such file: %s" % path)
    drafts = json.loads(path.read_text())
    if not isinstance(drafts, list):
        sys.exit("ERROR: %s must contain a JSON list" % path)

    for i, d in enumerate(drafts, 1):
        missing = [k for k in ("to", "subject", "body") if not d.get(k)]
        if missing:
            sys.exit("ERROR: draft %d is missing %s" % (i, ", ".join(missing)))
        if "@" not in d["to"]:
            sys.exit("ERROR: draft %d has no real address: %r" % (i, d["to"]))

    with sync_playwright() as p:
        ctx = open_context(p, headless=not args.headed)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if not signed_in(page):
            ctx.close()
            sys.exit("SESSION DEAD - run --login first. No drafts created.")

        made, receipt = 0, []
        for d in drafts:
            try:
                create_draft(page, d["to"], d["subject"], d["body"])
                made += 1
                receipt.append({"to": d["to"], "subject": d["subject"], "created": True})
                print("  drafted: %-34s %s" % (d["to"], d["subject"]))
            except Exception as e:
                receipt.append({"to": d["to"], "subject": d["subject"],
                                "created": False, "error": str(e)[:200]})
                print("  FAILED:  %-34s %s" % (d["to"], str(e)[:90]))
        ctx.close()

        # A receipt written by this script, not by a model. A run cannot claim
        # drafts it did not create, which is exactly what run 4 did.
        out = path.parent / (path.stem + "-receipt.json")
        out.write_text(json.dumps(receipt, indent=1))
        print("\nreceipt: %s" % out)
        print("%d of %d drafts created. Nothing was sent." % (made, len(drafts)))
        return 0 if made == len(drafts) else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="is the saved session still valid?")
    ap.add_argument("--login", action="store_true", help="open a visible window to sign in")
    ap.add_argument("--create", metavar="JSON", help="create drafts from a JSON file")
    ap.add_argument("--headed", action="store_true", help="show the browser (debugging)")
    ap.add_argument("--wait", type=int, default=10, metavar="MIN",
                    help="how long --login waits for you to sign in (default 10 min)")
    args = ap.parse_args()

    if args.login:
        sys.exit(cmd_login(args))
    if args.check:
        sys.exit(cmd_check(args))
    if args.create:
        sys.exit(cmd_create(args))
    ap.print_help()


if __name__ == "__main__":
    main()

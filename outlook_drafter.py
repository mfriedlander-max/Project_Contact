"""Create Outlook drafts headlessly, using the saved browser profile.

This is deliberately the only script left in the project. Research and judgment
live in the skills; this does one mechanical thing: put text into a draft.

It reuses the Chromium profile in .playwright_session/ that was authenticated by
hand. No token, no API key - just cookies. When they expire, re-run --login once
with a visible window and log in.

    ./.venv/bin/python outlook_drafter.py --check
    ./.venv/bin/python outlook_drafter.py --create daily/2026-08-13/drafts.json
    ./.venv/bin/python outlook_drafter.py --delete daily/2026-08-13/drafts.json
    ./.venv/bin/python outlook_drafter.py --login          # visible, to re-auth

drafts.json is a list of {"to", "subject", "body"} objects.

--delete takes the same file, or a -receipt.json, and matches on subject plus
recipient. It is a DRY RUN unless you add --yes: it reports how many drafts each
target matches (MATCH x2 when a batch was drafted twice) and stops. With --yes it
sweeps the folder in rounds, deleting every match - duplicates included - until a
pass deletes nothing. It only ever looks inside Drafts, and deleted drafts go to
Deleted Items where they can be recovered.

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
DRAFTS = "https://outlook.office.com/mail/drafts/"


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


def open_drafts(page):
    """Go to Drafts and refuse to continue if we did not land there.

    Every delete below is scoped to this view. Deleting from a list that turned
    out to be the Inbox is the failure worth engineering against.
    """
    page.goto(DRAFTS, wait_until="domcontentloaded")
    page.wait_for_selector('button:has-text("New mail")', timeout=45000)
    page.wait_for_timeout(2000)          # the list renders after the chrome does
    if "/drafts" not in page.url.lower():
        raise RuntimeError("not in the Drafts folder, refusing to delete: %s" % page.url)


def draft_rows(page):
    """Message rows in the list. Outlook renders each one as role=option."""
    return page.locator('div[role="option"]')


def matches_any(text, targets):
    """True if this Drafts row matches any (subject, recipient) target.

    Pure function, so it is unit-testable without a browser. The subject must
    appear as a WHOLE line, so a shorter subject cannot match a longer one it
    prefixes ("Cold Called My Way Through College"). The recipient email must
    appear somewhere in the row text.

    Fail-safe by design: OWA renders a recipient that resolves to a contact as a
    display NAME rather than an email ("Capossela, Alessandra"). Such a row does
    not match by email and is deliberately left untouched rather than risk
    deleting the wrong draft. Those surface as "still matching" and are deleted
    by hand.
    """
    lines = [ln.strip() for ln in text.split("\n")]
    low = text.lower()
    for s, to in targets:
        if s and s.strip() in lines and (not to or to.lower() in low):
            return True
    return False


def collect_row_texts(page):
    """Scroll the whole virtualised Drafts list, return every unique row text.

    The list renders ~7 rows at a time, and a wheel event needs the cursor
    parked over the list or nothing scrolls. Used for dry-run reporting and the
    final "did anything survive" check - never to delete by index.
    """
    rows = draft_rows(page)
    if rows.count():
        box = rows.nth(0).bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.wheel(0, -40000)
    page.wait_for_timeout(600)
    seen = []
    empty = 0
    for _ in range(120):
        r = draft_rows(page)
        before = len(seen)
        for i in range(r.count()):
            try:
                t = r.nth(i).inner_text()
            except Exception:
                continue                  # row recycled mid-scan
            if t not in seen:
                seen.append(t)
        empty = 0 if len(seen) > before else empty + 1
        if empty >= 8:                    # scrolled a while, nothing new: bottom
            break
        page.mouse.wheel(0, 600)
        page.wait_for_timeout(300)
    return seen


def find_match_index(page, targets):
    """Index of the first currently-rendered row matching any target, or None."""
    rows = draft_rows(page)
    for i in range(rows.count()):
        try:
            t = rows.nth(i).inner_text()
        except Exception:
            continue
        if matches_any(t, targets):
            return i
    return None


def sweep_round(page, targets):
    """One top-to-bottom pass, deleting every rendered row that matches a target.

    Deletes the first match in view, lets the list settle, re-scans - so
    duplicates that share a subject AND recipient are all removed (the old code
    deleted at most one of each), and a click that misses is retried on the next
    round rather than lost. Returns how many it deleted this pass.
    """
    rows = draft_rows(page)
    if rows.count():
        box = rows.nth(0).bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] / 2, box["y"] + box["height"] / 2)
    page.mouse.wheel(0, -40000)
    page.wait_for_timeout(600)
    deleted = 0
    empty_scrolls = 0
    for _ in range(200):
        i = find_match_index(page, targets)
        if i is not None:
            page.keyboard.press("Escape")     # clear any modal left by a prior delete
            page.wait_for_timeout(300)
            try:
                delete_row(page, i)
                deleted += 1
            except Exception as e:
                print("  FAILED a delete: %s" % str(e)[:80])
            page.wait_for_timeout(500)
            empty_scrolls = 0
        else:
            page.mouse.wheel(0, 600)
            page.wait_for_timeout(350)
            empty_scrolls += 1
            if empty_scrolls >= 12:           # a full screen of scrolling, no match: bottom
                break
    return deleted


def delete_row(page, i):
    """Delete one row without opening it.

    Three paths were tried against the live mailbox. Clicking the row opens the
    composer, whose modal backdrop then swallows every later click. The row's
    hover toolbar offers only "Mark as unread" and "Flag". The right-click menu
    is the one that deletes a draft without opening it first.
    """
    row = draft_rows(page).nth(i)
    row.scroll_into_view_if_needed()
    # Let the virtualised list settle before reading geometry: scrolling moves
    # rows under the cursor, and right-clicking a stale point opens no menu.
    # Rows at the bottom of the list failed every time until this wait existed.
    page.wait_for_timeout(1000)
    box = row.bounding_box()
    if not box:
        raise RuntimeError("row has no bounding box, cannot right-click it")
    page.mouse.click(box["x"] + box["width"] / 2,
                     box["y"] + box["height"] / 2, button="right")
    page.wait_for_timeout(1200)
    # The menu label carries a leading icon glyph, so match on contained text
    # rather than an exact string.
    page.locator('[role="menuitem"]').filter(has_text="Delete").first.click(timeout=8000)
    page.wait_for_timeout(1200)

    # Deleting a DRAFT raises "Are you sure you want to discard this draft?".
    # Nothing is deleted until OK is clicked, and pressing Escape answers Cancel.
    # This dialog is the whole reason the first three attempts reported success
    # on some rows and silent failure on others.
    try:
        page.locator('[role="dialog"] button:has-text("OK")').first.click(timeout=6000)
    except PWTimeout:
        pass          # a non-draft folder deletes without asking
    page.wait_for_timeout(1200)


def cmd_delete(args):
    path = Path(args.delete)
    if not path.exists():
        sys.exit("ERROR: no such file: %s" % path)
    items = json.loads(path.read_text())
    if not isinstance(items, list) or not items:
        sys.exit("ERROR: %s must contain a non-empty JSON list" % path)

    targets = [(d.get("subject"), d.get("to")) for d in items]
    if not all(s for s, _ in targets):
        sys.exit("ERROR: every entry needs a subject. Nothing is matched by address alone.")

    with sync_playwright() as p:
        ctx = open_context(p, headless=not args.headed)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        if not signed_in(page):
            ctx.close()
            sys.exit("SESSION DEAD - run --login first. Nothing was deleted.")
        open_drafts(page)

        # Scan the whole folder once and report matches per target. A target can
        # match MORE than one draft when a batch was drafted twice, so the count
        # is shown - the old code deleted at most one of each and then reported
        # the surviving duplicate as a failure.
        texts = collect_row_texts(page)
        total = 0
        for s, to in targets:
            n = sum(1 for t in texts if matches_any(t, [(s, to)]))
            total += n
            print("  %-11s %-44s %s" % (("MATCH x%d" % n) if n else "no match", s, to or ""))
        print("\n%d draft(s) match across %d target(s), in a folder of %d." % (total, len(targets), len(texts)))

        if not args.yes:
            print("DRY RUN, nothing deleted. Re-run with --yes to delete the matches above.")
            ctx.close()
            return 0

        # Sweep the folder in rounds until a full pass deletes nothing. This
        # removes every matching row (duplicates included) and retries any click
        # that missed, instead of one fragile pass keyed on a per-row poll.
        deleted = 0
        for rnd in range(1, 9):
            d = sweep_round(page, targets)
            deleted += d
            print("  round %d: deleted %d" % (rnd, d))
            if d == 0:
                break

        remaining = sum(1 for t in collect_row_texts(page) if matches_any(t, targets))
        ctx.close()
        print("\n%d deleted. They are in Deleted Items and can be recovered." % deleted)
        if remaining:
            print("%d still match - likely recipients OWA shows as a name, not an email. "
                  "Delete those by hand." % remaining)
        return 0 if remaining == 0 else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="is the saved session still valid?")
    ap.add_argument("--login", action="store_true", help="open a visible window to sign in")
    ap.add_argument("--create", metavar="JSON", help="create drafts from a JSON file")
    ap.add_argument("--delete", metavar="JSON",
                    help="delete drafts matching the subjects in a JSON file (dry run without --yes)")
    ap.add_argument("--yes", action="store_true",
                    help="actually delete; without it --delete only reports what it matched")
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
    if args.delete:
        sys.exit(cmd_delete(args))
    ap.print_help()


if __name__ == "__main__":
    main()

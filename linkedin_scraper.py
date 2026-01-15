#!/usr/bin/env python3
"""
LinkedIn Contact Enricher
=========================
Uses Playwright for browser automation to extract additional contact info
from LinkedIn profiles.

IMPORTANT: LinkedIn actively blocks scraping. This script uses a real browser
session with your logged-in cookies to avoid detection.

Usage:
    1. First, run: playwright install chromium
    2. Log into LinkedIn in your regular browser
    3. Export your cookies using a browser extension
    4. Run: python linkedin_scraper.py --input contacts.csv --output enriched.csv

Note: Use responsibly - LinkedIn may suspend accounts for automated access.
"""

import csv
import json
import time
import random
import argparse
import os
from typing import Optional, Dict, List
from dataclasses import dataclass

try:
    from playwright.sync_api import sync_playwright, Page
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️  Playwright not installed. Run: pip install playwright && playwright install chromium")


@dataclass
class LinkedInProfile:
    name: str
    linkedin_url: str
    headline: str = ""
    location: str = ""
    email: str = ""
    phone: str = ""
    website: str = ""
    twitter: str = ""
    current_company: str = ""
    about: str = ""


class LinkedInScraper:
    def __init__(self, headless: bool = False):
        self.headless = headless
        self.browser = None
        self.page = None
        
    def __enter__(self):
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("Playwright not available")
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        self.page = self.context.new_page()
        return self
        
    def __exit__(self, *args):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
    
    def load_cookies(self, cookies_file: str):
        """Load cookies from a JSON file exported from browser."""
        with open(cookies_file, 'r') as f:
            cookies = json.load(f)
        self.context.add_cookies(cookies)
        print(f"✓ Loaded {len(cookies)} cookies")
        
    def login_manual(self):
        """Open LinkedIn login page for manual login."""
        print("🔐 Opening LinkedIn for manual login...")
        print("   Please log in, then press Enter when done.")
        self.page.goto('https://www.linkedin.com/login')
        input("Press Enter after logging in...")
        
    def is_logged_in(self) -> bool:
        """Check if we're logged into LinkedIn."""
        self.page.goto('https://www.linkedin.com/feed/')
        time.sleep(2)
        return 'feed' in self.page.url and 'login' not in self.page.url
    
    def random_delay(self, min_sec: float = 2, max_sec: float = 5):
        """Random delay to appear more human."""
        time.sleep(random.uniform(min_sec, max_sec))
        
    def scrape_profile(self, linkedin_url: str) -> Optional[LinkedInProfile]:
        """Scrape a LinkedIn profile for contact info."""
        if not linkedin_url or 'linkedin.com' not in linkedin_url:
            return None
            
        try:
            print(f"  Fetching: {linkedin_url}")
            self.page.goto(linkedin_url, wait_until='networkidle')
            self.random_delay(3, 6)
            
            profile = LinkedInProfile(
                name="",
                linkedin_url=linkedin_url
            )
            
            # Get name
            try:
                name_el = self.page.query_selector('h1.text-heading-xlarge')
                if name_el:
                    profile.name = name_el.inner_text().strip()
            except:
                pass
                
            # Get headline
            try:
                headline_el = self.page.query_selector('div.text-body-medium')
                if headline_el:
                    profile.headline = headline_el.inner_text().strip()
            except:
                pass
                
            # Get location
            try:
                location_el = self.page.query_selector('span.text-body-small.inline')
                if location_el:
                    profile.location = location_el.inner_text().strip()
            except:
                pass
            
            # Try to get contact info (requires clicking "Contact info")
            try:
                contact_link = self.page.query_selector('a[href*="contact-info"]')
                if contact_link:
                    contact_link.click()
                    self.random_delay(1, 2)
                    
                    # Look for email
                    email_section = self.page.query_selector('section.ci-email a')
                    if email_section:
                        profile.email = email_section.get_attribute('href', '').replace('mailto:', '')
                    
                    # Look for phone
                    phone_section = self.page.query_selector('section.ci-phone span')
                    if phone_section:
                        profile.phone = phone_section.inner_text().strip()
                    
                    # Look for website
                    website_section = self.page.query_selector('section.ci-websites a')
                    if website_section:
                        profile.website = website_section.get_attribute('href', '')
                    
                    # Look for Twitter
                    twitter_section = self.page.query_selector('section.ci-twitter a')
                    if twitter_section:
                        profile.twitter = twitter_section.get_attribute('href', '')
                    
                    # Close modal
                    close_btn = self.page.query_selector('button[aria-label="Dismiss"]')
                    if close_btn:
                        close_btn.click()
                        self.random_delay(0.5, 1)
            except Exception as e:
                print(f"    Could not get contact info: {e}")
                
            return profile
            
        except Exception as e:
            print(f"  Error scraping {linkedin_url}: {e}")
            return None


def load_contacts(filepath: str) -> List[Dict]:
    """Load contacts from CSV."""
    contacts = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Name'):
                contacts.append(dict(row))
    return contacts


def save_results(contacts: List[Dict], profiles: Dict[str, LinkedInProfile], filepath: str):
    """Save enriched contacts to CSV."""
    fieldnames = list(contacts[0].keys()) if contacts else []
    new_fields = ['LI_Email', 'LI_Phone', 'LI_Website', 'LI_Twitter', 'LI_Headline', 'LI_Location']
    fieldnames.extend([f for f in new_fields if f not in fieldnames])
    
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contact in contacts:
            linkedin_url = contact.get('LinkedIn URL', '')
            profile = profiles.get(linkedin_url)
            
            if profile:
                contact['LI_Email'] = profile.email
                contact['LI_Phone'] = profile.phone
                contact['LI_Website'] = profile.website
                contact['LI_Twitter'] = profile.twitter
                contact['LI_Headline'] = profile.headline
                contact['LI_Location'] = profile.location
                
            writer.writerow(contact)


def main():
    parser = argparse.ArgumentParser(description='LinkedIn profile scraper')
    parser.add_argument('--input', '-i', required=True, help='Input CSV with LinkedIn URLs')
    parser.add_argument('--output', '-o', default='linkedin_enriched.csv', help='Output CSV')
    parser.add_argument('--cookies', '-c', help='Cookies JSON file from browser')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    parser.add_argument('--limit', '-l', type=int, help='Limit number of profiles')
    args = parser.parse_args()
    
    if not PLAYWRIGHT_AVAILABLE:
        print("❌ Playwright is required. Install with:")
        print("   pip install playwright")
        print("   playwright install chromium")
        return
    
    # Load contacts
    print(f"📂 Loading contacts from: {args.input}")
    contacts = load_contacts(args.input)
    print(f"   Found {len(contacts)} contacts")
    
    if args.limit:
        contacts = contacts[:args.limit]
    
    profiles = {}
    
    with LinkedInScraper(headless=args.headless) as scraper:
        # Login
        if args.cookies and os.path.exists(args.cookies):
            scraper.load_cookies(args.cookies)
        
        if not scraper.is_logged_in():
            print("⚠️  Not logged into LinkedIn")
            scraper.login_manual()
            
            if not scraper.is_logged_in():
                print("❌ Failed to log in")
                return
        
        print("✓ Logged into LinkedIn")
        
        # Scrape profiles
        for i, contact in enumerate(contacts, 1):
            linkedin_url = contact.get('LinkedIn URL', '')
            print(f"\n[{i}/{len(contacts)}] {contact.get('Name', 'Unknown')}")
            
            if linkedin_url:
                profile = scraper.scrape_profile(linkedin_url)
                if profile:
                    profiles[linkedin_url] = profile
                    if profile.email:
                        print(f"    ✓ Found email: {profile.email}")
                        
            # Random longer delay between profiles
            if i < len(contacts):
                scraper.random_delay(5, 15)
    
    # Save results
    print(f"\n💾 Saving to: {args.output}")
    save_results(contacts, profiles, args.output)
    
    # Summary
    found = sum(1 for p in profiles.values() if p.email)
    print(f"\n📊 Summary:")
    print(f"   Profiles scraped: {len(profiles)}")
    print(f"   Emails found: {found}")


if __name__ == '__main__':
    main()

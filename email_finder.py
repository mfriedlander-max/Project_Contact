#!/usr/bin/env python3
"""
Multi-Source Contact Email Finder
=================================
Searches multiple sources to find email addresses for a list of contacts.

Sources:
1. Hunter.io API - Email pattern detection and verification
2. Apollo.io API - B2B contact database  
3. RocketReach API - Professional contact finder
4. Clearbit API - Company/person enrichment
5. Google Search scraping - Public email mentions
6. GitHub profile scraping - Developer emails
7. Personal website scraping - Contact pages
8. Common email pattern generation + SMTP verification

Usage:
    python email_finder.py --input contacts.csv --output results.csv

API Keys (set as environment variables):
    HUNTER_API_KEY - Get free key at https://hunter.io/api-keys
    APOLLO_API_KEY - Get free key at https://app.apollo.io/#/settings/api-keys  
    ROCKETREACH_API_KEY - Get at https://rocketreach.co/api
    CLEARBIT_API_KEY - Get at https://clearbit.com/
"""

import csv
import json
import os
import re
import time
import argparse
import smtplib
import dns.resolver
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from urllib.parse import quote_plus, urljoin
import requests
from bs4 import BeautifulSoup


@dataclass
class Contact:
    name: str
    company: str
    title: str = ""
    industry: str = ""
    linkedin_url: str = ""
    location: str = ""
    # Results
    emails_found: List[Dict] = field(default_factory=list)
    sources_checked: List[str] = field(default_factory=list)


@dataclass  
class EmailResult:
    email: str
    source: str
    confidence: str  # high, medium, low
    verified: bool = False


class EmailFinder:
    """Multi-source email finder with rate limiting and caching."""
    
    def __init__(self):
        self.hunter_key = os.getenv('HUNTER_API_KEY')
        self.apollo_key = os.getenv('APOLLO_API_KEY')
        self.rocketreach_key = os.getenv('ROCKETREACH_API_KEY')
        self.clearbit_key = os.getenv('CLEARBIT_API_KEY')
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Rate limiting
        self.last_request_time = {}
        self.rate_limits = {
            'hunter': 1.0,      # 1 second between requests
            'apollo': 0.5,
            'rocketreach': 1.0,
            'google': 2.0,      # Be nice to Google
            'github': 1.0,
            'generic': 0.5
        }
        
        # Cache
        self.cache = {}
        
    def _rate_limit(self, source: str):
        """Enforce rate limiting per source."""
        limit = self.rate_limits.get(source, 0.5)
        last_time = self.last_request_time.get(source, 0)
        elapsed = time.time() - last_time
        if elapsed < limit:
            time.sleep(limit - elapsed)
        self.last_request_time[source] = time.time()

    def _get_company_domain(self, company: str) -> Optional[str]:
        """Try to find the company's domain."""
        # Common patterns
        company_domains = {
            'google': 'google.com',
            'amazon': 'amazon.com',
            'microsoft': 'microsoft.com',
            'apple': 'apple.com',
            'openai': 'openai.com',
            'paypal': 'paypal.com',
            'morgan stanley': 'morganstanley.com',
            'goldman sachs': 'gs.com',
            'barclays': 'barclays.com',
            'google ventures': 'gv.com',
            'google cloud': 'google.com',
            'amazon web services': 'amazon.com',
            'alexa': 'amazon.com',
            'shift': 'shift.com',
            'moore capital': 'moorecap.com',
            'bechtel': 'bechtel.com',
            'fidelity': 'fidelity.com',
            'lazard': 'lazard.com',
            'simon & schuster': 'simonandschuster.com',
            'npr': 'npr.org',
            'new balance': 'newbalance.com',
            'bleacher report': 'bleacherreport.com',
            'bustle': 'bustle.com',
            'pinboard': 'pinboard.in',
            'tsai capital': 'tsaicapital.com',
        }
        
        company_lower = company.lower()
        for key, domain in company_domains.items():
            if key in company_lower:
                return domain
        
        # Try to guess domain
        clean = re.sub(r'[^a-z0-9]', '', company_lower)
        return f"{clean}.com"

    # ========== HUNTER.IO ==========
    def search_hunter(self, contact: Contact) -> List[EmailResult]:
        """Search Hunter.io for email."""
        if not self.hunter_key:
            print("  [Hunter] No API key set")
            return []
            
        results = []
        self._rate_limit('hunter')
        
        domain = self._get_company_domain(contact.company)
        first_name = contact.name.split()[0] if contact.name else ""
        last_name = contact.name.split()[-1] if contact.name and len(contact.name.split()) > 1 else ""
        
        # Try email finder endpoint
        try:
            url = "https://api.hunter.io/v2/email-finder"
            params = {
                'domain': domain,
                'first_name': first_name,
                'last_name': last_name,
                'api_key': self.hunter_key
            }
            resp = self.session.get(url, params=params, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                if data.get('data', {}).get('email'):
                    email = data['data']['email']
                    score = data['data'].get('score', 0)
                    confidence = 'high' if score > 80 else 'medium' if score > 50 else 'low'
                    results.append(EmailResult(
                        email=email,
                        source='hunter.io',
                        confidence=confidence
                    ))
                    print(f"  [Hunter] Found: {email} (score: {score})")
            elif resp.status_code == 401:
                print("  [Hunter] Invalid API key")
            elif resp.status_code == 429:
                print("  [Hunter] Rate limited")
            else:
                print(f"  [Hunter] No result (status: {resp.status_code})")
                
        except Exception as e:
            print(f"  [Hunter] Error: {e}")
            
        return results

    # ========== APOLLO.IO ==========
    def search_apollo(self, contact: Contact) -> List[EmailResult]:
        """Search Apollo.io for email."""
        if not self.apollo_key:
            print("  [Apollo] No API key set")
            return []
            
        results = []
        self._rate_limit('apollo')
        
        try:
            url = "https://api.apollo.io/v1/people/match"
            headers = {
                'Content-Type': 'application/json',
                'Cache-Control': 'no-cache'
            }
            payload = {
                'api_key': self.apollo_key,
                'name': contact.name,
                'organization_name': contact.company,
                'linkedin_url': contact.linkedin_url if contact.linkedin_url else None
            }
            
            resp = self.session.post(url, json=payload, headers=headers, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                person = data.get('person', {})
                email = person.get('email')
                if email:
                    results.append(EmailResult(
                        email=email,
                        source='apollo.io',
                        confidence='high'
                    ))
                    print(f"  [Apollo] Found: {email}")
            else:
                print(f"  [Apollo] No result (status: {resp.status_code})")
                
        except Exception as e:
            print(f"  [Apollo] Error: {e}")
            
        return results

    # ========== ROCKETREACH ==========
    def search_rocketreach(self, contact: Contact) -> List[EmailResult]:
        """Search RocketReach for email."""
        if not self.rocketreach_key:
            print("  [RocketReach] No API key set")
            return []
            
        results = []
        self._rate_limit('rocketreach')
        
        try:
            url = "https://api.rocketreach.co/api/v2/person/lookup"
            headers = {
                'Api-Key': self.rocketreach_key,
                'Content-Type': 'application/json'
            }
            params = {
                'name': contact.name,
                'current_employer': contact.company
            }
            
            if contact.linkedin_url:
                params['linkedin_url'] = contact.linkedin_url
                
            resp = self.session.get(url, headers=headers, params=params, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                emails = data.get('emails', [])
                for email_data in emails:
                    if isinstance(email_data, dict):
                        email = email_data.get('email')
                    else:
                        email = email_data
                    if email:
                        results.append(EmailResult(
                            email=email,
                            source='rocketreach',
                            confidence='high'
                        ))
                        print(f"  [RocketReach] Found: {email}")
            else:
                print(f"  [RocketReach] No result (status: {resp.status_code})")
                
        except Exception as e:
            print(f"  [RocketReach] Error: {e}")
            
        return results

    # ========== CLEARBIT ==========
    def search_clearbit(self, contact: Contact) -> List[EmailResult]:
        """Search Clearbit for email."""
        if not self.clearbit_key:
            print("  [Clearbit] No API key set")
            return []
            
        results = []
        self._rate_limit('generic')
        
        domain = self._get_company_domain(contact.company)
        
        try:
            url = f"https://prospector.clearbit.com/v1/people/find"
            params = {
                'domain': domain,
                'name': contact.name
            }
            headers = {
                'Authorization': f'Bearer {self.clearbit_key}'
            }
            
            resp = self.session.get(url, headers=headers, params=params, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                email = data.get('email')
                if email:
                    results.append(EmailResult(
                        email=email,
                        source='clearbit',
                        confidence='high'
                    ))
                    print(f"  [Clearbit] Found: {email}")
            else:
                print(f"  [Clearbit] No result (status: {resp.status_code})")
                
        except Exception as e:
            print(f"  [Clearbit] Error: {e}")
            
        return results

    # ========== GOOGLE SEARCH SCRAPING ==========
    def search_google(self, contact: Contact) -> List[EmailResult]:
        """Search Google for publicly available email addresses."""
        results = []
        self._rate_limit('google')
        
        queries = [
            f'"{contact.name}" email',
            f'"{contact.name}" {contact.company} email',
            f'"{contact.name}" contact',
        ]
        
        email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
        found_emails = set()
        
        for query in queries[:2]:  # Limit to 2 queries to avoid rate limits
            try:
                self._rate_limit('google')
                url = f"https://www.google.com/search?q={quote_plus(query)}"
                resp = self.session.get(url, timeout=10)
                
                if resp.status_code == 200:
                    # Extract emails from search results
                    emails = email_pattern.findall(resp.text)
                    for email in emails:
                        # Filter out common false positives
                        if not any(x in email.lower() for x in ['example.com', 'sentry.io', 'schema.org', 'w3.org']):
                            found_emails.add(email.lower())
                elif resp.status_code == 429:
                    print("  [Google] Rate limited, skipping")
                    break
                    
            except Exception as e:
                print(f"  [Google] Error: {e}")
                
        for email in found_emails:
            # Try to match with person's name
            name_parts = contact.name.lower().split()
            if any(part in email for part in name_parts):
                results.append(EmailResult(
                    email=email,
                    source='google_search',
                    confidence='medium'
                ))
                print(f"  [Google] Found: {email}")
                
        return results

    # ========== GITHUB PROFILE ==========
    def search_github(self, contact: Contact) -> List[EmailResult]:
        """Search GitHub for developer email (works for tech folks)."""
        results = []
        
        # Only try for tech companies
        tech_companies = ['google', 'amazon', 'microsoft', 'apple', 'openai', 'meta', 'facebook']
        if not any(tc in contact.company.lower() for tc in tech_companies):
            return results
            
        self._rate_limit('github')
        
        try:
            # Search GitHub users
            name_query = contact.name.replace(' ', '+')
            url = f"https://api.github.com/search/users?q={name_query}"
            resp = self.session.get(url, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                for user in data.get('items', [])[:3]:  # Check top 3 matches
                    username = user.get('login')
                    if username:
                        self._rate_limit('github')
                        user_url = f"https://api.github.com/users/{username}"
                        user_resp = self.session.get(user_url, timeout=10)
                        if user_resp.status_code == 200:
                            user_data = user_resp.json()
                            email = user_data.get('email')
                            if email:
                                results.append(EmailResult(
                                    email=email,
                                    source='github',
                                    confidence='medium'
                                ))
                                print(f"  [GitHub] Found: {email}")
                                
        except Exception as e:
            print(f"  [GitHub] Error: {e}")
            
        return results

    # ========== EMAIL PATTERN GENERATION ==========
    def generate_email_patterns(self, contact: Contact) -> List[EmailResult]:
        """Generate likely email patterns based on common corporate formats."""
        results = []
        
        domain = self._get_company_domain(contact.company)
        if not domain:
            return results
            
        name_parts = contact.name.lower().split()
        if len(name_parts) < 2:
            return results
            
        first = name_parts[0]
        last = name_parts[-1]
        first_initial = first[0] if first else ""
        last_initial = last[0] if last else ""
        
        # Common patterns
        patterns = [
            f"{first}.{last}@{domain}",           # john.doe@company.com
            f"{first}{last}@{domain}",            # johndoe@company.com
            f"{first_initial}{last}@{domain}",    # jdoe@company.com
            f"{first}_{last}@{domain}",           # john_doe@company.com
            f"{first}@{domain}",                  # john@company.com
            f"{last}.{first}@{domain}",           # doe.john@company.com
            f"{first_initial}.{last}@{domain}",   # j.doe@company.com
            f"{first}{last_initial}@{domain}",    # johnd@company.com
        ]
        
        for pattern in patterns:
            results.append(EmailResult(
                email=pattern,
                source='pattern_guess',
                confidence='low'
            ))
            
        print(f"  [Patterns] Generated {len(patterns)} possible emails")
        return results

    # ========== SMTP VERIFICATION ==========
    def verify_email_smtp(self, email: str) -> bool:
        """
        Verify email exists via SMTP (use sparingly, can be slow/blocked).
        This checks if the mail server accepts the address.
        """
        try:
            domain = email.split('@')[1]
            
            # Get MX record
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_host = str(mx_records[0].exchange)
            
            # Connect to SMTP server
            server = smtplib.SMTP(timeout=10)
            server.connect(mx_host)
            server.helo('verify.com')
            server.mail('verify@verify.com')
            code, _ = server.rcpt(email)
            server.quit()
            
            return code == 250
            
        except Exception:
            return False

    # ========== MAIN SEARCH ==========
    def find_email(self, contact: Contact, verify: bool = False) -> Contact:
        """Run all searches for a contact."""
        print(f"\n{'='*60}")
        print(f"Searching: {contact.name} @ {contact.company}")
        print('='*60)
        
        all_results = []
        
        # Run all searches
        all_results.extend(self.search_hunter(contact))
        all_results.extend(self.search_apollo(contact))
        all_results.extend(self.search_rocketreach(contact))
        all_results.extend(self.search_clearbit(contact))
        all_results.extend(self.search_google(contact))
        all_results.extend(self.search_github(contact))
        
        # If no results from APIs, generate patterns
        if not any(r.confidence in ['high', 'medium'] for r in all_results):
            all_results.extend(self.generate_email_patterns(contact))
        
        # Optional SMTP verification for top candidates
        if verify:
            print("  [SMTP] Verifying top candidates...")
            for result in all_results:
                if result.confidence in ['high', 'medium']:
                    result.verified = self.verify_email_smtp(result.email)
                    if result.verified:
                        print(f"  [SMTP] Verified: {result.email}")
        
        # Deduplicate and store results
        seen = set()
        for result in all_results:
            if result.email.lower() not in seen:
                seen.add(result.email.lower())
                contact.emails_found.append({
                    'email': result.email,
                    'source': result.source,
                    'confidence': result.confidence,
                    'verified': result.verified
                })
        
        return contact


def load_contacts_csv(filepath: str) -> List[Contact]:
    """Load contacts from CSV file."""
    contacts = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Name'):
                contacts.append(Contact(
                    name=row.get('Name', ''),
                    company=row.get('Company', ''),
                    title=row.get('Title / Role', ''),
                    industry=row.get('Industry', ''),
                    linkedin_url=row.get('LinkedIn URL', ''),
                    location=row.get('Location', '')
                ))
    
    return contacts


def save_results_csv(contacts: List[Contact], filepath: str):
    """Save results to CSV."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        fieldnames = [
            'Name', 'Company', 'Title', 'Industry', 'LinkedIn URL',
            'Email 1', 'Email 1 Source', 'Email 1 Confidence',
            'Email 2', 'Email 2 Source', 'Email 2 Confidence',
            'Email 3', 'Email 3 Source', 'Email 3 Confidence',
            'All Emails'
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for contact in contacts:
            row = {
                'Name': contact.name,
                'Company': contact.company,
                'Title': contact.title,
                'Industry': contact.industry,
                'LinkedIn URL': contact.linkedin_url,
                'All Emails': '; '.join([e['email'] for e in contact.emails_found])
            }
            
            # Add top 3 emails
            sorted_emails = sorted(
                contact.emails_found,
                key=lambda x: {'high': 0, 'medium': 1, 'low': 2}.get(x['confidence'], 3)
            )
            
            for i, email_data in enumerate(sorted_emails[:3], 1):
                row[f'Email {i}'] = email_data['email']
                row[f'Email {i} Source'] = email_data['source']
                row[f'Email {i} Confidence'] = email_data['confidence']
                
            writer.writerow(row)


def main():
    parser = argparse.ArgumentParser(description='Multi-source email finder')
    parser.add_argument('--input', '-i', required=True, help='Input CSV file with contacts')
    parser.add_argument('--output', '-o', default='email_results.csv', help='Output CSV file')
    parser.add_argument('--verify', '-v', action='store_true', help='Verify emails via SMTP')
    parser.add_argument('--limit', '-l', type=int, help='Limit number of contacts to process')
    args = parser.parse_args()
    
    # Check for API keys
    print("\n🔑 API Keys Status:")
    print(f"  Hunter.io:    {'✓ Set' if os.getenv('HUNTER_API_KEY') else '✗ Not set'}")
    print(f"  Apollo.io:    {'✓ Set' if os.getenv('APOLLO_API_KEY') else '✗ Not set'}")
    print(f"  RocketReach:  {'✓ Set' if os.getenv('ROCKETREACH_API_KEY') else '✗ Not set'}")
    print(f"  Clearbit:     {'✓ Set' if os.getenv('CLEARBIT_API_KEY') else '✗ Not set'}")
    print()
    
    # Load contacts
    print(f"📂 Loading contacts from: {args.input}")
    contacts = load_contacts_csv(args.input)
    print(f"   Found {len(contacts)} contacts")
    
    if args.limit:
        contacts = contacts[:args.limit]
        print(f"   Processing first {args.limit} contacts")
    
    # Search for emails
    finder = EmailFinder()
    
    for i, contact in enumerate(contacts, 1):
        print(f"\n[{i}/{len(contacts)}]", end="")
        contact = finder.find_email(contact, verify=args.verify)
    
    # Save results
    print(f"\n\n💾 Saving results to: {args.output}")
    save_results_csv(contacts, args.output)
    
    # Summary
    found_count = sum(1 for c in contacts if any(e['confidence'] in ['high', 'medium'] for e in c.emails_found))
    print(f"\n📊 Summary:")
    print(f"   Total contacts: {len(contacts)}")
    print(f"   Emails found (high/medium confidence): {found_count}")
    print(f"   Success rate: {found_count/len(contacts)*100:.1f}%")


if __name__ == '__main__':
    main()

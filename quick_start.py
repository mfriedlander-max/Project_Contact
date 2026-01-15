#!/usr/bin/env python3
"""
Quick Start - Middlebury Contacts Email Finder
===============================================
This is your one-stop script to find emails for your Middlebury contacts.

Run this in Claude Code or any environment with network access:
    python quick_start.py

It will guide you through the process.
"""

import os
import sys
import subprocess


def check_dependencies():
    """Check and install required packages."""
    print("📦 Checking dependencies...")
    packages = ['requests', 'beautifulsoup4', 'dnspython']
    
    for package in packages:
        try:
            __import__(package.replace('-', '_').split('4')[0])
        except ImportError:
            print(f"   Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
    
    print("   ✓ All dependencies installed\n")


def get_api_keys():
    """Prompt for API keys if not set."""
    keys = {
        'HUNTER_API_KEY': ('Hunter.io', 'https://hunter.io/api-keys'),
        'APOLLO_API_KEY': ('Apollo.io', 'https://app.apollo.io/#/settings/api-keys'),
    }
    
    print("🔑 API Keys Setup")
    print("=" * 50)
    print("For best results, you'll need at least one API key.")
    print("Both services have free tiers.\n")
    
    for env_var, (name, url) in keys.items():
        current = os.getenv(env_var)
        if current:
            print(f"✓ {name}: Set")
        else:
            print(f"✗ {name}: Not set")
            print(f"  Get your free key at: {url}")
            key = input(f"  Enter {name} API key (or press Enter to skip): ").strip()
            if key:
                os.environ[env_var] = key
                print(f"  ✓ {name} key set for this session")
    
    print()


def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║           Middlebury Contacts Email Finder                  ║
╚══════════════════════════════════════════════════════════════╝
""")
    
    # Check dependencies
    check_dependencies()
    
    # Get API keys
    get_api_keys()
    
    # Check for input file
    input_file = "middlebury_contacts.csv"
    if not os.path.exists(input_file):
        print(f"📂 Looking for contacts file...")
        print(f"   Please ensure '{input_file}' is in the current directory")
        print(f"   Or specify the path to your contacts CSV:")
        input_file = input("   Path to CSV (or Enter for default): ").strip() or input_file
    
    if not os.path.exists(input_file):
        print(f"\n❌ Could not find {input_file}")
        print("   Please copy your contacts CSV to this directory and try again.")
        return
    
    print(f"\n✓ Found contacts file: {input_file}")
    
    # Run the email finder
    output_file = "middlebury_emails_found.csv"
    print(f"\n🔍 Starting email search...")
    print(f"   Results will be saved to: {output_file}\n")
    
    # Import and run
    from email_finder import EmailFinder, load_contacts_csv, save_results_csv
    
    contacts = load_contacts_csv(input_file)
    print(f"   Loaded {len(contacts)} contacts\n")
    
    finder = EmailFinder()
    
    for i, contact in enumerate(contacts, 1):
        print(f"[{i}/{len(contacts)}]", end="")
        contact = finder.find_email(contact)
    
    save_results_csv(contacts, output_file)
    
    # Summary
    high_conf = sum(1 for c in contacts if any(e['confidence'] == 'high' for e in c.emails_found))
    med_conf = sum(1 for c in contacts if any(e['confidence'] == 'medium' for e in c.emails_found))
    
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                      COMPLETE!                               ║
╚══════════════════════════════════════════════════════════════╝

📊 Results Summary:
   Total contacts processed: {len(contacts)}
   High confidence emails:   {high_conf}
   Medium confidence emails: {med_conf}
   
💾 Results saved to: {output_file}

📝 Next Steps:
   1. Open {output_file} in Excel/Sheets
   2. Prioritize high-confidence emails
   3. For low-confidence (pattern guesses), verify before sending
   
💡 Tips:
   - LinkedIn InMail is often better for executives
   - Middlebury alumni network is your best warm intro path
   - Keep your ask specific and brief (15-min call, one question)
""")


if __name__ == '__main__':
    main()

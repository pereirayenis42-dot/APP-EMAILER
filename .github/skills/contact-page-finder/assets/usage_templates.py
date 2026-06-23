"""
Contact Page Finder - Usage Templates

Common scenarios for extracting contact information from websites.
Copy and adapt these templates to your use case.
"""

# ============================================================================
# TEMPLATE 1: Single Website Email Extraction
# ============================================================================

def template_single_website():
    """Extract emails from a single known website."""
    import sys
    sys.path.insert(0, '.github/skills/contact-page-finder/scripts')
    from extract_emails import extract_emails
    
    website = "https://example.com"
    emails = extract_emails(website)
    
    print(f"Found {len(emails)} emails:")
    for email in emails:
        print(f"  - {email}")
    
    return emails


# ============================================================================
# TEMPLATE 2: Batch Processing from CSV
# ============================================================================

def template_csv_batch():
    """Extract emails from a list of websites in a CSV file."""
    import csv
    import sys
    sys.path.insert(0, '.github/skills/contact-page-finder/scripts')
    from extract_emails import extract_emails_batch
    
    # Read URLs from CSV
    websites = []
    with open('websites.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            websites.append(row['website_url'])
    
    # Extract emails from all websites
    results = extract_emails_batch(websites)
    
    # Save results to CSV
    with open('contact_emails.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Website', 'Emails', 'Count'])
        for url, emails in results.items():
            writer.writerow([url, ', '.join(emails), len(emails)])
    
    print(f"Results saved to contact_emails.csv")


# ============================================================================
# TEMPLATE 3: Integration with APP-EMAILER Database
# ============================================================================

def template_app_emailer_integration():
    """Extract and store emails in APP-EMAILER database."""
    import sys
    sys.path.insert(0, '.')  # Assuming we're in APP-EMAILER root
    
    from agent import extract_emails, save_business, save_emails
    
    # Sample business data
    businesses = [
        {
            'name': 'Example Corp',
            'website': 'https://example.com',
            'phone': '(555) 123-4567',
            'address': '123 Main St, Houston, TX 77001',
            'location': 'Houston'
        },
        {
            'name': 'Tech Startup Inc',
            'website': 'https://techstartup.io',
            'phone': None,
            'address': '456 Tech Ave, Houston, TX 77002',
            'location': 'Houston'
        }
    ]
    
    # Extract and save
    for biz in businesses:
        print(f"Processing: {biz['name']}")
        
        # Extract emails
        emails = extract_emails(biz['website']) if biz['website'] else []
        
        # Save to database
        business_id = save_business(
            biz['name'],
            biz['website'],
            biz['phone'],
            biz['address'],
            biz['location']
        )
        
        if business_id and emails:
            save_emails(business_id, emails)
            print(f"  ✓ Saved {len(emails)} email(s)")
        else:
            print(f"  ⊘ No emails found")


# ============================================================================
# TEMPLATE 4: With Error Tracking and Logging
# ============================================================================

def template_with_logging():
    """Extract emails with comprehensive error handling and logging."""
    import sys
    import logging
    from datetime import datetime
    
    sys.path.insert(0, '.github/skills/contact-page-finder/scripts')
    from extract_emails import extract_emails
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(f'contact_finder_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
            logging.StreamHandler()
        ]
    )
    
    websites = [
        "https://example.com",
        "https://anothersite.com",
        "https://invalid-url-that-will-fail.com"
    ]
    
    results = {}
    for website in websites:
        try:
            logging.info(f"Extracting: {website}")
            emails = extract_emails(website)
            results[website] = emails
            logging.info(f"  Found {len(emails)} emails")
        except Exception as e:
            logging.error(f"  Failed: {e}")
            results[website] = []
    
    # Summary
    total_emails = sum(len(e) for e in results.values())
    logging.info(f"Summary: {total_emails} emails from {len(results)} websites")
    
    return results


# ============================================================================
# TEMPLATE 5: Deduplication and Enrichment
# ============================================================================

def template_with_deduplication():
    """Extract emails and deduplicate across multiple sources."""
    import sys
    sys.path.insert(0, '.github/skills/contact-page-finder/scripts')
    from extract_emails import extract_emails
    
    websites = [
        "https://example.com",
        "https://example.co.uk",  # Same company, different domain
        "https://subsidiary.example.com",
    ]
    
    # Extract all emails
    all_emails = {}
    for website in websites:
        emails = extract_emails(website)
        all_emails[website] = emails
    
    # Deduplicate across all websites
    unique_emails = set()
    for emails in all_emails.values():
        unique_emails.update(emails)
    
    print(f"Websites processed: {len(websites)}")
    print(f"Unique emails found: {len(unique_emails)}")
    
    # Group by domain
    email_domains = {}
    for email in unique_emails:
        domain = email.split('@')[1]
        if domain not in email_domains:
            email_domains[domain] = []
        email_domains[domain].append(email)
    
    print("\nEmails by domain:")
    for domain, emails in sorted(email_domains.items()):
        print(f"  {domain}: {len(emails)} email(s)")
    
    return unique_emails


# ============================================================================
# TEMPLATE 6: Scheduled Scraping (Daily/Weekly)
# ============================================================================

def template_scheduled_scraping():
    """Setup scheduled email extraction using APScheduler."""
    import sys
    import json
    from datetime import datetime
    from apscheduler.schedulers.background import BackgroundScheduler
    
    sys.path.insert(0, '.github/skills/contact-page-finder/scripts')
    from extract_emails import extract_emails_batch
    
    scheduler = BackgroundScheduler()
    
    def scraping_job():
        """Daily scraping task."""
        print(f"[{datetime.now()}] Starting scraping job...")
        
        websites = [
            "https://example.com",
            "https://site2.com",
            "https://site3.com",
        ]
        
        results = extract_emails_batch(websites)
        
        # Save to file with timestamp
        filename = f"scrape_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[{datetime.now()}] Scraping complete. Results saved to {filename}")
    
    # Schedule job to run daily at 2 AM
    scheduler.add_job(scraping_job, 'cron', hour=2, minute=0)
    
    scheduler.start()
    print("Scheduler started. Scraping will run daily at 2:00 AM")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            pass  # Keep scheduler running
    except KeyboardInterrupt:
        scheduler.shutdown()
        print("Scheduler stopped")


# ============================================================================
# TEMPLATE 7: Validation and Quality Checks
# ============================================================================

def template_with_validation():
    """Extract and validate emails for quality."""
    import sys
    import re
    
    sys.path.insert(0, '.github/skills/contact-page-finder/scripts')
    from extract_emails import extract_emails, validate_email
    
    website = "https://example.com"
    emails = extract_emails(website)
    
    print(f"Found {len(emails)} email(s)\n")
    
    # Categorize emails
    valid_emails = []
    spam_emails = []
    suspicious_emails = []
    
    for email in emails:
        # Check if email is valid format
        if not validate_email(email):
            suspicious_emails.append(email)
            continue
        
        # Check for common spam indicators
        spam_keywords = ['noreply', 'no-reply', 'donotreply', 'noemails', 'spam']
        if any(keyword in email.lower() for keyword in spam_keywords):
            spam_emails.append(email)
        else:
            valid_emails.append(email)
    
    print("✓ Valid business emails:")
    for email in valid_emails:
        print(f"  - {email}")
    
    print(f"\n⚠ Spam/auto-reply emails ({len(spam_emails)}):")
    for email in spam_emails:
        print(f"  - {email}")
    
    print(f"\n✗ Suspicious format ({len(suspicious_emails)}):")
    for email in suspicious_emails:
        print(f"  - {email}")
    
    return {
        'valid': valid_emails,
        'spam': spam_emails,
        'suspicious': suspicious_emails
    }


if __name__ == "__main__":
    print("Contact Page Finder - Usage Templates\n")
    print("Choose a template:")
    print("1. Single website")
    print("2. Batch CSV processing")
    print("3. APP-EMAILER integration")
    print("4. With logging")
    print("5. Deduplication")
    print("6. Scheduled scraping")
    print("7. Validation")
    
    choice = input("\nSelect template (1-7): ").strip()
    
    templates = {
        '1': template_single_website,
        '2': template_csv_batch,
        '3': template_app_emailer_integration,
        '4': template_with_logging,
        '5': template_with_deduplication,
        '6': template_scheduled_scraping,
        '7': template_with_validation,
    }
    
    if choice in templates:
        templates[choice]()
    else:
        print("Invalid selection")

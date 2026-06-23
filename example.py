"""
Example usage script for APP-EMAILER
This demonstrates the main features of the lead scraper.
"""

from agent import (
    init_database,
    search_places,
    extract_emails,
    save_business,
    save_emails,
    validate_email,
    get_all_leads,
    get_validated_leads,
    export_to_csv,
    export_to_json,
    export_to_excel
)


def main():
    """Main example workflow"""
    
    print("=" * 50)
    print("APP-EMAILER - Lead Scraper Example")
    print("=" * 50)
    
    # Step 1: Initialize database
    print("\n[1] Initializing database...")
    init_database()
    
    # Step 2: Search for a single business
    print("\n[2] Searching for businesses...")
    results = search_places("Audi repair shop Houston")
    print(f"Found {len(results)} results")
    
    if results:
        business = results[0]
        name = business.get("displayName", {}).get("text", "")
        website = business.get("websiteUri")
        phone = business.get("nationalPhoneNumber", "")
        address = business.get("formattedAddress", "")
        
        print(f"  Business: {name}")
        print(f"  Website: {website}")
        print(f"  Phone: {phone}")
        print(f"  Address: {address}")
        
        # Step 3: Extract emails
        print("\n[3] Extracting emails...")
        emails = extract_emails(website) if website else []
        print(f"  Found {len(emails)} email(s): {emails}")
        
        # Step 4: Save to database
        print("\n[4] Saving to database...")
        business_id = save_business(name, website, phone, address, "Houston")
        if business_id and emails:
            save_emails(business_id, emails)
            print(f"  ✓ Saved business and {len(emails)} email(s)")
        elif business_id:
            print(f"  ✓ Saved business (no emails found)")
    
    # Step 5: Retrieve leads
    print("\n[5] Retrieving all leads...")
    all_leads = get_all_leads("Houston")
    print(f"  Total leads in database: {len(all_leads)}")
    
    # Step 6: Export data
    print("\n[6] Exporting data...")
    try:
        export_to_csv("Houston")
        print("  ✓ Exported to CSV")
    except Exception as e:
        print(f"  ✗ CSV export failed: {e}")
    
    try:
        export_to_json("Houston")
        print("  ✓ Exported to JSON")
    except Exception as e:
        print(f"  ✗ JSON export failed: {e}")
    
    try:
        export_to_excel("Houston")
        print("  ✓ Exported to Excel")
    except Exception as e:
        print(f"  ✗ Excel export failed: {e}")
    
    print("\n" + "=" * 50)
    print("Example completed! Check your exports.")
    print("=" * 50)


if __name__ == "__main__":
    main()

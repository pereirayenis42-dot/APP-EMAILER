"""
Simple script to view all leads in the database
"""

from agent import get_all_leads, get_validated_leads
import sqlite3

def view_all_leads():
    """Display all leads in a readable format"""
    leads = get_all_leads("Houston")
    
    print("\n" + "="*100)
    print("ALL LEADS IN DATABASE")
    print("="*100 + "\n")
    
    for i, lead in enumerate(leads, 1):
        name, website, phone, address, emails, email_count = lead
        print(f"{i}. {name}")
        print(f"   Address: {address}")
        print(f"   Phone: {phone}")
        print(f"   Website: {website}")
        print(f"   Emails ({email_count}): {emails if emails else 'None found'}")
        print()
    
    print(f"Total leads: {len(leads)}")

def view_database_stats():
    """Show database statistics"""
    conn = sqlite3.connect("leads.db")
    cursor = conn.cursor()
    
    # Count businesses
    cursor.execute("SELECT COUNT(*) FROM businesses")
    business_count = cursor.fetchone()[0]
    
    # Count emails
    cursor.execute("SELECT COUNT(*) FROM emails")
    email_count = cursor.fetchone()[0]
    
    # Count businesses with emails
    cursor.execute("""
        SELECT COUNT(DISTINCT business_id) FROM emails
    """)
    businesses_with_emails = cursor.fetchone()[0]
    
    conn.close()
    
    print("\n" + "="*50)
    print("DATABASE STATISTICS")
    print("="*50)
    print(f"Total Businesses: {business_count}")
    print(f"Total Emails: {email_count}")
    print(f"Businesses with Emails: {businesses_with_emails}")
    print(f"Businesses without Emails: {business_count - businesses_with_emails}")
    print("="*50 + "\n")

if __name__ == "__main__":
    view_database_stats()
    view_all_leads()

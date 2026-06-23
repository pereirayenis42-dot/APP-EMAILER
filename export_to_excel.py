"""
Export leads database to Excel format
"""

import sqlite3
import pandas as pd
from datetime import datetime

def export_leads_to_excel(filename=None):
    """
    Export leads.db to an Excel file with two sheets:
    - Businesses: all business information with associated emails
    - Emails: all emails with their associated businesses
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"leads_export_{timestamp}.xlsx"
    
    conn = sqlite3.connect("leads.db")
    
    # Read businesses with aggregated emails
    businesses_df = pd.read_sql_query("""
        SELECT 
            b.id,
            b.business_name,
            b.website,
            b.phone,
            b.address,
            b.location,
            b.created_at,
            GROUP_CONCAT(e.email, '; ') as emails,
            COUNT(e.id) as email_count
        FROM businesses b
        LEFT JOIN emails e ON b.id = e.business_id
        GROUP BY b.id
        ORDER BY b.business_name
    """, conn)
    
    # Read emails table with business names joined
    emails_df = pd.read_sql_query("""
        SELECT 
            e.id,
            b.business_name,
            e.email,
            e.is_valid,
            e.added_at
        FROM emails e
        JOIN businesses b ON e.business_id = b.id
        ORDER BY b.business_name, e.email
    """, conn)
    
    conn.close()
    
    # Create Excel file with multiple sheets
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        businesses_df.to_excel(writer, sheet_name='Businesses', index=False)
        emails_df.to_excel(writer, sheet_name='Emails', index=False)
    
    print(f"✓ Export complete: {filename}")
    print(f"  - Businesses: {len(businesses_df)} records")
    print(f"  - Emails: {len(emails_df)} records")
    
    return filename

if __name__ == "__main__":
    export_leads_to_excel()

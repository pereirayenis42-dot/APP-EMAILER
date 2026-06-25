import requests
import pandas as pd
import re
import sqlite3
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime
from openpyxl import Workbook

API_KEY = "INSERT GOOGLE MAPS API KEY HERE"
DB_NAME = "leads.db"

# Optional: Email validation API (sign up at zerobounce.io for free tier)
EMAIL_VALIDATION_ENABLED = True
EMAIL_VALIDATION_API_KEY = "INSERT API KEY HERE"

BUSINESS_TYPES = [
    "Audi repair shop",
    "Audi specialist",
    "Audi service center",
    "European auto repair",
    "Collision center",
    "Luxury car repair",
    "Import auto repair",
]

CITIES = [
    "Houston",
    "Katy",
    "Sugar Land",
    "The Woodlands",
    "Spring",
    "Cypress",
    "Pearland",
    "Missouri City",
    "League City",
    "Conroe",
    "Baytown",
    "Pasadena",
    "Friendswood",
    "Humble",
    "Tomball",
    "Galveston",
    "La Porte",
    "Deer Park",
    "Seabrook",
    "Stafford",
    "Bellaire",
    "Richmond",
    "Clear Lake",
    "Alvin",
    "Webster",
    "Rosenberg",
    "Montgomery",
    "Porter",
    "Cleveland",
    "Tomball",
    "Fresno",
    "Manvel",
    "Magnolia",
    "Bammel",
    "Rosharon",
    "Shenandoah",
]

SEARCH_TERMS = [
    f"{business} {city}"
    for business in BUSINESS_TYPES
    for city in CITIES
]

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# ==================== DATABASE SETUP ====================
def init_database():
    """Initialize SQLite database with schema"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_name TEXT NOT NULL,
            website TEXT,
            phone TEXT,
            address TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(business_name, address)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            email TEXT NOT NULL,
            is_valid BOOLEAN DEFAULT NULL,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (business_id) REFERENCES businesses(id),
            UNIQUE(email, business_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def business_exists(name, address):
    """Check if business already exists (duplicate detection)"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM businesses WHERE business_name = ? AND address = ?",
        (name, address)
    )
    result = cursor.fetchone()
    conn.close()
    return result is not None

def save_business(name, website, phone, address, location):
    """Save business to database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO businesses (business_name, website, phone, address, location)
            VALUES (?, ?, ?, ?, ?)
        """, (name, website, phone, address, location))
        conn.commit()
        business_id = cursor.lastrowid
        conn.close()
        return business_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def save_emails(business_id, emails):
    """Save emails for a business"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    for email in emails:
        try:
            cursor.execute("""
                INSERT INTO emails (business_id, email)
                VALUES (?, ?)
            """, (business_id, email))
        except sqlite3.IntegrityError:
            pass  # Email already exists
    conn.commit()
    conn.close()

def validate_email(email):
    """Validate email using ZeroBounce API (optional)"""
    if not EMAIL_VALIDATION_ENABLED or not EMAIL_VALIDATION_API_KEY:
        return None
    
    try:
        url = "https://api.zerobounce.net/v2/validate"
        params = {
            "email": email,
            "api_key": EMAIL_VALIDATION_API_KEY
        }
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            is_valid = data.get("status") == "valid"
            
            # Update database
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE emails SET is_valid = ? WHERE email = ?",
                (is_valid, email)
            )
            conn.commit()
            conn.close()
            return is_valid
    except Exception as e:
        print(f"Email validation error for {email}: {e}")
    
    return None


def test_zerobounce_api(sample_email="test@example.com"):
    """
    Quick test to verify ZeroBounce API is reachable and returning a response.

    Returns True when a valid response with a 'status' field is received,
    False otherwise.
    """
    if not EMAIL_VALIDATION_ENABLED or not EMAIL_VALIDATION_API_KEY:
        print("ZeroBounce validation is disabled or API key missing.")
        return False

    try:
        url = "https://api.zerobounce.net/v2/validate"
        params = {"email": sample_email, "api_key": EMAIL_VALIDATION_API_KEY}
        resp = requests.get(url, params=params, timeout=10)
        print(f"ZeroBounce HTTP status: {resp.status_code}")

        if resp.status_code != 200:
            print("ZeroBounce request failed:", resp.text)
            return False

        data = resp.json()
        # Print summary
        print("ZeroBounce response keys:", list(data.keys()))
        if 'status' in data:
            print("ZeroBounce appears to be working. Status:", data.get('status'))
            return True
        else:
            print("ZeroBounce response missing 'status' field.")
            return False
    except Exception as e:
        print("ZeroBounce test error:", e)
        return False

# ==================== SCRAPING FUNCTIONS ====================

def search_places(query):
    url = "https://places.googleapis.com/v1/places:searchText"

    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask":
            "places.displayName,"
            "places.websiteUri,"
            "places.formattedAddress,"
            "places.nationalPhoneNumber"
    }

    payload = {
        "textQuery": query
    }

    r = requests.post(url, json=payload, headers=headers)

    if r.status_code != 200:
        print(f"API Error: {r.text}")
        return []

    return r.json().get("places", [])

def extract_emails(url):
    try:
        r = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        emails = set(re.findall(EMAIL_REGEX, r.text))

        soup = BeautifulSoup(r.text, "html.parser")

        for link in soup.find_all("a", href=True):
            href = link["href"]

            if "contact" in href.lower():
                contact_url = urljoin(url, href)

                try:
                    c = requests.get(
                        contact_url,
                        timeout=10,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )

                    emails.update(
                        re.findall(EMAIL_REGEX, c.text)
                    )

                except:
                    pass

        return list(emails)

    except:
        return []

# ==================== MAIN EXECUTION ====================
init_database()

for term in SEARCH_TERMS:

    print(f"Searching: {term}")

    businesses = search_places(term)

    for business in businesses:

        name = business.get("displayName", {}).get("text", "")

        website = business.get("websiteUri")

        phone = business.get("nationalPhoneNumber", "")

        address = business.get("formattedAddress", "")

        # Check for duplicates
        if business_exists(name, address):
            print(f"  ⊘ Skipping duplicate: {name}")
            continue

        emails = []

        if website:
            emails = extract_emails(website)

        # Save to database
        business_id = save_business(name, website, phone, address, "Houston")
        
        if business_id:
            if emails:
                save_emails(business_id, emails)
            print(f"  ✓ Saved: {name} ({len(emails)} emails)")

print("\nDone! Results saved to database.")

# ==================== EXPORT FUNCTIONS ====================

def export_to_csv(location="Houston"):
    """Export leads from database to CSV"""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT b.business_name, b.website, b.phone, b.address, 
               GROUP_CONCAT(e.email, ', ') as emails
        FROM businesses b
        LEFT JOIN emails e ON b.id = e.business_id
        WHERE b.location = ?
        GROUP BY b.id
    """
    df = pd.read_sql_query(query, conn, params=(location,))
    conn.close()
    
    filename = f"{location.lower().replace(' ', '_')}_leads.csv"
    df.to_csv(filename, index=False)
    print(f"Exported to {filename}")

def export_to_json(location="Houston"):
    """Export leads from database to JSON"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT b.id, b.business_name, b.website, b.phone, b.address, 
               GROUP_CONCAT(e.email, ', ') as emails
        FROM businesses b
        LEFT JOIN emails e ON b.id = e.business_id
        WHERE b.location = ?
        GROUP BY b.id
    """, (location,))
    
    rows = cursor.fetchall()
    conn.close()
    
    data = [
        {
            "business_name": row[1],
            "website": row[2],
            "phone": row[3],
            "address": row[4],
            "emails": row[5].split(", ") if row[5] else []
        }
        for row in rows
    ]
    
    filename = f"{location.lower().replace(' ', '_')}_leads.json"
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Exported to {filename}")

def export_to_excel(location="Houston"):
    """Export leads from database to Excel"""
    conn = sqlite3.connect(DB_NAME)
    query = """
        SELECT b.business_name, b.website, b.phone, b.address, 
               GROUP_CONCAT(e.email, ', ') as emails
        FROM businesses b
        LEFT JOIN emails e ON b.id = e.business_id
        WHERE b.location = ?
        GROUP BY b.id
    """
    df = pd.read_sql_query(query, conn, params=(location,))
    conn.close()
    
    filename = f"{location.lower().replace(' ', '_')}_leads.xlsx"
    df.to_excel(filename, index=False)
    print(f"Exported to {filename}")

def get_all_leads(location="Houston"):
    """Retrieve all leads from database"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.business_name, b.website, b.phone, b.address, 
               GROUP_CONCAT(e.email, ', ') as emails, COUNT(e.id) as email_count
        FROM businesses b
        LEFT JOIN emails e ON b.id = e.business_id
        WHERE b.location = ?
        GROUP BY b.id
        ORDER BY b.created_at DESC
    """, (location,))
    
    results = cursor.fetchall()
    conn.close()
    return results

def get_validated_leads(location="Houston"):
    """Retrieve only validated email leads"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT b.business_name, b.website, b.phone, b.address, 
               GROUP_CONCAT(e.email, ', ') as emails, COUNT(e.id) as email_count
        FROM businesses b
        LEFT JOIN emails e ON b.id = e.business_id
        WHERE b.location = ? AND (e.is_valid = 1 OR e.is_valid IS NULL)
        GROUP BY b.id
        ORDER BY b.created_at DESC
    """, (location,))
    
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    init_database()
    
    # Uncomment to export:
    # export_to_csv("Houston")
    # export_to_json("Houston")
    # export_to_excel("Houston")

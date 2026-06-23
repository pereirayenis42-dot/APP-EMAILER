# APP-EMAILER

A Python-based lead scraper for finding and extracting contact information from businesses. Currently configured to find Audi repair shops and related automotive service centers in specific locations.

## Features

✅ **Database Storage** - Uses SQLite for persistent lead storage instead of CSV files
✅ **Duplicate Detection** - Automatically prevents duplicate businesses from being saved
✅ **Multiple Export Formats** - Export leads to CSV, JSON, or Excel
✅ **Location-Based Search** - Query different cities and regions
✅ **Email Extraction** - Automatically scrapes websites to extract email addresses
✅ **Email Validation** - Optional integration with ZeroBounce for email verification
✅ **Contact Information** - Captures phone numbers, addresses, and website URLs

## Tech Stack

- **Python 3.x**
- **SQLite3** - Database
- **Pandas** - Data manipulation and export
- **Requests** - HTTP requests
- **BeautifulSoup4** - Web scraping
- **OpenPyXL** - Excel export
- **Google Places API** - Business discovery

## Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd APP-EMAILER
```

2. Install dependencies:
```bash
pip install requests pandas beautifulsoup4 openpyxl
```

3. Set up your Google Places API key in `agent.py`:
```python
API_KEY = "your_api_key_here"
```

4. (Optional) Set up email validation with ZeroBounce:
   - Sign up at [zerobounce.io](https://www.zerobounce.io/)
   - Get your API key and add to `agent.py`:
```python
EMAIL_VALIDATION_ENABLED = True
EMAIL_VALIDATION_API_KEY = "your_zerobounce_api_key"
```

## Usage

### Basic Run

Initialize the database and run the scraper:
```python
python agent.py
```

This will:
- Create a SQLite database (`leads.db`)
- Search for all terms in `SEARCH_TERMS`
- Extract emails from business websites
- Store results in the database

### Export Data

Uncomment the export functions in `agent.py` to export:

```python
# CSV Export
export_to_csv("Houston")

# JSON Export
export_to_json("Houston")

# Excel Export
export_to_excel("Houston")
```

### Retrieve Leads Programmatically

```python
from agent import init_database, get_all_leads, get_validated_leads

init_database()

# Get all leads
leads = get_all_leads("Houston")

# Get only validated leads
validated_leads = get_validated_leads("Houston")

for lead in validated_leads:
    name, website, phone, address, emails, count = lead
    print(f"{name}: {emails}")
```

## Database Schema

### businesses table
- `id` - Primary key
- `business_name` - Name of the business
- `website` - Website URL
- `phone` - Phone number
- `address` - Physical address
- `location` - City/region (e.g., "Houston")
- `created_at` - Timestamp

### emails table
- `id` - Primary key
- `business_id` - Foreign key to businesses
- `email` - Email address
- `is_valid` - Email validation status (for future use)
- `added_at` - Timestamp

## Search Terms

Currently configured for Audi repair shops in Houston:
- Audi repair shop Houston
- European auto repair shop Houston
- German auto repair shop Houston
- Volkswagen repair shop Houston
- BMW repair shop Houston
- Mercedes repair shop Houston
- Collision center Houston

To customize, edit the `SEARCH_TERMS` list in `agent.py`.

## Roadmap

- [x] Database storage with SQLite
- [x] Duplicate detection
- [x] Multiple location support
- [x] CSV, JSON, Excel export
- [x] Email validation integration (optional)
- [ ] Phone number normalization
- [ ] Contact enrichment (LinkedIn, social media)
- [ ] Web dashboard for viewing leads
- [ ] REST API endpoints
- [ ] Automated scheduling (APScheduler)
- [ ] Email campaign integration (Mailchimp, SendGrid)
- [ ] Multi-source scraping (Yelp, Yellow Pages)

## Important Notes

- ⚠️ Respect `robots.txt` and terms of service when scraping
- ⚠️ Use appropriate rate limiting
- ⚠️ Ensure you have a valid Google Places API key with billing enabled

## License

MIT
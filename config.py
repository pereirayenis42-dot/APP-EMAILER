# Configuration for APP-EMAILER
# Edit these values according to your needs

# Google Places API
GOOGLE_PLACES_API_KEY = "your_api_key_here"

# Email Validation (ZeroBounce)
EMAIL_VALIDATION_ENABLED = False
ZEROBOUNCE_API_KEY = "your_zerobounce_api_key_here"

# Search Configuration
DEFAULT_LOCATION = "Houston"

# Search terms for finding businesses
SEARCH_TERMS = [
    "Audi repair shop Houston",
    "European auto repair shop Houston",
    "German auto repair shop Houston",
    "Volkswagen repair shop Houston",
    "BMW repair shop Houston",
    "Mercedes repair shop Houston",
    "Collision center Houston"
]

# Database
DATABASE_FILE = "leads.db"

# Export Settings
EXPORT_FORMATS = ["csv", "json", "excel"]  # Formats to use when exporting

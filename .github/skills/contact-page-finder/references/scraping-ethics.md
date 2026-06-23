# Web Scraping Best Practices

## Ethical Considerations

### Respect robots.txt
Always check a website's `robots.txt` file before scraping:
```
# Check at: https://example.com/robots.txt
User-agent: *
Disallow: /private/
```

If the site disallows scraping, respect it or contact the site owner for permission.

### Check Terms of Service
Many websites prohibit automated scraping in their ToS. Verify you have permission before scraping.

### Rate Limiting
Don't hammer servers with rapid requests:

```python
import time
from requests import Session

session = Session()

for url in urls:
    response = session.get(url)
    time.sleep(1)  # Wait 1 second between requests
```

## Technical Best Practices

### Use Appropriate Headers
```python
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}
response = requests.get(url, headers=headers, timeout=10)
```

### Implement Error Handling
```python
try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
except requests.Timeout:
    print(f"Timeout: {url}")
except requests.HTTPError as e:
    print(f"HTTP Error: {e}")
except requests.RequestException as e:
    print(f"Request failed: {e}")
```

### Cache Results
Avoid re-scraping the same page:
```python
import json

def save_cache(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_cache(filename):
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
```

## Email Extraction Specifics

### Common Email Patterns
```python
# Standard emails
contact@example.com
info@example.com
support@example.com
sales@example.com
help@example.com

# Department emails
engineering@example.com
hr@example.com
accounting@example.com
```

### Where to Look
1. **Contact pages** - Usually linked from navigation
2. **Footer** - Often contains support/contact emails
3. **About pages** - Team member emails
4. **Job listings** - HR/recruitment emails
5. **Privacy policy** - Data protection officer email

### What NOT to Trust
- Emails in JavaScript (dynamic content)
- Emails in images (obfuscated from scrapers)
- Honeypot/trap emails (designed to catch bots)
- Bulk email list footers (often inaccurate)

## Advanced Techniques

### Use Rotating User-Agents
```python
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)...",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15)...",
    "Mozilla/5.0 (X11; Linux x86_64)...",
]
random_agent = random.choice(user_agents)
```

### Handle JavaScript-Rendered Content
For sites that load content dynamically:
```python
# Use Selenium for browser automation
from selenium import webdriver

driver = webdriver.Chrome()
driver.get(url)
content = driver.page_source
# Now parse with BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')
```

### Session Management
```python
from requests import Session

session = Session()
session.headers.update({
    "User-Agent": "...",
    "Accept": "text/html",
})

# Session maintains cookies, connection pooling
response = session.get(url)
```

## Data Privacy

### GDPR Compliance (EU)
- Don't scrape personal email addresses for unsolicited marketing
- Provide opt-out mechanisms
- Store scraped data securely

### CCPA Compliance (California)
- Disclose data collection practices
- Allow users to request/delete their data
- Don't sell personal information without consent

## Debugging Tips

### Check HTTP Status Codes
```python
response = requests.get(url)
print(response.status_code)
# 200: Success
# 429: Rate limited
# 403: Forbidden
# 404: Not found
# 5xx: Server error
```

### Inspect HTML Structure
```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())  # Pretty-print HTML
print(soup.find_all('a'))  # Debug link parsing
```

### Verify Regex Pattern
```python
import re

pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
test_emails = [
    "valid@example.com",
    "invalid@",
    "test.email+tag@sub.example.co.uk",
]

for email in test_emails:
    if re.match(pattern, email):
        print(f"✓ {email}")
    else:
        print(f"✗ {email}")
```

## Alternatives to Scraping

- **Email finder APIs**: Hunter.io, Clearbit, EmailHunter
- **Data providers**: Apollo.io, ZoomInfo, Leadiro
- **Official feeds**: RSS, webhooks, APIs
- **Contact forms**: Send inquiry and collect response

These are often more reliable and legally compliant than scraping.

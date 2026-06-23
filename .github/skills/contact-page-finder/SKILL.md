---
name: contact-page-finder
description: 'Extract email addresses from business websites by finding and scraping contact pages. Use when: building lead lists, enriching business data, automating email discovery, scraping contact information from unknown websites.'
argument-hint: 'Website URL or list of URLs to scrape for contact information'
user-invocable: true
---

# Contact Page Finder

A workflow for discovering and extracting email addresses from business websites by intelligently finding contact pages and scraping them for email information.

## When to Use

- Building lead lists for outreach campaigns
- Enriching business contact databases
- Automating email discovery from unknown websites
- Mass-scraping contact information from multiple websites
- Finding contact pages when direct URLs are unknown
- Extracting multiple email addresses per website

## What This Skill Does

This skill implements a multi-step email extraction strategy:

1. **Scrapes the main website** for visible email addresses
2. **Finds contact page links** by searching for "contact" keywords in URLs
3. **Scrapes contact pages** for additional email addresses
4. **Deduplicates results** and returns all found emails

### Key Features

✓ Regex-based email pattern matching  
✓ Intelligent contact page discovery  
✓ Graceful error handling (timeouts, missing pages)  
✓ Request throttling with proper headers  
✓ Result deduplication  

## Procedure

### Step 1: Set Up Email Pattern Detection
Define a regex pattern to match email addresses:
```
[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}
```

### Step 2: Request the Website
- Use `requests.get()` with a User-Agent header
- Set timeout (recommended: 10 seconds)
- Handle connection errors gracefully
- Extract all emails from the HTML content using regex

### Step 3: Detect Contact Page Links
- Parse HTML with BeautifulSoup
- Find all `<a>` tags with `href` attributes
- Filter for links containing "contact" (case-insensitive)
- Convert relative URLs to absolute using `urljoin()`

### Step 4: Scrape Contact Pages
For each contact link found:
- Make HTTP request with same headers/timeout
- Extract emails using same regex pattern
- Add to results set (automatic deduplication)

### Step 5: Return Results
- Combine emails from main page + contact pages
- Remove duplicates (use `set()`)
- Return as list or comma-separated string

## Quick Implementation

See the reference implementation in [extract_emails.py](./scripts/extract_emails.py):

```python
from extract_emails import extract_emails

# Single URL
emails = extract_emails("https://example.com")
print(emails)  # ['contact@example.com', 'info@example.com']

# Multiple URLs
urls = ["https://site1.com", "https://site2.com"]
for url in urls:
    emails = extract_emails(url)
    print(f"{url}: {emails}")
```

## Configuration Options

| Option | Default | Purpose |
|--------|---------|---------|
| Timeout | 10 seconds | Prevent hanging on slow websites |
| User-Agent | Mozilla/5.0 | Avoid being blocked by servers |
| Contact keywords | "contact" | What to search for in links |
| Retry attempts | 0 | Retry failed requests |

## Troubleshooting

### No emails found
- **Cause**: Emails embedded in images, JavaScript, or forms
- **Solution**: Extend regex or use browser automation (Selenium/Playwright)

### Too many timeouts
- **Cause**: Website is slow or blocking requests
- **Solution**: Increase timeout, add rate limiting, use rotating proxies

### False positives
- **Cause**: Regex too broad (matches non-email patterns)
- **Solution**: Add stricter validation (verify domain exists)

### Rate limiting
- **Cause**: Too many requests to same server
- **Solution**: Add delays between requests using `time.sleep()`

## Integration with APP-EMAILER

This skill powers the lead enrichment pipeline in APP-EMAILER:

```python
from agent import extract_emails, save_business, save_emails

# Find a business website
website = "https://example.com"

# Extract emails using this skill
emails = extract_emails(website)

# Save to database
business_id = save_business("Example Inc", website, None, "Houston")
if business_id and emails:
    save_emails(business_id, emails)
```

## Related Tasks

- **Email validation**: Verify found emails are deliverable (use ZeroBounce API)
- **Business enrichment**: Add company details (LinkedIn, employee count, funding)
- **Contact normalization**: Parse emails to extract first/last names
- **Multi-source scraping**: Extract from Yelp, Google Maps, Yellow Pages

## References

- [BeautifulSoup Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Requests Library](https://requests.readthedocs.io/)
- [Regular Expressions Guide](https://regex101.com/)
- [Web Scraping Best Practices](./references/scraping-ethics.md)

# Quick Reference

## What This Skill Does

Extracts email addresses from websites by:
1. Scraping the main page for emails
2. Finding contact page links
3. Scraping contact pages for more emails
4. Deduplicating and returning all found emails

## Basic Usage

```python
from .scripts.extract_emails import extract_emails

# Extract from one website
emails = extract_emails("https://example.com")
# Returns: ['contact@example.com', 'info@example.com']

# Extract from multiple websites
results = extract_emails_batch([
    "https://site1.com",
    "https://site2.com",
])
```

## Key Functions

| Function | Purpose | Returns |
|----------|---------|---------|
| `extract_emails(url)` | Extract emails from website + contact pages | `List[str]` |
| `extract_emails_batch(urls)` | Extract from multiple websites | `Dict[str, List[str]]` |
| `validate_email(email)` | Check if email format is valid | `bool` |
| `_scrape_page(url)` | Scrape single page for emails | `Set[str]` |
| `_find_contact_links(url)` | Find contact page links | `List[str]` |

## Configuration

```python
# Adjust these constants in extract_emails.py
TIMEOUT = 10              # Request timeout in seconds
USER_AGENT = "Mozilla..." # HTTP User-Agent header
EMAIL_REGEX = r"..."      # Email pattern to match
```

## Error Handling

```python
try:
    emails = extract_emails(url)
except requests.Timeout:
    print("Website too slow")
except requests.RequestException as e:
    print(f"Failed to fetch: {e}")
```

## Common Issues

| Issue | Solution |
|-------|----------|
| No emails found | Site may have emails in JavaScript/images |
| Too many timeouts | Increase TIMEOUT or add rate limiting |
| Rate limited (429) | Add delays: `time.sleep(1)` between requests |
| Permission denied (403) | Website blocks automated scraping |

## Performance Tips

1. **Batch processing**: Use `extract_emails_batch()` for multiple URLs
2. **Rate limiting**: Add `time.sleep(1)` between requests
3. **Caching**: Store results to avoid re-scraping
4. **Parallel processing**: Use `ThreadPoolExecutor` for concurrent scraping

## Examples

### Find emails from company website
```python
emails = extract_emails("https://company.com")
print(emails)
```

### Save results to CSV
```python
import csv
results = extract_emails_batch(urls)
with open('emails.csv', 'w') as f:
    writer = csv.writer(f)
    for url, emails in results.items():
        for email in emails:
            writer.writerow([url, email])
```

### Integrate with APP-EMAILER
```python
from agent import extract_emails, save_business, save_emails

emails = extract_emails(website)
business_id = save_business(name, website, phone, address, "Houston")
if business_id and emails:
    save_emails(business_id, emails)
```

## Resources

- [Full SKILL.md](./SKILL.md) - Complete documentation
- [Scraping Ethics](./references/scraping-ethics.md) - Best practices
- [Usage Templates](./assets/usage_templates.py) - Code examples
- [Reference Implementation](./scripts/extract_emails.py) - Source code

## When NOT to Use

- ❌ Violates website's robots.txt
- ❌ Against website's Terms of Service
- ❌ No consent from website owner
- ❌ Personal data for unsolicited marketing (GDPR/CCPA)

## Alternatives

If scraping isn't suitable, consider:
- Email finder APIs (Hunter.io, Clearbit, Apollo)
- Data providers (ZoomInfo, Leadiro)
- Official feeds (RSS, APIs, webhooks)
- Contact forms (ask directly)

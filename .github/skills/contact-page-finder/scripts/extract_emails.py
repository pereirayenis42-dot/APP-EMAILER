"""
Contact Page Finder - Reference Implementation
Extract email addresses from business websites by finding and scraping contact pages.
"""

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Set, List

# Email regex pattern
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Request configuration
TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def extract_emails(url: str, max_contact_links: int = 5) -> List[str]:
    """
    Extract email addresses from a website and its contact pages.
    
    Args:
        url: Website URL to scrape
        max_contact_links: Maximum number of contact links to scrape (for efficiency)
    
    Returns:
        List of unique email addresses found
    
    Example:
        >>> emails = extract_emails("https://example.com")
        >>> print(emails)
        ['contact@example.com', 'info@example.com']
    """
    
    emails = set()
    
    try:
        # Step 1: Scrape main page for emails
        main_emails = _scrape_page(url)
        emails.update(main_emails)
        
        # Step 2: Find contact page links
        contact_links = _find_contact_links(url, max_links=max_contact_links)
        
        # Step 3: Scrape each contact page
        for contact_url in contact_links:
            try:
                contact_emails = _scrape_page(contact_url)
                emails.update(contact_emails)
            except Exception as e:
                print(f"  Error scraping contact page {contact_url}: {e}")
                continue
    
    except Exception as e:
        print(f"Error extracting emails from {url}: {e}")
    
    return list(emails)


def _scrape_page(url: str) -> Set[str]:
    """
    Scrape a single page for email addresses.
    
    Args:
        url: Page URL to scrape
    
    Returns:
        Set of unique email addresses found on the page
    """
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, timeout=TIMEOUT, headers=headers)
        response.raise_for_status()
        
        # Extract all email addresses from page content
        emails = set(re.findall(EMAIL_REGEX, response.text))
        
        if emails:
            print(f"  Found {len(emails)} email(s) on {url}")
        
        return emails
    
    except requests.Timeout:
        print(f"  Timeout scraping {url} (>{TIMEOUT}s)")
        return set()
    except requests.RequestException as e:
        print(f"  Request error for {url}: {e}")
        return set()


def _find_contact_links(url: str, max_links: int = 5) -> List[str]:
    """
    Find links to contact pages on a website.
    
    Args:
        url: Website URL to search
        max_links: Maximum number of contact links to return
    
    Returns:
        List of contact page URLs
    """
    contact_links = []
    
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, timeout=TIMEOUT, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all links that contain "contact" in href
        for link in soup.find_all("a", href=True):
            href = link["href"]
            
            if "contact" in href.lower():
                # Convert relative URLs to absolute
                full_url = urljoin(url, href)
                
                # Avoid duplicates
                if full_url not in contact_links:
                    contact_links.append(full_url)
                
                # Limit number of links to scrape
                if len(contact_links) >= max_links:
                    break
        
        if contact_links:
            print(f"  Found {len(contact_links)} contact link(s)")
        
        return contact_links
    
    except Exception as e:
        print(f"  Error finding contact links for {url}: {e}")
        return []


def validate_email(email: str) -> bool:
    """
    Basic email validation (format only, not delivery).
    
    Args:
        email: Email address to validate
    
    Returns:
        True if email matches pattern, False otherwise
    """
    pattern = re.compile(EMAIL_REGEX)
    return pattern.match(email) is not None


def extract_emails_batch(urls: List[str]) -> dict:
    """
    Extract emails from multiple websites.
    
    Args:
        urls: List of website URLs
    
    Returns:
        Dictionary mapping URLs to lists of emails found
    
    Example:
        >>> results = extract_emails_batch(['https://site1.com', 'https://site2.com'])
        >>> for url, emails in results.items():
        ...     print(f"{url}: {emails}")
    """
    results = {}
    
    for url in urls:
        print(f"Processing: {url}")
        emails = extract_emails(url)
        results[url] = emails
        print(f"  Found {len(emails)} unique emails\n")
    
    return results


if __name__ == "__main__":
    # Example usage
    test_urls = [
        "https://example.com",
    ]
    
    for url in test_urls:
        print(f"\nExtracting emails from: {url}")
        emails = extract_emails(url)
        print(f"Results: {emails}")

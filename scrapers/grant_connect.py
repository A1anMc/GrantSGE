import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_date(date_str: str) -> Optional[datetime]:
    """Parse date string from GrantConnect format to datetime object."""
    try:
        return datetime.strptime(date_str.strip(), '%d-%b-%Y')
    except ValueError as e:
        logger.warning(f"Could not parse date: {date_str}. Error: {e}")
        return None

def scrape_grant_connect(url: str) -> List[Dict]:
    """
    Scrape grant listings from GrantConnect search results page.
    
    Args:
        url (str): URL of the GrantConnect search results page
        
    Returns:
        List[Dict]: List of dictionaries containing grant information
        
    Example:
        >>> url = "https://www.grants.gov.au/go/list"
        >>> grants = scrape_grant_connect(url)
        >>> for grant in grants:
        ...     print(grant['title'])
    """
    try:
        # Add headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all grant listings
        # Note: Update these selectors based on actual GrantConnect HTML structure
        grant_listings = soup.find_all('div', class_='grant-listing')
        
        grants = []
        for listing in grant_listings:
            try:
                # Extract grant details
                # Note: Update these selectors based on actual GrantConnect HTML structure
                title_element = listing.find('h3', class_='grant-title')
                funder_element = listing.find('div', class_='grant-agency')
                date_element = listing.find('div', class_='grant-close-date')
                link_element = title_element.find('a') if title_element else None
                
                if not all([title_element, funder_element, date_element, link_element]):
                    logger.warning(f"Skipping incomplete grant listing: {listing}")
                    continue
                
                # Build the full URL for the grant detail page
                detail_url = link_element['href']
                if not detail_url.startswith('http'):
                    detail_url = f"https://www.grants.gov.au{detail_url}"
                
                grant_data = {
                    'title': title_element.text.strip(),
                    'funder': funder_element.text.strip(),
                    'closing_date': parse_date(date_element.text),
                    'detail_url': detail_url,
                    'scraped_at': datetime.utcnow()
                }
                
                grants.append(grant_data)
                logger.info(f"Successfully scraped grant: {grant_data['title']}")
                
            except Exception as e:
                logger.error(f"Error processing grant listing: {e}")
                continue
        
        return grants
        
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return []

def scrape_grant_details(detail_url: str) -> Dict:
    """
    Scrape detailed information from a grant's detail page.
    
    Args:
        detail_url (str): URL of the grant detail page
        
    Returns:
        Dict: Detailed grant information
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(detail_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Note: Update these selectors based on actual GrantConnect HTML structure
        details = {
            'description': soup.find('div', class_='grant-description').text.strip() if soup.find('div', class_='grant-description') else None,
            'amount': soup.find('div', class_='grant-amount').text.strip() if soup.find('div', class_='grant-amount') else None,
            'eligibility': soup.find('div', class_='grant-eligibility').text.strip() if soup.find('div', class_='grant-eligibility') else None,
            # Add more fields as needed
        }
        
        return details
        
    except Exception as e:
        logger.error(f"Error scraping grant details from {detail_url}: {e}")
        return {} 
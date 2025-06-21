import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase: Client = create_client(
    os.getenv('SUPABASE_URL', ''),
    os.getenv('SUPABASE_SERVICE_ROLE_KEY', '')
)

class GrantScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def parse_amount(self, amount_text: str) -> Dict:
        """Parse amount text into structured format."""
        amount_text = amount_text.lower().strip()
        try:
            if 'up to' in amount_text:
                return {'max': float(amount_text.split('up to')[1].strip().replace('$', '').replace(',', ''))}
            elif '-' in amount_text:
                min_str, max_str = amount_text.split('-')
                return {
                    'min': float(min_str.strip().replace('$', '').replace(',', '')),
                    'max': float(max_str.strip().replace('$', '').replace(',', ''))
                }
            elif '$' in amount_text:
                return {'fixed': float(amount_text.replace('$', '').replace(',', ''))}
            return {'description': amount_text}
        except:
            return {'description': amount_text}

    def parse_date(self, date_text: str) -> Optional[str]:
        """Parse date text into ISO format."""
        try:
            # Add more date formats as needed
            formats = [
                '%d/%m/%Y',
                '%Y-%m-%d',
                '%B %d, %Y',
                '%d %B %Y'
            ]
            for fmt in formats:
                try:
                    return datetime.strptime(date_text.strip(), fmt).isoformat()
                except ValueError:
                    continue
            return None
        except:
            return None

    def scrape_grants_gov_au(self) -> List[Dict]:
        """Scrape grants from grants.gov.au."""
        grants = []
        url = 'https://www.grants.gov.au/grants/all-grants'
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example selectors - adjust based on actual HTML structure
            grant_elements = soup.find_all('div', class_='grant-card')
            
            for element in grant_elements:
                grant = {
                    'title': element.find('h3').text.strip(),
                    'funder': element.find('div', class_='funder').text.strip(),
                    'description': element.find('div', class_='description').text.strip(),
                    'amount_range': self.parse_amount(element.find('div', class_='amount').text.strip()),
                    'due_date': self.parse_date(element.find('div', class_='due-date').text.strip()),
                    'source_url': element.find('a')['href'],
                    'guidelines_url': element.find('a', class_='guidelines')['href']
                }
                grants.append(grant)
                
        except Exception as e:
            print(f"Error scraping grants.gov.au: {e}")
        
        return grants

    def scrape_community_grants(self) -> List[Dict]:
        """Scrape grants from community grants websites."""
        # Implementation for additional grant sources
        return []

    def save_to_supabase(self, grants: List[Dict]) -> None:
        """Save grants to Supabase database."""
        try:
            for grant in grants:
                # Check if grant already exists
                existing = supabase.table('grants').select('id').eq('source_url', grant['source_url']).execute()
                
                if not existing.data:
                    # Insert new grant
                    supabase.table('grants').insert(grant).execute()
                else:
                    # Update existing grant
                    supabase.table('grants').update(grant).eq('source_url', grant['source_url']).execute()
                    
        except Exception as e:
            print(f"Error saving to Supabase: {e}")

def main():
    scraper = GrantScraper()
    
    # Scrape from different sources
    grants = []
    grants.extend(scraper.scrape_grants_gov_au())
    grants.extend(scraper.scrape_community_grants())
    
    # Save to database
    scraper.save_to_supabase(grants)
    
    print(f"Scraped {len(grants)} grants")

if __name__ == '__main__':
    main() 
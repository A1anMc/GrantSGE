from grant_connect import scrape_grant_connect, scrape_grant_details

def test_grant_connect_scraper():
    # Test URL - replace with an actual GrantConnect search results page
    test_url = "https://www.grants.gov.au/go/list"
    
    print("Testing GrantConnect scraper...")
    
    # Test main listing scraper
    grants = scrape_grant_connect(test_url)
    
    if not grants:
        print("No grants found or error occurred")
        return
    
    print(f"\nFound {len(grants)} grants")
    
    # Print first grant as example
    print("\nExample grant:")
    for key, value in grants[0].items():
        print(f"{key}: {value}")
    
    # Test detail scraper with first grant
    print("\nTesting detail scraper...")
    details = scrape_grant_details(grants[0]['detail_url'])
    
    print("\nGrant details:")
    for key, value in details.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    test_grant_connect_scraper() 
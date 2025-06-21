import os
from dotenv import load_dotenv
from supabase import create_client, Client
import requests
from bs4 import BeautifulSoup

def test_env():
    """Test environment variables are loaded"""
    load_dotenv()
    required_vars = [
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print("❌ Missing environment variables:", missing)
        return False
    print("✅ Environment variables loaded")
    return True

def test_supabase():
    """Test Supabase connection"""
    try:
        supabase: Client = create_client(
            os.getenv('SUPABASE_URL', ''),
            os.getenv('SUPABASE_ANON_KEY', '')
        )
        # Try a simple query
        response = supabase.table('grants').select("count", count='exact').execute()
        print(f"✅ Supabase connected. Found {response.count} grants")
        return True
    except Exception as e:
        print("❌ Supabase connection failed:", str(e))
        return False

def test_scraper():
    """Test web scraping functionality"""
    try:
        url = 'https://www.grants.gov.au'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        print("✅ Web scraping working")
        return True
    except Exception as e:
        print("❌ Web scraping failed:", str(e))
        return False

def test_ai():
    """Test AI service connection"""
    ai_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GROQ_API_KEY']
    available_services = [key for key in ai_keys if os.getenv(key)]
    
    if not available_services:
        print("❌ No AI service keys found")
        return False
    
    print(f"✅ Found {len(available_services)} AI service(s):", available_services)
    return True

def main():
    print("\n🔍 Testing Grant Application Dashboard Setup\n")
    
    tests = [
        ("Environment Variables", test_env),
        ("Supabase Connection", test_supabase),
        ("Web Scraping", test_scraper),
        ("AI Services", test_ai)
    ]
    
    results = []
    for name, test_func in tests:
        print(f"\n📋 Testing {name}...")
        results.append(test_func())
    
    print("\n📊 Summary:")
    for (name, _), result in zip(tests, results):
        status = "✅ Passed" if result else "❌ Failed"
        print(f"{name}: {status}")
    
    if all(results):
        print("\n🎉 All tests passed! You're ready to start development.")
    else:
        print("\n⚠️  Some tests failed. Please check the errors above and fix them before proceeding.")

if __name__ == '__main__':
    main() 
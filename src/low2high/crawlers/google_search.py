import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import urllib.parse
import uuid

class GoogleSearchCrawler:
    """
    Uses DuckDuckGo HTML search as a fallback web scraper.
    (Named GoogleSearchCrawler for historical reasons, but uses DDG to avoid hard blocking).
    """
    def __init__(self):
        self.base_url = "https://html.duckduckgo.com/html/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def search_businesses(self, city: str, category: str) -> List[Dict[str, Any]]:
        query = f"{category} in {city}"
        print(f"Running fallback web search for '{query}'...")
        
        businesses = []
        try:
            resp = requests.post(
                self.base_url,
                data={"q": query},
                headers=self.headers,
                timeout=15
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            
            results = soup.find_all("div", class_="result")
            for result in results:
                title_elem = result.find("h2", class_="result__title")
                snippet_elem = result.find("a", class_="result__snippet")
                url_elem = result.find("a", class_="result__url")
                
                if not title_elem or not url_elem:
                    continue
                    
                name = title_elem.text.strip()
                url = url_elem.get("href", "")
                
                # DDG often prefixes URLs with //duckduckgo.com/l/?uddg=...
                if "uddg=" in url:
                    parsed = urllib.parse.urlparse(url)
                    qs = urllib.parse.parse_qs(parsed.query)
                    if "uddg" in qs:
                        url = qs["uddg"][0]
                        
                if not url.startswith("http"):
                    url = "https://" + url.lstrip("/")

                # Skip standard directory sites, we want the actual business websites
                skip_domains = ["yelp.com", "tripadvisor.com", "yellowpages.com", "facebook.com", "instagram.com", "linkedin.com", "zomato.com", "justdial.com"]
                if any(domain in url for domain in skip_domains):
                    continue
                    
                businesses.append({
                    "name": name,
                    "address": f"Located in {city}", # Search results rarely give exact addresses
                    "latitude": None,
                    "longitude": None,
                    "rating": None,
                    "reviews_count": None,
                    "place_id": f"web_{uuid.uuid4().hex[:10]}",
                    "phone": None, # Search results rarely give raw phones
                    "website": url,
                    "source": "web_search"
                })
                
                if len(businesses) >= 10:
                    break
                    
        except Exception as e:
            print(f"Fallback search error: {e}")
            
        print(f"Found {len(businesses)} results via fallback web search.")
        return businesses

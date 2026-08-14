from typing import Dict, Any
from sqlalchemy.future import select
from src.low2high.models.business import Business
from src.low2high.models.database import AsyncSessionLocal
from src.low2high.utils.dedup import normalize_phone
from src.low2high.crawlers.osm_crawler import OSMCrawler
from src.low2high.crawlers.google_search import GoogleSearchCrawler

class DiscoveryAgent:
    def __init__(self):
        self.maps_crawler = OSMCrawler()
        self.search_crawler = GoogleSearchCrawler()

    async def run_discovery(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        city = payload.get("location", {}).get("city", "")
        category = payload.get("category", "")
        
        print(f"Starting discovery for {category} in {city}...")
        
        # maps_results = self.maps_crawler.search_businesses(city, category)
        # search_results = []
        # if len(maps_results) < 5:
        #     search_results = self.search_crawler.search_businesses(city, category)
        # all_results = maps_results + search_results
        
        # DEMO DATA (Mocking API responses for Phase 1 testing)
        print("Using Demo Data for Discovery (Google Maps API pending)...")
        all_results = [
            {
                "place_id": "ChIJD7fiBh9u5kcRYJSMaMOCCwQ",
                "name": "Apex Digital Marketing",
                "address": f"101 Tech Blvd, {city}",
                "phone": "+1-555-0199",
                "email": "hello@apexdigitaldemo.com",
                "website": "https://apexdigitaldemo.com",
                "rating": 4.8,
                "reviews_count": 124,
                "latitude": 37.7749,
                "longitude": -122.4194,
                "source": "google_maps_demo"
            },
            {
                "place_id": "ChIJb_fHbh9u5kcR4PPMaMOCCwQ",
                "name": "Hometown Diner & Cafe",
                "address": f"45 Main St, {city}",
                "phone": "+1-555-0255",
                "email": None,
                "website": "", # No website!
                "rating": 4.2,
                "reviews_count": 89,
                "latitude": 37.7845,
                "longitude": -122.4150,
                "source": "google_maps_demo"
            },
            {
                "place_id": "ChIJc_hGfh9u5kcR8TQMxNOCCwQ",
                "name": "Mike's Neighborhood Garage",
                "address": f"900 Industrial Way, {city}",
                "phone": "+1-555-0800",
                "email": None,
                "website": None, # No website!
                "rating": 3.5,
                "reviews_count": 12,
                "latitude": 37.7654,
                "longitude": -122.4032,
                "source": "google_maps_demo"
            }
        ]
        
        # Quality Control: Filter out leads without a website AND without a phone
        valid_results = []
        for b in all_results:
            if b.get('website') or b.get('phone'):
                valid_results.append(b)
        
        saved_count = await self._save_businesses(valid_results, category)
                
        return {
            "job_id": payload.get("job_id"),
            "status": "completed",
            "total_discovered": len(valid_results),
            "new_businesses_saved": saved_count
        }

    async def import_from_json(self, json_data: list, category: str = "Imported") -> Dict[str, Any]:
        print(f"Importing {len(json_data)} businesses from JSON...")
        
        valid_results = []
        for b in json_data:
            if b.get('website') or b.get('phone'):
                valid_results.append(b)
                
        saved_count = await self._save_businesses(valid_results, category)
        
        return {
            "status": "completed",
            "total_discovered": len(valid_results),
            "new_businesses_saved": saved_count
        }
        
    async def _save_businesses(self, businesses: list, category: str) -> int:
        saved_count = 0
        async with AsyncSessionLocal() as session:
            for biz_data in businesses:
                raw_phone = biz_data.get("phone")
                norm_phone = normalize_phone(raw_phone) if raw_phone else None
                
                existing = None
                if norm_phone:
                    result = await session.execute(select(Business).where(Business.phone == norm_phone))
                    existing = result.scalars().first()
                
                if not existing and biz_data.get("place_id"):
                    result = await session.execute(select(Business).where(Business.place_id == biz_data["place_id"]))
                    existing = result.scalars().first()
                    
                if not existing:
                    biz_data["phone"] = norm_phone
                    biz_data["category"] = category
                    
                    new_biz = Business(**biz_data)
                    session.add(new_biz)
                    saved_count += 1
            
            await session.commit()
            
        return saved_count

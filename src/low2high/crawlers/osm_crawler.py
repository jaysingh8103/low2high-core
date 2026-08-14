import requests
from typing import List, Dict, Any

class OSMCrawler:
    def __init__(self):
        self.overpass_url = "http://overpass-api.de/api/interpreter"
        # Expanded tag list for a much broader discovery net
        self.search_tags = ["amenity", "shop", "office", "leisure", "healthcare", "craft", "tourism"]

    def search_businesses(self, city: str, category: str) -> List[Dict[str, Any]]:
        print(f"Querying OpenStreetMap (Overpass API) for {category} in {city}...")
        category = category.lower()
        
        # Build a dynamic query that checks ALL relevant commercial tags
        query_parts = []
        for tag in self.search_tags:
            query_parts.append(f'node[{tag}~"{category}"](area.searchArea);')
            query_parts.append(f'way[{tag}~"{category}"](area.searchArea);')
            
        combined_queries = "\n          ".join(query_parts)
            
        query = f"""
        [out:json];
        area[name="{city}"]->.searchArea;
        (
          {combined_queries}
        );
        out center;
        """
        
        try:
            headers = {"User-Agent": "Low2High_DiscoveryAgent/2.0"}
            response = requests.post(self.overpass_url, data=query, headers=headers, timeout=25)
            response.raise_for_status()
            data = response.json()
            
            businesses = []
            for element in data.get('elements', []):
                tags = element.get('tags', {})
                if not tags.get('name'):
                    continue # Skip unnamed locations
                    
                lat = element.get('lat') or (element.get('center', {})).get('lat')
                lon = element.get('lon') or (element.get('center', {})).get('lon')
                
                # Robust Address Parsing
                address_parts = []
                if tags.get('addr:housenumber'): address_parts.append(tags.get('addr:housenumber'))
                if tags.get('addr:street'): address_parts.append(tags.get('addr:street'))
                if tags.get('addr:city'): address_parts.append(tags.get('addr:city'))
                if tags.get('addr:postcode'): address_parts.append(tags.get('addr:postcode'))
                
                address = ", ".join(address_parts)
                if not address:
                    address = city
                    
                biz = {
                    "name": tags.get('name'),
                    "address": address,
                    "latitude": lat,
                    "longitude": lon,
                    "rating": None,
                    "reviews_count": None,
                    "place_id": f"osm_{element.get('id')}",
                    "phone": tags.get('phone') or tags.get('contact:phone'),
                    "website": tags.get('website') or tags.get('contact:website'),
                    "source": "openstreetmap"
                }
                businesses.append(biz)
            
            # Deduplicate by name just in case node/way return the same place
            unique_businesses = {b['name']: b for b in businesses}.values()
            
            print(f"Found {len(unique_businesses)} unique results on OpenStreetMap.")
            return list(unique_businesses)
            
        except Exception as e:
            print(f"Error querying OpenStreetMap: {e}")
            return []

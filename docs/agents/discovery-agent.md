# Business Discovery Agent

## Purpose
Continuously discover businesses from public sources within a specified geographical area and category.

## Tools & Dependencies
- **Playwright / Crawl4AI**: For headless browser crawling of directory sites.
- **Google Maps API**: Primary source for local business discovery (Places API).
- **BeautifulSoup4**: For parsing static HTML public listings.

## Input JSON Contract
```json
{
  "job_id": "disc_12345",
  "location": {
    "city": "Indore",
    "lat": 22.7196,
    "lng": 75.8577,
    "radius_km": 10
  },
  "category": "Restaurant",
  "keywords": ["dining", "cafe", "food"]
}
```

## Output JSON Contract
```json
{
  "businesses": [
    {
      "business_id": "biz_8829",
      "name": "ABC Restaurant",
      "address": "123 Main St, Indore",
      "phone": "+91XXXXXXXXXX",
      "website": "abc.com",
      "rating": 4.2,
      "reviews": 245,
      "source": "google_maps",
      "place_id": "ChIJ..."
    }
  ],
  "total_discovered": 1
}
```

## Internal Execution Flow
1. **Receive Job**: Consumes payload from the message queue.
2. **Query Google Maps API**: Searches for `category` in `location`.
3. **Scrape Directories**: Uses Crawl4AI to scrape JustDial/IndiaMART if Maps yields < 10 results.
4. **Deduplication**: Normalizes phone numbers (E.164) and addresses to remove duplicates.
5. **Persistence**: Saves new entries to the `businesses` table in SQLite.

## Error Handling
- **API Limits**: If Google Maps rate limit is hit, sleeps for 60s and retries.
- **Scraper Blocks**: If Crawl4AI receives a CAPTCHA or 403, it routes the request through a residential proxy pool.


## Configuration
LLM Prompts and backstories for this agent are stored in src/low2high/config/agents.yaml and 	asks.yaml.
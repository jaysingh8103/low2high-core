# Website Audit Agent

## Purpose
Determine website quality, technical performance, and presence of conversion tools based on modern web standards.

## Tools & Dependencies
- **Lighthouse API / Pyppeteer**: For generating performance and accessibility scores.
- **Playwright**: To load the DOM and check for dynamic widgets (chatbots).
- **urllib3 / requests**: For SSL and broken link validation.

## Input JSON Contract
```json
{
  "business_id": "biz_8829",
  "website_url": "https://abc.com"
}
```

## Output JSON Contract
```json
{
  "business_id": "biz_8829",
  "website_score": 72,
  "metrics": {
    "ssl_enabled": true,
    "mobile_responsive": true,
    "load_time_ms": 3400,
    "broken_links": 3,
    "contact_form_present": false,
    "chat_widget_present": false,
    "online_booking_present": false
  },
  "lighthouse_scores": {
    "performance": 65,
    "accessibility": 80,
    "best_practices": 90
  }
}
```

## Internal Execution Flow
1. **SSL Validation**: Performs a quick HEAD request to verify HTTPS and cert validity.
2. **Lighthouse Audit**: Triggers a mobile Lighthouse scan to get load speeds and responsiveness metrics.
3. **DOM Parsing**: Uses Playwright to wait for the page to reach `networkidle`.
4. **Element Detection**: 
   - Looks for `<form>` tags containing "contact", "email", or "message".
   - Looks for common chat widget iframes (Intercom, Zendesk, Tawk.to).
   - Looks for booking keywords/buttons ("Book Now", "Reserve").
5. **Link Checking**: Scrapes all `href` attributes and runs concurrent HEAD requests to find 404s.

## Error Handling
- **Timeout**: If the website fails to load within 15 seconds, marks `website_score: 0` and `status: "offline"`.
- **Bot Mitigation**: If blocked by Cloudflare, falls back to a stealth Playwright context.


## Configuration
LLM Prompts and backstories for this agent are stored in src/low2high/config/agents.yaml and 	asks.yaml.
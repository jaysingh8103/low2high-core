# Data Privacy & Compliance

As a platform that discovers and audits businesses, ensuring data privacy and compliance with regional regulations (such as GDPR, CCPA, or DPDP Act) is crucial.

## 1. Public Data Handling
- The `Discovery Agent` only scrapes information that is publicly available on the internet (Google Maps, public websites).
- We do not attempt to bypass paywalls, private networks, or password-protected directories.

## 2. PII (Personally Identifiable Information)
- The platform deals primarily with **Business Entity Data** (Business Name, Public Phone, Public Address), which is generally excluded from strict PII definitions.
- However, if a business owner provides personal contact information via the inbound lead form, it is treated as PII.
- PII is masked in application logs and analytics dashboards.

## 3. Data Retention & Deletion
- **Audit Data**: Raw audit data (like HTML DOM snapshots) are retained for 30 days and then automatically purged from SQLite.
- **Right to be Forgotten**: We provide an internal API mechanism for businesses to request deletion of their profile from our database, ensuring compliance with data removal requests.

## 4. Crawling Etiquette
- The `Website Audit Agent` strictly respects `robots.txt` directives.
- We utilize identifiable User-Agent strings (e.g., `Low2HighBot/1.0`) so webmasters can easily identify our traffic.

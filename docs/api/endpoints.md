# API Endpoints Detailed

## 1. Initiate Discovery
**POST** `/api/v1/search-businesses`

Initiates a background task to discover businesses in a specific area.

**cURL Example**:
```bash
curl -X POST "https://api.low2high.com/api/v1/search-businesses"      -H "Authorization: Bearer YOUR_JWT_TOKEN"      -H "Content-Type: application/json"      -d '{
           "city": "Indore",
           "category": "Restaurant",
           "radius_km": 10
         }'
```

**Response (202 Accepted)**:
```json
{
  "job_id": "disc_9901",
  "status": "processing",
  "message": "Discovery task queued."
}
```

## 2. Get Business Profile
**GET** `/api/v1/business/{business_id}`

Retrieves the complete profile and latest audit scores for a business.

**cURL Example**:
```bash
curl -X GET "https://api.low2high.com/api/v1/business/biz_8829"      -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response (200 OK)**:
```json
{
  "id": "biz_8829",
  "name": "ABC Restaurant",
  "digital_score": 45,
  "classification": "Basic Digital Presence",
  "audits": {
    "website": 72,
    "seo": 38
  }
}
```

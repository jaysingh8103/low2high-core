# API Request/Response Data

Example `POST /search-businesses` Request:
```json
{
  "city": "Indore",
  "category": "Restaurant",
  "radius_km": 10
}
```

Example Response:
```json
{
  "job_id": "req_1234abc",
  "status": "processing",
  "message": "Discovery started."
}
```

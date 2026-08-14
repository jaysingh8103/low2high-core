# Coding Rules & Snippets

## Architecture Rules
- Fast, async I/O.
- Strict Pydantic models for all agent contracts.

## Example: FastAPI Endpoint with Pydantic
```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
import uuid

router = APIRouter()

class SearchRequest(BaseModel):
    city: str = Field(..., description="Target city for discovery")
    category: str = Field(..., description="Business category")
    radius_km: int = Field(default=10, ge=1, le=50)

class SearchResponse(BaseModel):
    job_id: str
    status: str

@router.post("/search-businesses", response_model=SearchResponse, status_code=202)
async def search_businesses(request: SearchRequest):
    # Enqueue task to Celery/Redis
    job_id = f"disc_{uuid.uuid4().hex[:8]}"
    # task_queue.send(job_id, request.dict())
    return SearchResponse(job_id=job_id, status="processing")
```

# Prompt Engineering Details

We use `instructor` with `openai` to force structured JSON outputs from the LLM, ensuring the Recommendation Agent never outputs free-text that breaks the pipeline.

## Example System Prompt
```text
You are an elite Digital Transformation Consultant.
Your goal is to analyze the following business metrics and generate a 3-step actionable roadmap.
Prioritize low-cost, high-impact digital changes.
Do NOT recommend a website overhaul if their website score is > 80.
Do NOT hallucinate costs; use standard market rates for SMBs.
```

## Code Example: Enforcing JSON
```python
import instructor
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import List

client = instructor.apatch(AsyncOpenAI())

class Recommendation(BaseModel):
    priority: int
    title: str
    description: str
    estimated_cost_usd: float

class Roadmap(BaseModel):
    recommendations: List[Recommendation]

async def generate_roadmap(business_context: str) -> Roadmap:
    return await client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=Roadmap,
        messages=[
            {"role": "system", "content": "You are an elite Digital Transformation Consultant."},
            {"role": "user", "content": business_context}
        ]
    )
```

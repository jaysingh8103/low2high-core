import asyncio
import sys
from pathlib import Path
from sqlalchemy.future import select

sys.path.insert(0, str(Path(__file__).parent.parent))

from dotenv import load_dotenv
load_dotenv()

from src.low2high.models.database import init_db, AsyncSessionLocal
from src.low2high.models.business import Business
from src.low2high.agents.discovery_agent import DiscoveryAgent

async def run_test():
    await init_db()
    
    # Clear table before test
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Business))
        for biz in result.scalars().all():
            await session.delete(biz)
        await session.commit()
    
    agent = DiscoveryAgent()
    
    payloads = [
        {"job_id": "test_job_1", "location": {"city": "Indore"}, "category": "Restaurant"},
        {"job_id": "test_job_2", "location": {"city": "Indore"}, "category": "Gym"},
        {"job_id": "test_job_3", "location": {"city": "Indore"}, "category": "Salon"}
    ]
    
    for payload in payloads:
        result = await agent.run_discovery(payload)
        print(f"\n--- Discovery Result for {payload['category']} ---")
        print(f"Total Discovered (raw): {result['total_discovered']}")
        print(f"New Businesses Saved (deduplicated): {result['new_businesses_saved']}")
    
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Business))
        saved_businesses = result.scalars().all()
        print("\n--- Saved Businesses ---")
        for b in saved_businesses:
            print(f"- {b.name} | Phone: {b.phone} | Source: {b.source}")

if __name__ == "__main__":
    asyncio.run(run_test())

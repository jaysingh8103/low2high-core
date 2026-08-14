import asyncio
import sys
from pathlib import Path
import json

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.low2high.agents.audit_pipeline import AuditPipeline

async def run_test():
    pipeline = AuditPipeline()
    
    # Using a real accessible URL for testing Playwright and scraping
    test_url = "https://example.com"
    business_id = "test_biz_example"
    
    result = await pipeline.run_full_audit(business_id, test_url)
    
    print("\n=== AUDIT RESULTS ===")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(run_test())

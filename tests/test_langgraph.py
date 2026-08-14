import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from src.low2high.agents.orchestrator import Orchestrator

async def run_test():
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY is missing in .env")
        return

    orchestrator = Orchestrator()
    graph = orchestrator.build_graph()
    
    initial_state = {
        "business_id": "test_biz_langgraph",
        "website_url": "https://example.com"
    }
    
    print("=== Invoking LangGraph ===")
    result = await graph.ainvoke(initial_state)
    
    print("\n=== FINAL LANGGRAPH STATE ===")
    print(f"Business: {result['business_id']}")
    print(f"Overall Health: {result['audit_results']['overall_health']}")
    print(f"Maturity Grade: {result['maturity_grade']}")
    print("\nAI Recommendations:")
    print(result['recommendations'])

if __name__ == "__main__":
    asyncio.run(run_test())

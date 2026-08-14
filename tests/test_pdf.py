import asyncio
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()

from src.low2high.agents.orchestrator import Orchestrator
from src.low2high.utils.pdf_generator import PDFGenerator

async def run_test():
    if not os.getenv("GROQ_API_KEY"):
        print("ERROR: GROQ_API_KEY is missing in .env")
        return

    orchestrator = Orchestrator()
    graph = orchestrator.build_graph()
    
    initial_state = {
        "business_id": "PDF_Test_Business",
        "website_url": "https://example.com"
    }
    
    print("=== Running Audit & AI Recommendation ===")
    result = await graph.ainvoke(initial_state)
    
    print("=== Generating PDF ===")
    pdf_gen = PDFGenerator()
    pdf_gen.generate_pdf(result, "pdf_test_report.pdf")

if __name__ == "__main__":
    asyncio.run(run_test())

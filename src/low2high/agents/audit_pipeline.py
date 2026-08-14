import asyncio
from typing import Dict, Any
from src.low2high.agents.website_agent import WebsiteAuditAgent
from src.low2high.agents.seo_agent import SEOAgent
from src.low2high.agents.social_agent import SocialAgent

class AuditPipeline:
    def __init__(self):
        self.website_agent = WebsiteAuditAgent()
        self.seo_agent = SEOAgent()
        self.social_agent = SocialAgent()

    async def run_full_audit(self, business_id: str, website_url: str) -> Dict[str, Any]:
        print(f"--- Starting Full Digital Audit Pipeline for {business_id} ---")
        
        if not website_url:
            print("No website URL provided. Skipping technical audits.")
            return {
                "business_id": business_id,
                "website_url": website_url,
                "website_audit": {"website_score": 0, "metrics": {}},
                "seo_audit": {"seo_score": 0},
                "social_audit": {},
                "overall_health": 0
            }
            
        # 1. Run Website Agent (generates DOM snapshot)
        website_results = await self.website_agent.run_audit(business_id, website_url)
        html_content = website_results.pop("html_content", "")
        
        # 2. Run Synchronous Agents locally parsing the DOM
        seo_results = self.seo_agent.run_audit(business_id, html_content)
        social_results = self.social_agent.run_audit(business_id, html_content)
        
        # 3. Combine results
        final_report = {
            "business_id": business_id,
            "website_url": website_url,
            "website_audit": website_results,
            "seo_audit": seo_results,
            "social_audit": social_results,
            "overall_health": (website_results.get("website_score", 0) + seo_results.get("seo_score", 0)) / 2
        }
        
        return final_report

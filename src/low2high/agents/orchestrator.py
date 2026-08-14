from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END
from src.low2high.agents.audit_pipeline import AuditPipeline
from src.low2high.agents.recommendation_agent import RecommendationAgent
from src.low2high.agents.email_agent import EmailAgent

# Define the State
class AuditState(TypedDict):
    business_id: str
    website_url: str
    audit_results: Dict[str, Any]
    recommendations: str
    maturity_grade: str
    draft_email: str

class Orchestrator:
    def __init__(self):
        self.audit_pipeline = AuditPipeline()
        self.recommendation_agent = RecommendationAgent()
        self.email_agent = EmailAgent()

    async def node_run_audits(self, state: AuditState):
        print(f"[Orchestrator] Running Technical Audits for {state['business_id']}...")
        try:
            results = await self.audit_pipeline.run_full_audit(state['business_id'], state['website_url'])
        except Exception as e:
            print(f"[Orchestrator] Audit failed: {e}")
            results = {"overall_health": 0, "website_audit": {}, "seo_audit": {}, "social_audit": {}}
        return {"audit_results": results}

    async def node_generate_recommendations(self, state: AuditState):
        print(f"[Orchestrator] Generating AI Recommendations...")
        
        # If no website is provided, short-circuit and provide a fixed recommendation
        if not state.get('website_url'):
            return {"recommendations": '[{"weakness": "No Digital Presence", "solution": "Build a modern, mobile-responsive website to establish an online presence.", "impact": "High: Essential for discovery and credibility.", "priority": "High", "effort": "High"}]'}

        # Skip if audit failed to gather any meaningful data
        if state['audit_results'].get('overall_health', 0) == 0:
            return {"recommendations": "[]"}
            
        rec = self.recommendation_agent.generate_recommendations(state['audit_results'])
        return {"recommendations": rec}

    async def node_calculate_maturity(self, state: AuditState):
        print(f"[Orchestrator] Calculating Digital Maturity Score...")
        health = state['audit_results'].get('overall_health', 0)
        
        grade = "F"
        if health >= 90: grade = "A"
        elif health >= 80: grade = "B"
        elif health >= 70: grade = "C"
        elif health >= 60: grade = "D"
        
        return {"maturity_grade": grade}

    async def node_draft_email(self, state: AuditState):
        print(f"[Orchestrator] Drafting Outreach Email...")
        if state['audit_results'].get('overall_health', 0) == 0 and not state.get('website_url'):
            # Offline business, simplify recommendations payload for prompt
            draft = self.email_agent.draft_email(state['business_id'], state.get('maturity_grade', 'F'), state.get('recommendations', ''))
            return {"draft_email": draft}
            
        draft = self.email_agent.draft_email(state['business_id'], state.get('maturity_grade', 'F'), state.get('recommendations', ''))
        return {"draft_email": draft}

    def build_graph(self):
        workflow = StateGraph(AuditState)
        
        # Add Nodes
        workflow.add_node("run_audits", self.node_run_audits)
        workflow.add_node("generate_recommendations", self.node_generate_recommendations)
        workflow.add_node("calculate_maturity", self.node_calculate_maturity)
        workflow.add_node("draft_email_node", self.node_draft_email)
        
        # Add Edges
        workflow.set_entry_point("run_audits")
        workflow.add_edge("run_audits", "generate_recommendations")
        workflow.add_edge("generate_recommendations", "calculate_maturity")
        workflow.add_edge("calculate_maturity", "draft_email_node")
        workflow.add_edge("draft_email_node", END)
        
        return workflow.compile()

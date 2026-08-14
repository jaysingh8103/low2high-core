import streamlit as st
import asyncio
import json
import os
import sys
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path and load environment variables FIRST
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
load_dotenv()

from src.low2high.models.database import engine, get_db, init_db
from src.low2high.models.business import Business
from sqlalchemy.future import select

from src.low2high.agents.orchestrator import Orchestrator
from src.low2high.agents.discovery_agent import DiscoveryAgent
from src.low2high.integrations.mailer import AutoMailer

st.set_page_config(page_title="Low2High Dashboard", layout="wide")
st.title("Low2High Digital Agency Platform")

async def init_and_get_businesses():
    # Initialize DB (create tables if missing)
    await init_db()
    # Query businesses
    async with get_db() as session:
        result = await session.execute(select(Business).limit(50))
        return result.scalars().all()

async def save_audit_to_db(b_id: str, grade: str, audit_data: dict):
    async with get_db() as session:
        result = await session.execute(select(Business).where(Business.id == b_id))
        biz = result.scalars().first()
        if biz:
            biz.audit_grade = grade
            biz.audit_data = json.dumps(audit_data)
            await session.commit()

def run_async(coro):
    """Run async coroutine in a background thread with ProactorEventLoop on Windows.
    Playwright requires ProactorEventLoop to spawn browser subprocesses."""
    import sys

    def _run(coro):
        if sys.platform == "win32":
            loop = asyncio.ProactorEventLoop()
        else:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        future = pool.submit(_run, coro)
        return future.result()
st.sidebar.header("Actions")
if st.sidebar.button("Run Phase 1 Discovery"):
    with st.spinner("Running Discovery Agent (Demo)..."):
        agent = DiscoveryAgent()
        payload = {"location": {"city": "San Francisco"}, "category": "Local Business"}
        result = run_async(agent.run_discovery(payload))
        st.sidebar.success(f"Discovered {result['total_discovered']} businesses. Saved {result['new_businesses_saved']}.")
        st.rerun()

st.sidebar.divider()
st.sidebar.subheader("Import Custom Data")
uploaded_file = st.sidebar.file_uploader("Upload Phase 1 JSON", type=["json"])
if uploaded_file is not None:
    if st.sidebar.button("Import JSON Data"):
        with st.spinner("Importing..."):
            try:
                json_data = json.load(uploaded_file)
                if isinstance(json_data, list):
                    agent = DiscoveryAgent()
                    result = run_async(agent.import_from_json(json_data, category="JSON Upload"))
                    st.sidebar.success(f"Imported {result['total_discovered']} businesses. Saved {result['new_businesses_saved']} new records.")
                    import time; time.sleep(1) # Let the user see the success message briefly
                    st.rerun()
                else:
                    st.sidebar.error("Invalid JSON format. Expected a list of businesses.")
            except Exception as e:
                st.sidebar.error(f"Error parsing JSON: {e}")

st.header("Discovered Leads")
businesses = run_async(init_and_get_businesses())

if not businesses:
    st.info("No businesses found in the database. Run Discovery Phase 1 first.")
else:
    for b in businesses:
        with st.expander(f"{b.name} ({b.category})"):
            # Create a 2-column layout for details
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"📍 **Address:** {b.address or 'N/A'}")
                st.markdown(f"📞 **Phone:** {b.phone or 'N/A'}")
                st.markdown(f"✉️ **Email:** {b.email or 'N/A'}")
            
            with col2:
                st.markdown(f"🌐 **Website:** {b.website or 'N/A'}")
                st.markdown(f"⭐ **Rating:** {b.rating or 'N/A'} ({b.reviews_count or 0} reviews)")
                st.markdown(f"📅 **Added On:** {b.created_at.strftime('%Y-%m-%d') if b.created_at else 'N/A'}")
                
            st.divider()
            
            if st.button("Run Digital Audit", key=b.id):
                with st.spinner(f"Running LangGraph AI Audit for {b.name}..."):
                    
                    orchestrator = Orchestrator()
                    graph = orchestrator.build_graph()
                    
                    initial_state = {
                        "business_id": b.name,
                        "website_url": b.website
                    }
                    
                    result = run_async(graph.ainvoke(initial_state))
                    
                    st.success(f"Audit Complete! Grade: {result['maturity_grade']}")
                    
                    # Dashboard UI Upgrades: Tabs and Metrics
                    tab_metrics, tab_seo, tab_recs = st.tabs(["Technical Metrics", "SEO Audit", "AI Recommendations"])
                    
                    with tab_metrics:
                        website_audit = result.get('audit_results', {}).get('website_audit', {})
                        score = website_audit.get('website_score', 0)
                        st.metric("Technical Performance Score", f"{score}/100")
                        st.progress(score / 100.0)
                        st.json(website_audit.get('metrics', {}))
                        
                    with tab_seo:
                        seo_audit = result.get('audit_results', {}).get('seo_audit', {})
                        seo_score = seo_audit.get('seo_score', 0)
                        st.metric("SEO Health Score", f"{seo_score}/100")
                        st.progress(seo_score / 100.0)
                        st.json(seo_audit)
                        
                    with tab_recs:
                        raw_recs = result.get('recommendations', '[]')
                        if isinstance(raw_recs, str):
                            import re as _re
                            m = _re.search(r'\[.*?\]', raw_recs, _re.DOTALL)
                            try:
                                parsed_recs = json.loads(m.group()) if m else []
                            except Exception:
                                parsed_recs = []
                        else:
                            parsed_recs = raw_recs if isinstance(raw_recs, list) else []

                        st.json(parsed_recs)

                    # Display the drafted email
                    draft_email = result.get('draft_email')
                    html_email_draft = None
                    
                    if draft_email:
                        html_email_draft = f"""
                        <html>
                          <body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #333; line-height: 1.6; padding: 20px; background-color: #f4f7f6;">
                            <div style="max-width: 600px; margin: 0 auto; background: #ffffff; padding: 40px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.05);">
                              <div style="text-align: center; margin-bottom: 30px;">
                                <h1 style="color: #002060; margin: 0; font-size: 24px;">Digital Audit Complete</h1>
                              </div>
                              <p style="font-size: 16px; color: #444;">{draft_email.replace(chr(10), '<br>')}</p>
                              <div style="text-align: center; margin-top: 40px;">
                                <a href="#" style="background-color: #002060; color: #ffffff; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; display: inline-block;">Schedule Your Review</a>
                              </div>
                              <hr style="border: none; border-top: 1px solid #eaeaea; margin: 30px 0;">
                              <p style="font-size: 12px; color: #999; text-align: center;">Low2High Digital Agency</p>
                            </div>
                          </body>
                        </html>
                        """
                        st.subheader("✉️ Automated Outreach Drafts")
                        with st.expander("Preview HTML Email Design"):
                            st.html(html_email_draft)
                        st.text_area("Plain Text Version", draft_email, height=150)
                        
                        import urllib.parse
                        import re
                        if b.phone:
                            clean_phone = re.sub(r'\D', '', b.phone)
                            encoded_msg = urllib.parse.quote(draft_email)
                            wa_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"
                            st.link_button("💬 Send via WhatsApp", wa_link)

                    # Store the results in the database
                    with st.spinner("Saving audit to database..."):
                        run_async(save_audit_to_db(b.id, result.get('maturity_grade', 'N/A'), result))
                        st.success(f"💾 Audit data successfully saved to the database for {b.name}.")
                        
                    # Attempt to send the email directly
                    if draft_email and b.email:
                        mailer = AutoMailer()
                        subject = f"Your Digital Growth Ideas - {b.name}"
                        
                        with st.spinner("Sending HTML Email..."):
                            success = mailer.send_audit_email(
                                recipient_email=b.email,
                                subject=subject,
                                body_text=draft_email,
                                html_content=html_email_draft
                            )
                            
                        if success:
                            st.success(f"✅ Automated HTML email successfully sent to {b.email}!")
                        else:
                            st.warning(f"⚠️ Email could not be sent to {b.email}. Please ensure your SMTP credentials are set in the .env file.")
                    elif not b.email:
                        st.warning("⚠️ This business has no email on file. Outreach must be done manually.")

import re
import json
from fpdf import FPDF
from datetime import datetime

LEFT_M = 15
RIGHT_M = 15
TOP_M = 15

class PDFGenerator:
    def __init__(self):
        pass

    def _extract_json_recommendations(self, raw: str) -> list:
        if not raw:
            return []
        match = re.search(r'\[.*?\]', raw, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
        cleaned = raw
        for marker in ['```json', '```']:
            cleaned = cleaned.replace(marker, '')
        cleaned = cleaned.strip()
        try:
            return json.loads(cleaned)
        except Exception as e:
            print(f"Warning: Could not parse recommendations JSON: {e}")
            return []

    def _new_pdf(self):
        pdf = FPDF()
        pdf.set_margins(left=LEFT_M, top=TOP_M, right=RIGHT_M)
        pdf.set_auto_page_break(auto=True, margin=20)
        return pdf

    def _add_cover_page(self, pdf, business_id, grade):
        pdf.add_page()
        pdf.set_fill_color(0, 32, 96) # Deep Blue
        pdf.rect(0, 0, 210, 297, 'F')
        
        pdf.set_text_color(255, 255, 255)
        
        # Title
        pdf.set_y(80)
        pdf.set_font("Helvetica", "B", 36)
        pdf.cell(0, 20, "DIGITAL MATURITY", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.cell(0, 20, "AUDIT REPORT", align="C", new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(20)
        
        # Business Name
        pdf.set_font("Helvetica", "", 18)
        pdf.cell(0, 10, "Prepared exclusively for:", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 24)
        pdf.cell(0, 15, business_id, align="C", new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(30)
        
        # Grade Shield
        pdf.set_font("Helvetica", "", 16)
        pdf.cell(0, 10, "Final Maturity Grade", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 48)
        pdf.cell(0, 25, grade, align="C", new_x="LMARGIN", new_y="NEXT")
        
        # Date Footer
        pdf.set_y(-50)
        pdf.set_font("Helvetica", "I", 12)
        pdf.set_text_color(200, 200, 200)
        pdf.cell(0, 10, f"Generated on {datetime.now().strftime('%B %d, %Y')}", align="C", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "B", 16)
        pdf.set_text_color(255, 255, 255)
        pdf.cell(0, 10, "Low2High Digital Agency Platform", align="C", new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "", 10)
        pdf.set_text_color(150, 150, 150)
        pdf.cell(0, 10, "CONFIDENTIAL & PROPRIETARY", align="C")

    def generate_pdf(self, state: dict, output_path: str) -> str:
        business_id = state.get('business_id', 'Unknown')
        print(f"[PDF Generator] Building PDF for {business_id}...")

        recs = state.get('recommendations', [])
        if isinstance(recs, str):
            recs = self._extract_json_recommendations(recs)

        overall_health = state['audit_results'].get('overall_health', 0)
        maturity_grade = state.get('maturity_grade', 'N/A')
        metrics = state['audit_results'].get('website_audit', {}).get('metrics', {})
        seo = state['audit_results'].get('seo_audit', {})

        pdf = self._new_pdf()
        
        # 1. Cover Page
        self._add_cover_page(pdf, business_id, maturity_grade)
        
        # 2. Content Pages
        pdf.add_page()
        pdf.set_text_color(0, 0, 0)
        
        W = pdf.epw
        LW = 75              
        VW = W - LW          

        # ── Header ────────────────────────────────────
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(0, 32, 96)
        pdf.cell(W, 12, "Executive Summary", new_x="LMARGIN", new_y="NEXT")
        pdf.set_line_width(0.5)
        pdf.set_draw_color(0, 32, 96)
        pdf.line(LEFT_M, pdf.get_y(), LEFT_M + W, pdf.get_y())
        pdf.ln(8)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Helvetica", "", 12)
        summary_text = (
            f"This report details the technical, SEO, and strategic digital health of {business_id}. "
            f"The overall health score is {overall_health} out of 100."
        )
        pdf.multi_cell(W, 6, summary_text, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(10)

        # ── Section helper ────────────────────────────────────────────
        def section_title(title):
            pdf.set_fill_color(240, 244, 250)
            pdf.set_text_color(0, 32, 96)
            pdf.set_font("Helvetica", "B", 14)
            pdf.cell(W, 10, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True, border="L")
            pdf.set_text_color(0, 0, 0)
            pdf.ln(4)

        def kv_row(label, value):
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(LW, 8, label, border="B")
            pdf.set_font("Helvetica", "", 11)
            # Use color for boolean values
            if str(value).lower() in ["true", "yes"]:
                pdf.set_text_color(34, 139, 34) # Green
            elif str(value).lower() in ["false", "no"]:
                pdf.set_text_color(220, 20, 60) # Red
            else:
                pdf.set_text_color(0, 0, 0)
            pdf.cell(VW, 8, str(value), new_x="LMARGIN", new_y="NEXT", border="B")
            pdf.set_text_color(0, 0, 0)

        # ── Technical Metrics ─────────────────────────────────────────
        section_title("Technical Performance")
        kv_row("SSL/HTTPS Security",    metrics.get("ssl_enabled", "N/A"))
        kv_row("Mobile Responsiveness", metrics.get("mobile_responsive", "N/A"))
        kv_row("Page Load Time",        str(metrics.get("load_time_ms", "N/A")) + " ms")
        kv_row("Broken Links Count",    metrics.get("broken_links", "N/A"))
        kv_row("Lead Generation Form",  metrics.get("contact_form_present", "N/A"))
        kv_row("Live Chat Widget",      metrics.get("chat_widget_present", "N/A"))
        kv_row("Online Booking Engine", metrics.get("online_booking_present", "N/A"))
        kv_row("Security Headers",      metrics.get("security_headers_present", "False"))
        kv_row("Branding (Favicon)",    metrics.get("has_favicon", "False"))
        kv_row("Charset (UTF-8)",       metrics.get("has_charset_utf8", "False"))
        kv_row("Accessibility (Aria)",  metrics.get("accessibility_aria_labels", "False"))
        pdf.ln(10)

        # ── Marketing Technology ──────────────────────────────────────
        section_title("Marketing Technology & Analytics")
        kv_row("Google Analytics (GA4/UA)", metrics.get("has_google_analytics", "False"))
        kv_row("Facebook/Meta Pixel",       metrics.get("has_facebook_pixel", "False"))
        pdf.ln(10)

        # ── SEO Audit ─────────────────────────────────────────────────
        section_title("Search Engine Optimization (SEO)")
        kv_row("Meta Title Tag",       seo.get("meta_title_present", "N/A"))
        kv_row("Meta Description Tag", seo.get("meta_desc_present", "N/A"))
        kv_row("Primary H1 Header",    seo.get("h1_present", "N/A"))
        kv_row("Supporting H2/H3",     seo.get("h2_or_h3_present", "False"))
        kv_row("Canonical Tag",        seo.get("has_canonical", "False"))
        kv_row("Open Graph (Social)",  seo.get("has_open_graph", "False"))
        kv_row("Advanced Schema (JSON-LD)", seo.get("has_schema_markup", "False"))
        kv_row("Homepage Word Count",  seo.get("word_count", "0"))
        kv_row("Overall SEO Score",    seo.get("seo_score", "N/A"))
        pdf.ln(10)
        
        # ── Extracted Contact & Social ────────────────────────────────
        social = state['audit_results'].get('social_audit', {})
        section_title("Public Contact & Social Profiles")
        
        emails = metrics.get("extracted_emails", [])
        if emails:
            kv_row("Extracted Emails", ", ".join(emails))
        else:
            kv_row("Extracted Emails", "None found")
            
        kv_row("Facebook URL",  social.get("facebook_url", "Not Found") or "Not Found")
        kv_row("Instagram URL", social.get("instagram_url", "Not Found") or "Not Found")
        kv_row("LinkedIn URL",  social.get("linkedin_url", "Not Found") or "Not Found")
        kv_row("Twitter/X URL", social.get("twitter_url", "Not Found") or "Not Found")
        pdf.ln(10)

        # ── AI Recommendations ────────────────────────────────────────
        if pdf.get_y() > 220:
            pdf.add_page()
            
        section_title("Strategic Roadmap (AI Generated)")
        
        if not recs:
            pdf.set_font("Helvetica", "I", 11)
            pdf.cell(W, 10, "No actionable recommendations found.", new_x="LMARGIN", new_y="NEXT")
        
        for i, rec in enumerate(recs, 1):
            if pdf.get_y() > 250:
                pdf.add_page()
            
            # Recommendation Box
            pdf.set_fill_color(248, 250, 252)
            pdf.set_draw_color(200, 210, 225)
            
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(0, 32, 96)
            weakness = str(rec.get('weakness', ''))
            pdf.multi_cell(W, 8, f"{i}. Identified Area: {weakness}",
                           fill=True, border="TLR", new_x="LMARGIN", new_y="NEXT")
                           
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Helvetica", "", 10)
            solution = str(rec.get('solution', '')).replace('\n', ' ')
            pdf.multi_cell(W, 6, f"Solution: {solution}",
                           fill=True, border="LR", new_x="LMARGIN", new_y="NEXT")
                           
            pdf.set_font("Helvetica", "I", 10)
            impact = str(rec.get('impact', '')).replace('\n', ' ')
            
            # Use priority and effort if available
            priority = str(rec.get('priority', 'Medium'))
            effort = str(rec.get('effort', 'Medium'))
            
            pdf.multi_cell(W, 6, f"Business Impact: {impact}",
                           fill=True, border="LR", new_x="LMARGIN", new_y="NEXT")
            
            # Bottom row with priority and effort
            pdf.set_font("Helvetica", "B", 9)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(W/2, 6, f"Priority: {priority}", fill=True, border="BL", align="L")
            pdf.cell(W/2, 6, f"Effort: {effort}", fill=True, border="BR", align="R", new_x="LMARGIN", new_y="NEXT")
            pdf.set_text_color(0, 0, 0)
            
            pdf.ln(5)

        # ── Footer Overlay on all pages ──────────────────────────────
        for page_no in range(2, pdf.page_no() + 1):
            pdf.page = page_no
            pdf.set_y(-15)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(W, 10, f"Confidential Report | Generated by Low2High Platform | Page {page_no-1}", align="C")

        pdf.output(output_path)
        print(f"[PDF Generator] Premium PDF saved to {output_path}")
        return output_path

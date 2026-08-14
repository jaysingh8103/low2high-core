from typing import Dict, Any
import httpx
from bs4 import BeautifulSoup
import time

class WebsiteAuditAgent:
    async def run_audit(self, business_id: str, website_url: str) -> Dict[str, Any]:
        if not website_url:
            website_url = "https://example.com"
        
        if not website_url.startswith("http"):
            website_url = "https://" + website_url
            
        print(f"[{business_id}] Auditing website via HTTPX: {website_url}")
        
        metrics = {
            "ssl_enabled": False,
            "mobile_responsive": True, # Assume true for modern web
            "load_time_ms": 0,
            "broken_links": 0,
            "contact_form_present": False,
            "chat_widget_present": False,
            "online_booking_present": False,
            "has_google_analytics": False,
            "has_facebook_pixel": False,
            "extracted_emails": [],
            "has_favicon": False,
            "has_charset_utf8": False,
            "accessibility_aria_labels": False,
            "security_headers_present": False
        }
        
        html_content = ""
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient(verify=False, timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(
                    website_url, 
                    headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
                )
                end_time = time.time()
                
                metrics["load_time_ms"] = int((end_time - start_time) * 1000)
                
                if str(resp.url).startswith("https"):
                    metrics["ssl_enabled"] = True
                    
                # Security Headers Check
                headers = {k.lower(): v for k, v in resp.headers.items()}
                if 'strict-transport-security' in headers or 'x-content-type-options' in headers or 'x-frame-options' in headers:
                    metrics["security_headers_present"] = True
                    
                html_content = resp.text
                
                soup = BeautifulSoup(html_content, "html.parser")
                
                # Check for contact forms
                forms = soup.find_all("form")
                for form in forms:
                    action = form.get("action", "").lower()
                    id_attr = form.get("id", "").lower()
                    class_attr = " ".join(form.get("class", [])).lower()
                    combined = action + id_attr + class_attr
                    if "contact" in combined or "message" in combined:
                        metrics["contact_form_present"] = True
                        break
                        
                # Check for chat widgets (iframes or script variables)
                iframes = soup.find_all("iframe")
                chat_keywords = ["intercom", "tawk", "zendesk", "drift", "chat"]
                for iframe in iframes:
                    src = iframe.get("src", "").lower()
                    if any(k in src for k in chat_keywords):
                        metrics["chat_widget_present"] = True
                        break
                        
                # Scripts (Chat widgets & Pixels)
                scripts = soup.find_all("script")
                for script in scripts:
                    src = script.get("src", "").lower()
                    if any(k in src for k in chat_keywords):
                        metrics["chat_widget_present"] = True
                    # Analytics & Pixels
                    if "google-analytics.com" in src or "googletagmanager.com" in src:
                        metrics["has_google_analytics"] = True
                    if "connect.facebook.net" in src and "fbevents.js" in src:
                        metrics["has_facebook_pixel"] = True
                        
                # Check inline script text for analytics tags
                for script in scripts:
                    content = script.string or ""
                    if "G-" in content or "UA-" in content or "gtag(" in content:
                        metrics["has_google_analytics"] = True
                    if "fbq(" in content:
                        metrics["has_facebook_pixel"] = True

                # Check for mobile viewport
                viewport = soup.find("meta", attrs={"name": "viewport"})
                if viewport and "width=device-width" in viewport.get("content", "").lower():
                    metrics["mobile_responsive"] = True
                else:
                    metrics["mobile_responsive"] = False
                    
                # Check for Favicon
                favicon = soup.find("link", rel=lambda r: r and "icon" in r.lower())
                if favicon:
                    metrics["has_favicon"] = True
                    
                # Check for Charset UTF-8
                charset_meta = soup.find("meta", charset=True)
                content_type_meta = soup.find("meta", attrs={"http-equiv": lambda h: h and h.lower() == "content-type"})
                if (charset_meta and "utf-8" in charset_meta.get("charset", "").lower()) or \
                   (content_type_meta and "utf-8" in content_type_meta.get("content", "").lower()):
                    metrics["has_charset_utf8"] = True
                    
                # Basic Accessibility Check (aria-label on interactive elements)
                buttons_or_links = soup.find_all(['button', 'a'])
                for el in buttons_or_links:
                    if el.has_attr('aria-label') or el.has_attr('role'):
                        metrics["accessibility_aria_labels"] = True
                        break

                # Extract Emails using Regex
                import re
                emails = set()
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                # Search in mailto links
                for a in soup.find_all('a', href=True):
                    if a['href'].startswith('mailto:'):
                        email = a['href'].replace('mailto:', '').split('?')[0].strip()
                        if re.match(email_pattern, email):
                            emails.add(email.lower())
                # Search in raw text
                text_emails = re.findall(email_pattern, soup.get_text())
                for e in text_emails:
                    # filter out common false positive image extensions like @2x.png
                    if not any(e.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp']):
                        emails.add(e.lower())
                        
                metrics["extracted_emails"] = list(emails)[:3] # Keep top 3

        except Exception as e:
            print(f"[{business_id}] HTTPX error: {e}")
            metrics["load_time_ms"] = 10000 # Timeout penalty
            
        # Calculate a basic score based on metrics
        score = 100
        if not metrics["ssl_enabled"]: score -= 15
        if not metrics["mobile_responsive"]: score -= 15
        if metrics["load_time_ms"] > 3000: score -= 10
        if not metrics["contact_form_present"] and not metrics["extracted_emails"]: score -= 10
        if not metrics["has_google_analytics"]: score -= 5
        if not metrics["has_favicon"]: score -= 5
        if not metrics["has_charset_utf8"]: score -= 5
        if not metrics["accessibility_aria_labels"]: score -= 5
        
        return {
            "business_id": business_id,
            "website_score": max(0, score),
            "metrics": metrics,
            "html_content": html_content # Passed down to SEO agent
        }

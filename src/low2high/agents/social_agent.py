from typing import Dict, Any
from bs4 import BeautifulSoup
import re

class SocialAgent:
    def run_audit(self, business_id: str, html_content: str) -> Dict[str, Any]:
        print(f"[{business_id}] Running Social Presence Audit...")
        
        metrics = {
            "facebook_url": None,
            "instagram_url": None,
            "linkedin_url": None,
            "twitter_url": None,
            "youtube_url": None
        }
        
        if not html_content:
            return metrics
            
        soup = BeautifulSoup(html_content, "html.parser")
        links = soup.find_all("a", href=True)
        
        for link in links:
            href = link["href"].lower()
            if "facebook.com" in href and not metrics["facebook_url"]: metrics["facebook_url"] = link["href"]
            if "instagram.com" in href and not metrics["instagram_url"]: metrics["instagram_url"] = link["href"]
            if "linkedin.com" in href and not metrics["linkedin_url"]: metrics["linkedin_url"] = link["href"]
            if ("twitter.com" in href or "x.com" in href) and not metrics["twitter_url"]: metrics["twitter_url"] = link["href"]
            if "youtube.com" in href and not metrics["youtube_url"]: metrics["youtube_url"] = link["href"]
            
        return metrics

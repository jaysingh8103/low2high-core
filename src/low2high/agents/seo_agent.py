from typing import Dict, Any
from bs4 import BeautifulSoup

class SEOAgent:
    def run_audit(self, business_id: str, html_content: str) -> Dict[str, Any]:
        print(f"[{business_id}] Running SEO Audit...")
        
        metrics = {
            "meta_title_present": False,
            "meta_desc_present": False,
            "h1_present": False,
            "h2_or_h3_present": False,
            "has_canonical": False,
            "has_open_graph": False,
            "images_missing_alt": 0,
            "has_schema_markup": False,
            "word_count": 0,
            "seo_score": 100
        }
        
        if not html_content:
            metrics["seo_score"] = 0
            return metrics
            
        soup = BeautifulSoup(html_content, "html.parser")
        
        # Title
        title = soup.find("title")
        if title and title.text.strip():
            metrics["meta_title_present"] = True
        else:
            metrics["seo_score"] -= 20
            
        # Meta Description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            metrics["meta_desc_present"] = True
        else:
            metrics["seo_score"] -= 20
            
        # H1
        h1 = soup.find("h1")
        if h1 and h1.text.strip():
            metrics["h1_present"] = True
        else:
            metrics["seo_score"] -= 20
            
        # H2/H3
        h2 = soup.find("h2")
        h3 = soup.find("h3")
        if (h2 and h2.text.strip()) or (h3 and h3.text.strip()):
            metrics["h2_or_h3_present"] = True
        else:
            metrics["seo_score"] -= 10
            
        # Canonical Tag
        canonical = soup.find("link", rel="canonical")
        if canonical and canonical.get("href"):
            metrics["has_canonical"] = True
        else:
            metrics["seo_score"] -= 5
            
        # Open Graph Tags (Social)
        og_title = soup.find("meta", property="og:title")
        og_image = soup.find("meta", property="og:image")
        if og_title or og_image:
            metrics["has_open_graph"] = True
        else:
            metrics["seo_score"] -= 5
            
        # Images without ALT
        images = soup.find_all("img")
        missing_alt = 0
        for img in images:
            if not img.get("alt"):
                missing_alt += 1
                
        metrics["images_missing_alt"] = missing_alt
        
        # Schema Markup (JSON-LD)
        schema_tags = soup.find_all("script", type="application/ld+json")
        if schema_tags:
            metrics["has_schema_markup"] = True
            
        # Word Count
        text = soup.get_text(separator=' ', strip=True)
        metrics["word_count"] = len(text.split())
        
        # Adjust score based on missing alt tags
        if missing_alt > 0:
            metrics["seo_score"] -= min(30, missing_alt * 5)
            
        metrics["seo_score"] = max(0, metrics["seo_score"])
        return metrics

import re
import math
from bs4 import BeautifulSoup

class AppContextDetector:
    def __init__(self):
        # Map raw XML corpus categories to our standardized Phase 3B/4B Pipeline App Types
        self.category_map = {
            "Health": "Healthcare",
            "Science": "Healthcare",
            "Shopping": "E-Commerce",
            "Business": "Commerce", # Most business in this dataset leans to e-commerce/corporate
            "Society": "Social Media",
            "Recreation": "Social Media",
            "Kids and Teens": "Education",
            "Reference": "Education",
            "Arts": "General",
            "Games": "General",
            "Home": "General",
            "Computers": "General",
            "News": "General",
            "Regional": "General",
            "Sports": "General"
        }
        
        # Keyword frequency targets for fallback ML-less detection
        self.keywords = {
            "Healthcare": ["patient", "diagnosis", "treatment", "medical", "doctor", "health", "hipaa", "clinic", "therapy", "symptoms"],
            "E-Commerce": ["cart", "checkout", "shipping", "refund", "buyer", "seller", "order", "purchase", "store", "merchandise"],
            "Finance": ["bank", "loan", "credit", "financial", "investment", "tax", "banking", "lending", "mortgage", "transaction"],
            "Social Media": ["profile", "friends", "post", "share", "messaging", "followers", "timeline", "social", "community", "chat"],
            "Education": ["student", "course", "teacher", "school", "academic", "university", "grades", "curriculum", "learning", "class"],
            "SaaS": ["subscription", "tenant", "saas", "dashboard", "enterprise", "api", "integration", "software", "deployment"]
        }

    def detect_context(self, xml_content):
        # 1. Try to extract exact metadata from <POLICY> tag
        match = re.search(r'<policy[^>]*website_category\s*=\s*["\']([^"\']+)["\']', xml_content, re.IGNORECASE)
        if match:
            raw_cat = match.group(1).strip()
            return {
                "App_Context": raw_cat,
                "Confidence": 100.0,
                "Method": "Metadata_Extraction",
                "Raw_Category": raw_cat
            }
                
        # 2. Fallback to Keyword Heuristic Detection
        soup = BeautifulSoup(xml_content, 'html.parser')
        text = soup.get_text(separator=" ").lower()
        words = re.findall(r'\b\w+\b', text)
        total_words = len(words)
        
        if total_words == 0:
            return {"App_Context": "Unconfirmed", "Confidence": 0.0, "Method": "Keyword_Detection", "Raw_Category": "None"}
            
        scores = {}
        for app_type, kw_list in self.keywords.items():
            count = sum(1 for w in words if w in kw_list)
            # Density per 100 words (normalized)
            density = (count / total_words) * 100 if total_words > 0 else 0
            scores[app_type] = density
            
        best_match = max(scores, key=scores.get)
        best_density = scores[best_match]
        
        # Calculate heuristic confidence:
        # A density of >= 0.5 keywords per 100 words is considered highly confident (100%) for privacy texts.
        confidence = min(100.0, (best_density / 0.5) * 100.0)
        
        if confidence > 60.0:
            return {
                "App_Context": best_match,
                "Confidence": confidence,
                "Method": "Keyword_Detection",
                "Raw_Category": "None"
            }
        else:
            return {
                "App_Context": "Unconfirmed",
                "Confidence": confidence,
                "Method": "Keyword_Detection",
                "Raw_Category": "None"
            }

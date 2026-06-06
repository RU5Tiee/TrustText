import json
import random

class NarrativeGenerator:
    def __init__(self, patterns_path):
        with open(patterns_path, 'r') as f:
            self.patterns = json.load(f)
            
        self.app_focus_map = {
            "Healthcare": "patient information and sensitive health data",
            "Banking": "financial records and transaction information",
            "Finance": "financial records and transaction information",
            "E-Commerce": "customer purchase history and order records",
            "Social Media": "user-generated content and behavioral activity",
            "Education": "student records and educational information",
            "SaaS": "business records and customer account information",
            "General": "general consumer personal data",
            "Unconfirmed": "personal data"
        }

    def generate(self, category, risk_level, app_type):
        app_focus = self.app_focus_map.get(app_type, "personal data")
        
        # Fallback to HIGH if CRITICAL not explicitly in patterns
        safe_risk = risk_level if risk_level in self.patterns.get(category, {}) else "HIGH"
        
        candidates = self.patterns.get(category, {}).get(safe_risk, [
            f"The clause addresses {category} but requires attention regarding {app_focus}."
        ])
        
        pattern = random.choice(candidates)
        return pattern.replace("{cat}", category.lower()).replace("{app_focus}", app_focus)
import json

class SlotFiller:
    def __init__(self, library_path, legal_lookup):
        self.legal_lookup = legal_lookup
        with open(library_path, 'r') as f:
            self.templates = json.load(f)
            
        self.tmpl_map = {}
        for t in self.templates:
            # Map SEVERE to CRITICAL to match new schema
            rl = "CRITICAL" if t["Risk_Level"] == "SEVERE" else t["Risk_Level"]
            self.tmpl_map[(t["Category"], rl)] = t

    def fill_normal(self, category, risk_level):
        safe_risk = risk_level
        tmpl = self.tmpl_map.get((category, safe_risk))
        if not tmpl:
            # Fallback
            return {
                "DeveloperAction": "Audit underlying systems.",
                "PrivacyTeamAction": "Review policy alignment.",
                "ImmediateRemediation": "Update clause for clarity.",
                "LongTermRemediation": "Implement governance checks."
            }
            
        refs = self.legal_lookup.get_references(category)
        
        return {
            "DeveloperAction": tmpl.get("DeveloperAction", tmpl.get("Developer_Action", "N/A")),
            "PrivacyTeamAction": tmpl.get("PrivacyTeamAction", tmpl.get("Privacy_Team_Action", "N/A")),
            "ImmediateRemediation": tmpl.get("ImmediateRemediation", tmpl.get("Immediate_Remediation", "N/A")),
            "LongTermRemediation": tmpl.get("LongTermRemediation", tmpl.get("Long_Term_Remediation", "N/A")),
            "DPDP_References": refs["DPDPControls"],
            "GDPR_References": refs["GDPRArticles"]
        }
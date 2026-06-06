import os
import json
import csv
import re

class RiskScorerB:
    def __init__(self, mapping_csv_path):
        self.mapping_csv_path = mapping_csv_path
        self.legal_kb = self._build_knowledge_base()
        
        self.risk_levels = ["LOW", "MEDIUM", "HIGH", "SEVERE", "REVIEW"]
        
        # Base Risk Matrix mapping
        self.base_risk_map = {
            "Data Security": "MEDIUM",
            "Data Retention": "LOW",
            "Third Party Sharing/Collection": "MEDIUM",
            "First Party Collection/Use": "LOW",
            "User Choice/Control": "LOW",
            "User Access, Edit and Deletion": "LOW",
            "Policy Change": "LOW",
            "International and Specific Audiences": "MEDIUM",
            "Do Not Track": "LOW",
            "Other": "LOW"
        }
        
    def _build_knowledge_base(self):
        kb = {}
        # Parse the alignment CSV. If there are multiple mappings for the same category,
        # we will store the first one encountered that has valid DPDP/GDPR details.
        if os.path.exists(self.mapping_csv_path):
            with open(self.mapping_csv_path, 'r', encoding='utf-8', errors='ignore') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cat = row.get("OPP_Category", "").strip()
                    if cat and cat not in kb and cat != "NONE" and cat != "UNMAPPED":
                        kb[cat] = {
                            "section": row.get("DPDP_Section", "N/A").strip() or "N/A",
                            "rule": row.get("DPDP_Rule", "N/A").strip() or "N/A",
                            "schedule": row.get("DPDP_Schedule", "N/A").strip() or "N/A",
                            "control_id": row.get("DPDP_Control", "N/A").strip() or "N/A",
                            "gdpr_reference": row.get("GDPR_Article", "N/A").strip() or "N/A"
                        }
        return kb

    def _bump_tier(self, current_tier, bumps=1):
        if current_tier == "REVIEW":
            return "REVIEW"
        try:
            idx = self.risk_levels.index(current_tier)
            new_idx = min(idx + bumps, len(self.risk_levels) - 1)
            # The last normal tier is SEVERE. Beyond that, or if manually set, is REVIEW.
            # However, the tier bumping logic explicitly states:
            # LOW -> MEDIUM -> HIGH -> SEVERE -> REVIEW
            return self.risk_levels[new_idx]
        except ValueError:
            return "REVIEW"

    def fix_article_grammar(self, text):
        # Fixes 'a' vs 'an' in generated rationales
        def replacer(match):
            article = match.group(1).lower()
            word = match.group(2)
            # Preserve capitalization of article if it was at start
            is_cap = match.group(1)[0].isupper()
            new_article = "an" if word.lower().startswith(tuple('aeiou')) else "a"
            if is_cap:
                new_article = new_article.capitalize()
            return f"{new_article} {word}"
        return re.sub(r'\b(a|an)\s+([a-zA-Z]+)', replacer, text, flags=re.IGNORECASE)

    # ---------------- Escalation Logic ----------------
    def escalate_vague_retention(self, text):
        keywords = ["indefinite", "forever", "perpetual", "as long as necessary", "no limit"]
        return any(k in text.lower() for k in keywords)

    def escalate_children_data(self, text):
        keywords = ["under 13", "children", "minor", "kids"]
        return any(k in text.lower() for k in keywords)

    def escalate_unnamed_third_parties(self, text):
        keywords = ["any third party", "unrestricted", "all third parties"]
        return any(k in text.lower() for k in keywords)

    def escalate_no_user_control(self, text):
        keywords = ["cannot opt out", "no choice", "mandatory", "must accept"]
        return any(k in text.lower() for k in keywords)

    def evaluate(self, clause_text, predicted_category, confidence, app_type):
        escalations = []
        
        # 1. Base Risk
        current_risk = self.base_risk_map.get(predicted_category, "LOW")
        
        # Context-Sensitivity (Utility, Finance, Health, Social, E-commerce, General)
        if app_type in ["Finance", "Health"]:
            current_risk = self._bump_tier(current_risk, 1)
        elif app_type in ["Social", "E-commerce"] and predicted_category == "Third Party Sharing/Collection":
            current_risk = self._bump_tier(current_risk, 1)

        # 2. Apply Escalations
        if predicted_category == "Data Retention" and self.escalate_vague_retention(clause_text):
            escalations.append("VAGUE_RETENTION")
            current_risk = self._bump_tier(current_risk, 1)
            
        if predicted_category == "International and Specific Audiences" and self.escalate_children_data(clause_text):
            escalations.append("CHILDREN_DATA")
            current_risk = self._bump_tier(current_risk, 1)
            
        if predicted_category == "Third Party Sharing/Collection" and self.escalate_unnamed_third_parties(clause_text):
            escalations.append("UNNAMED_THIRD_PARTIES")
            current_risk = self._bump_tier(current_risk, 1)
            
        if predicted_category == "User Choice/Control" and self.escalate_no_user_control(clause_text):
            escalations.append("NO_USER_CONTROL")
            current_risk = self._bump_tier(current_risk, 1)

        # 3. Reliability Constraint
        if confidence < 0.70:
            current_risk = "REVIEW"

        # 4. Legal Anchors Lookup (Mapping B)
        anchors = self.legal_kb.get(predicted_category, {
            "section": "N/A", "rule": "N/A", "schedule": "N/A", "control_id": "N/A", "gdpr_reference": "N/A"
        })

        # 5. Grammar Corrected Rationale
        rationale = f"This clause is classified as a {predicted_category} statement. "
        if escalations:
            rationale += f"It triggered an escalation due to {', '.join(escalations)}. "
        rationale += f"The evaluated risk is {current_risk} for a {app_type} context."
        
        rationale = self.fix_article_grammar(rationale)

        return {
            "clause": clause_text,
            "app_context": app_type,
            "final_risk": current_risk,
            "legal_anchors": {
                "section": anchors["section"],
                "rule": anchors["rule"],
                "schedule": anchors["schedule"],
                "control_id": anchors["control_id"]
            },
            "escalations": escalations,
            "gdpr_reference": anchors["gdpr_reference"],
            "rationale": rationale
        }

if __name__ == "__main__":
    # Quick Test
    mapping_path = r"D:\TrustText#2\Phase3_Classifier\Classification_schema\DPDP_GDPR_OPP_Alignment.csv"
    scorer = RiskScorerB(mapping_path)
    
    test_clause = "We may retain your data for as long as necessary."
    res = scorer.evaluate(test_clause, "Data Retention", 0.95, "Health")
    print(json.dumps(res, indent=4))

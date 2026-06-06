import csv

class LegalLookup:
    def __init__(self, mapping_csv_path):
        self.kb = {}
        with open(mapping_csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cat = row.get("OPP_Category", "").strip()
                if cat and cat != "NONE" and cat != "UNMAPPED":
                    if cat not in self.kb:
                        self.kb[cat] = {
                            "DPDPSections": [], "DPDPRules": [], "DPDPSchedules": [],
                            "DPDPControls": [], "GDPRArticles": [], "GDPRControls": [], "GDPRPrinciples": []
                        }
                    
                    if row.get("DPDP_Section"): self.kb[cat]["DPDPSections"].append(row.get("DPDP_Section"))
                    if row.get("DPDP_Rule"): self.kb[cat]["DPDPRules"].append(row.get("DPDP_Rule"))
                    if row.get("DPDP_Schedule"): self.kb[cat]["DPDPSchedules"].append(row.get("DPDP_Schedule"))
                    if row.get("DPDP_Control"): self.kb[cat]["DPDPControls"].append(row.get("DPDP_Control"))
                    if row.get("GDPR_Article"): self.kb[cat]["GDPRArticles"].append(row.get("GDPR_Article"))
                    if row.get("GDPR_Control"): self.kb[cat]["GDPRControls"].append(row.get("GDPR_Control"))
                    if row.get("GDPR_Principle"): self.kb[cat]["GDPRPrinciples"].append(row.get("GDPR_Principle"))

        # Deduplicate
        for cat in self.kb:
            for key in self.kb[cat]:
                self.kb[cat][key] = list(set([x for x in self.kb[cat][key] if x]))

    def get_references(self, category):
        return self.kb.get(category, {
            "DPDPSections": [], "DPDPRules": [], "DPDPSchedules": [],
            "DPDPControls": [], "GDPRArticles": [], "GDPRControls": [], "GDPRPrinciples": []
        })

    def generate_context_summary(self, category):
        refs = self.get_references(category)
        dpdp = ", ".join(refs["DPDPControls"][:2])
        gdpr = ", ".join(refs["GDPRArticles"][:2])
        if dpdp or gdpr:
            return f"Relevant obligations associated with {category} require compliance with {dpdp} and {gdpr}."
        return f"Relevant obligations associated with {category} require adherence to standard data protection principles."
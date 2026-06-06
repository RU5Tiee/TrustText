import sys
import time
from app.core.config import settings

if settings.SLOT_FILLING_DIR not in sys.path:
    sys.path.append(settings.SLOT_FILLING_DIR)

from AppContextDetector import AppContextDetector
from NarrativeGenerator import NarrativeGenerator

from app.services.parser import ParsingService
from app.services.classifier import ClassificationService
from app.services.risk import RiskAssessmentService
from app.services.remediation import RemediationService
from app.services.legal import LegalMappingService
from app.services.report import ReportGenerationService
from app.utils.logger import logger

class TrustTextPipelineController:
    def __init__(self):
        logger.info("Initializing Pipeline Controller...")
        self.parser = ParsingService()
        self.classifier = ClassificationService()
        self.risk_scorer = RiskAssessmentService()
        
        self.legal_lookup = LegalMappingService()
        self.remediation = RemediationService(self.legal_lookup.legal_lookup)
        self.report_generator = ReportGenerationService()
        
        self.context_detector = AppContextDetector()
        self.narrative_generator = NarrativeGenerator(settings.PATTERNS_JSON)
        logger.info("All engines initialized.")
        
    def process_policy(self, file_path: str) -> dict:
        start_time = time.time()
        logger.info(f"Processing policy: {file_path}")
        
        # 1. Parsing
        doc = self.parser.parse_file(file_path)
        logger.info(f"Parsing complete. Found {len(doc['clauses'])} clauses.")
        
        if not doc["clauses"]:
            raise ValueError("No clauses found in the document.")
            
        # Context Detection
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                raw_xml = f.read()
        except Exception:
            raw_xml = doc["cleaned_text"]
        ctx_res = self.context_detector.detect_context(raw_xml)
        app_context = ctx_res["App_Context"]
        logger.info(f"Detected context: {app_context}")
        
        # 2. Classification
        clause_texts = [c["clause_text"] for c in doc["clauses"]]
        predictions = self.classifier.classify_clauses(clause_texts)
        logger.info("Classification complete.")
        
        # 3, 4, 5. Risk, Remediation, Legal
        findings = []
        for i, clause in enumerate(doc["clauses"]):
            text = clause["clause_text"]
            cat = predictions[i]["category"]
            conf = predictions[i]["confidence"]
            
            if cat == "Other" and conf > 0.80:
                continue
                
            risk_res = self.risk_scorer.evaluate_risk(text, cat, conf, app_context)
            
            if risk_res.get("Status") == "REVIEW_REQUIRED":
                finding = {
                    "clause": text,
                    "Category": cat,
                    "Confidence": conf,
                    "ReviewStatus": "REVIEW_REQUIRED",
                    "ReviewExplanation": risk_res.get("Review Note", "")
                }
            else:
                risk_level = risk_res["final_risk"]
                exp = self.narrative_generator.generate(cat, risk_level, app_context)
                ctx_sum = self.legal_lookup.legal_lookup.generate_context_summary(cat)
                filled = self.remediation.generate_remediation(cat, risk_level)
                
                finding = {
                    "clause": text,
                    "Category": cat,
                    "Confidence": conf,
                    "RiskLevel": risk_level,
                    "Explanation": exp,
                    "LegalContextSummary": ctx_sum,
                    "DPDP_References": filled["DPDP_References"],
                    "GDPR_References": filled["GDPR_References"],
                    "TriggeredRules": risk_res.get("escalations", []),
                    "DeveloperAction": filled["DeveloperAction"],
                    "PrivacyTeamAction": filled["PrivacyTeamAction"],
                    "ImmediateRemediation": filled["ImmediateRemediation"],
                    "LongTermRemediation": filled["LongTermRemediation"]
                }
                
            findings.append(finding)
            
        logger.info(f"Generated {len(findings)} findings.")
        
        # 6. Report Generation
        exec_time = round(time.time() - start_time, 2)
        report = self.report_generator.generate_report(
            policy_id=doc["policy_id"],
            title=doc["title"],
            app_context=app_context,
            execution_time=exec_time,
            quality_score=doc.get("quality_score", 0),
            clauses_processed=len(clause_texts),
            findings=findings
        )
        
        logger.info("Report generation complete.")
        return report

# Global instance initialized once at startup
pipeline_controller = None

def get_pipeline_controller():
    global pipeline_controller
    if pipeline_controller is None:
        pipeline_controller = TrustTextPipelineController()
    return pipeline_controller

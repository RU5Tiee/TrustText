import os
import sys
import time
import json
import logging
import torch
import traceback
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Any

# ==========================================
# PATH CONFIGURATION
# ==========================================
sys.path.append(r"D:\TrustText#2\Phase5_Pipeline\Parsing Engine")
sys.path.append(r"D:\TrustText#2\Phase3_Classifier\Risk_Matrix")
sys.path.append(r"D:\TrustText#2\Phase4_Remediation\Slot_filling")

from pipeline import PolicyIngestionPipeline
from AppContextDetector import AppContextDetector
from Phase3_B_RiskScorer import RiskScorerB
from LegalLookup import LegalLookup
from NarrativeGenerator import NarrativeGenerator
from SlotFiller import SlotFiller
from ComplianceFinding import NormalFinding, ReviewFinding
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# ==========================================
# CHECKPOINTER
# ==========================================
class Checkpointer:
    def __init__(self, base_dir=r"D:\TrustText#2\Phase5_Pipeline\End-to_End Pipeline\checkpoints"):
        self.base_dir = base_dir
        self.stages = ["preprocessing", "classification", "mapping", "risk", "remediation", "final"]
        for stage in self.stages:
            os.makedirs(os.path.join(self.base_dir, stage), exist_ok=True)
            
    def save(self, stage: str, policy_id: str, data: Any):
        filepath = os.path.join(self.base_dir, stage, f"{policy_id}.json")
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
    def load(self, stage: str, policy_id: str):
        filepath = os.path.join(self.base_dir, stage, f"{policy_id}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

# ==========================================
# PIPELINE CONTROLLER
# ==========================================
class TrustTextPipelineController:
    def __init__(self):
        self._setup_logging()
        self.logger.info("Initializing TrustText Pipeline Orchestrator...")
        
        self.checkpointer = Checkpointer()
        self.batch_size = 32
        
        # Load Phase 5A
        self.ingestion = PolicyIngestionPipeline()
        self.context_detector = AppContextDetector()
        
        # Load Phase 3A (CUDA Inference)
        model_dir = r"D:\TrustText#2\Phase3_Classifier\Classifier_model"
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = AutoTokenizer.from_pretrained(model_dir)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_dir).to(self.device)
        self.model.eval()
        
        self.target_labels = [
            "First Party Collection/Use", "Third Party Sharing/Collection", "User Choice/Control",
            "User Access, Edit and Deletion", "Data Retention", "Data Security", "Policy Change",
            "International and Specific Audiences", "Do Not Track", "Other"
        ]
        
        # Load Phase 4B/3B
        mapping_csv = r"D:\TrustText#2\Phase3_Classifier\Classification_schema\DPDP_GDPR_OPP_Alignment.csv"
        templates_json = r"D:\TrustText#2\Phase4_Remediation\Remediation_library\Remediation_Templates.json"
        patterns_json = r"D:\TrustText#2\Phase4_Remediation\Slot_filling\NarrativePatterns.json"
        
        self.risk_scorer = RiskScorerB(mapping_csv)
        self.legal_lookup = LegalLookup(mapping_csv)
        self.narrative = NarrativeGenerator(patterns_json)
        self.slot_filler = SlotFiller(templates_json, self.legal_lookup)
        
        self.logger.info("All engines loaded successfully.")

    def _setup_logging(self):
        log_dir = r"D:\TrustText#2\Phase5_Pipeline\End-to_End Pipeline\logs"
        os.makedirs(os.path.join(log_dir, "execution_logs"), exist_ok=True)
        os.makedirs(os.path.join(log_dir, "error_logs"), exist_ok=True)
        
        self.logger = logging.getLogger("TrustTextOrchestrator")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        fh = logging.FileHandler(os.path.join(log_dir, "execution_logs", "pipeline.log"))
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def _batch_infer(self, clauses: List[str]) -> List[Dict]:
        results = []
        for i in range(0, len(clauses), self.batch_size):
            batch = clauses[i:i + self.batch_size]
            inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=256).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            for prob in probs:
                conf = torch.max(prob).item()
                pred = self.target_labels[torch.argmax(prob).item()]
                results.append({"PredictedCategory": pred, "Confidence": conf})
        return results

    def process_policy(self, filepath: str) -> Dict:
        start_time = time.time()
        self.logger.info(f"--- Starting execution for: {filepath} ---")
        
        try:
            # 1. PHASE 5A: INGESTION
            doc = self.ingestion.process_file(filepath)
            doc_dict = doc.to_dict()
            self.checkpointer.save("preprocessing", doc.policy_id, doc_dict)
            
            # Detect Context
            ctx_res = self.context_detector.detect_context(doc.cleaned_text)
            app_context = ctx_res["App_Context"]
            self.logger.info(f"App Context Detected: {app_context}")
            
            # 2. PHASE 3A: CLASSIFICATION (CUDA BATCH)
            clause_texts = [c["clause_text"] for c in doc_dict["clauses"]]
            if not clause_texts:
                self.logger.warning(f"No clauses found for {doc.policy_id}")
                return {"status": "FAILED", "reason": "No clauses"}
                
            predictions = self._batch_infer(clause_texts)
            
            for i, c in enumerate(doc_dict["clauses"]):
                c.update(predictions[i])
            self.checkpointer.save("classification", doc.policy_id, doc_dict)
            
            # 3, 4, 5, 6, 7: ORCHESTRATE RISK, MAPPING, REMEDIATION, EXPLAINABILITY
            final_findings = []
            
            for clause in doc_dict["clauses"]:
                text = clause["clause_text"]
                cat = clause["PredictedCategory"]
                conf = clause["Confidence"]
                
                # Skip trivial "Other" classifications unless they trigger rules
                if cat == "Other" and conf > 0.80:
                    continue
                    
                risk_res = self.risk_scorer.evaluate(text, cat, conf, app_context)
                
                if "Status" in risk_res and risk_res["Status"] == "REVIEW_REQUIRED":
                    if conf < 0.60:
                        finding = ReviewFinding(Clause=text, PredictedCategory=cat, Confidence=conf, ReviewStatus="REVIEW_REQUIRED", ReviewExplanation=risk_res["Review Note"])
                    else:
                        finding = ReviewFinding(Clause=text, PredictedCategory=cat, Confidence=conf, ReviewStatus="REVIEW_REQUIRED", ReviewExplanation=risk_res["Review Note"], PotentialLegalContext=risk_res["Potential Legal Context"], PotentialReferences=risk_res["Potential References"])
                else:
                    risk_level = risk_res["final_risk"]
                    exp = self.narrative.generate(cat, risk_level, app_context)
                    ctx_sum = self.legal_lookup.generate_context_summary(cat)
                    filled = self.slot_filler.fill_normal(cat, risk_level)
                    
                    finding = NormalFinding(
                        Clause=text, Category=cat, Confidence=conf, RiskScore=0.0, RiskLevel=risk_level,
                        Explanation=exp, LegalContextSummary=ctx_sum,
                        DPDP_References=filled["DPDP_References"], GDPR_References=filled["GDPR_References"],
                        TriggeredRules=risk_res.get("escalations", []),
                        DeveloperAction=filled["DeveloperAction"], PrivacyTeamAction=filled["PrivacyTeamAction"],
                        ImmediateRemediation=filled["ImmediateRemediation"], LongTermRemediation=filled["LongTermRemediation"]
                    )
                
                final_findings.append(asdict(finding))
                
            # 8. FINAL ASSEMBLY
            result = {
                "policy_id": doc.policy_id,
                "title": doc.title,
                "app_context": app_context,
                "execution_metadata": {
                    "runtime_seconds": round(time.time() - start_time, 2),
                    "clauses_processed": len(clause_texts),
                    "findings_generated": len(final_findings),
                    "quality_score": doc.quality_score
                },
                "findings": final_findings
            }
            
            self.checkpointer.save("final", doc.policy_id, result)
            self.logger.info(f"Execution complete. Output saved to final/{doc.policy_id}.json")
            return result

        except Exception as e:
            self.logger.error(f"Unrecoverable error processing {filepath}: {str(e)}")
            self.logger.error(traceback.format_exc())
            return {"status": "FAILED", "error": str(e)}

    def batch_process(self, directory: str, limit: int = 100):
        import glob
        files = glob.glob(os.path.join(directory, "*.xml")) + glob.glob(os.path.join(directory, "*.html"))
        target_files = files[:limit]
        
        success = 0
        self.logger.info(f"Starting bulk execution of {len(target_files)} policies...")
        
        for f in target_files:
            res = self.process_policy(f)
            if res.get("status") != "FAILED":
                success += 1
                
        self.logger.info(f"Batch complete. {success}/{len(target_files)} successful ({(success/len(target_files))*100:.1f}%).")

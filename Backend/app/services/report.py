from typing import List, Dict, Any

class ReportGenerationService:
    def generate_report(self, policy_id: str, title: str, app_context: str, execution_time: float, 
                        quality_score: int, clauses_processed: int, findings: List[Dict[str, Any]]) -> dict:
        
        # Calculate risk statistics
        risk_counts = {"LOW": 0, "MEDIUM": 0, "HIGH": 0, "SEVERE": 0, "REVIEW": 0}
        category_counts = {}
        
        for f in findings:
            r = f.get("RiskLevel") or f.get("ReviewStatus", "REVIEW")
            if r == "REVIEW_REQUIRED": r = "REVIEW"
            if r in risk_counts:
                risk_counts[r] += 1
                
            cat = f.get("Category") or f.get("PredictedCategory")
            if cat:
                category_counts[cat] = category_counts.get(cat, 0) + 1
        
        # Calculate overall severity
        if risk_counts["SEVERE"] > 0:
            severity = "SEVERE"
            overall_score = 100
        elif risk_counts["HIGH"] > 0:
            severity = "HIGH"
            overall_score = 80
        elif risk_counts["MEDIUM"] > 0:
            severity = "MEDIUM"
            overall_score = 50
        elif risk_counts["REVIEW"] > 0:
            severity = "REVIEW"
            overall_score = 0
        else:
            severity = "LOW"
            overall_score = 20
            
        risk_assessment = {
            "overall_score": overall_score,
            "severity": severity,
            "reason": "Based on highest severity finding."
        }
        
        summary = {
            "policy_id": policy_id,
            "title": title,
            "app_context": app_context,
            "execution_time": execution_time,
            "clauses_processed": clauses_processed,
            "findings_generated": len(findings),
            "quality_score": quality_score
        }
        
        return {
            "analysis_id": policy_id,
            "summary": summary,
            "findings": findings,
            "risk_assessment": risk_assessment,
            "compliance_mappings": {
                "gdpr": [], # Can be aggregated from findings
                "dpdp": []
            },
            "recommendations": [f.get("ImmediateRemediation") for f in findings if f.get("ImmediateRemediation")]
        }

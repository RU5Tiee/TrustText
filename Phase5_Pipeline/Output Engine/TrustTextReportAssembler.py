import os
import json
import uuid
from datetime import datetime
from collections import defaultdict

class TrustTextReportAssembler:
    def __init__(self, output_dir=r"D:\TrustText#2\Phase5_Pipeline\Output Engine\reports"):
        self.output_dir = output_dir
        self.formats = ["json", "markdown", "html", "audit"]
        for f in self.formats:
            os.makedirs(os.path.join(self.output_dir, f), exist_ok=True)

    def assemble(self, pipeline_result: dict, mode: str = "TECHNICAL") -> dict:
        """Assembles the raw PipelineResult into the canonical TrustTextReport schema."""
        report_id = f"REP-{uuid.uuid4()}"
        
        # 1. Evidence Appendix & Explainability Chains
        evidence_appendix = {}
        explainability_chains = []
        category_stats = defaultdict(lambda: {"count": 0, "confidences": [], "evidence_ids": []})
        framework_mappings = []
        risk_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0, "REVIEW": 0}
        remediations = []
        critical_findings = []
        
        for idx, finding in enumerate(pipeline_result.get("findings", [])):
            ev_id = f"EV-{idx+1}"
            evidence_appendix[ev_id] = {
                "clause_text": finding["Clause"],
                "classification": finding.get("Category") or finding.get("PredictedCategory"),
                "confidence": finding["Confidence"]
            }
            
            cat = finding.get("Category") or finding.get("PredictedCategory", "Other")
            category_stats[cat]["count"] += 1
            category_stats[cat]["confidences"].append(finding["Confidence"])
            category_stats[cat]["evidence_ids"].append(ev_id)
            
            if finding.get("ReviewStatus") == "REVIEW_REQUIRED":
                risk_counts["REVIEW"] += 1
                continue
                
            risk_level = finding["RiskLevel"]
            risk_counts[risk_level] += 1
            
            if risk_level in ["CRITICAL", "HIGH"]:
                critical_findings.append(ev_id)
                
            # Mappings
            for dpdp in finding.get("DPDP_References", []):
                framework_mappings.append({"framework": "DPDPA", "article_section": dpdp, "evidence_id": ev_id})
            for gdpr in finding.get("GDPR_References", []):
                framework_mappings.append({"framework": "GDPR", "article_section": gdpr, "evidence_id": ev_id})
                
            # Remediations
            if finding.get("ImmediateRemediation") or finding.get("LongTermRemediation"):
                priority = "Immediate" if risk_level in ["CRITICAL", "HIGH"] else "Medium"
                remediations.append({
                    "priority": priority,
                    "evidence_id": ev_id,
                    "recommended_action": finding.get("ImmediateRemediation", ""),
                    "long_term_action": finding.get("LongTermRemediation", ""),
                    "expected_benefit": f"Mitigates {risk_level} risk in {cat}"
                })
                
            # Explainability Chain
            explainability_chains.append({
                "chain_id": f"CHAIN-{idx+1}",
                "evidence_id": ev_id,
                "original_clause": finding["Clause"],
                "classification": cat,
                "confidence": finding["Confidence"],
                "risk_determination": finding["Explanation"],
                "remediation_rationale": finding.get("ImmediateRemediation", "")
            })

        # 2. Executive Summary
        total_risks = sum(risk_counts.values()) - risk_counts["LOW"] - risk_counts["REVIEW"]
        overall_posture = "POOR" if risk_counts["CRITICAL"] > 0 or risk_counts["HIGH"] > 2 else "FAIR" if total_risks > 0 else "STRONG"
        
        exec_summary = {
            "overall_posture": overall_posture,
            "major_strengths": [f"Clear disclosures in {c}" for c in category_stats if risk_counts.get("CRITICAL", 0) == 0][:2],
            "major_weaknesses": [f"High risk found in {c}" for c in category_stats if category_stats[c]["count"] > 0][:2],
            "compliance_observations": f"{len(framework_mappings)} legal obligations mapped.",
            "risk_observations": f"{risk_counts['CRITICAL']} Critical, {risk_counts['HIGH']} High risks detected."
        }
        
        # 3. Category Summaries
        cat_summaries = []
        for cat, stats in category_stats.items():
            cat_summaries.append({
                "category_name": cat,
                "clause_count": stats["count"],
                "average_confidence": sum(stats["confidences"])/len(stats["confidences"]) if stats["confidences"] else 0,
                "supporting_evidence_ids": stats["evidence_ids"]
            })
            
        # 4. Visualization Datasets
        vis_data = {
            "risk_distribution": [{"label": k, "value": v} for k, v in risk_counts.items() if v > 0],
            "category_distribution": [{"label": c["category_name"], "value": c["clause_count"]} for c in cat_summaries]
        }

        # Assembly
        report = {
            "report_id": report_id,
            "report_type": mode,
            "generated_timestamp": datetime.utcnow().isoformat() + "Z",
            "overview": {
                "policy_id": pipeline_result["policy_id"],
                "policy_name": pipeline_result.get("title", "Unknown Policy"),
                "app_context": pipeline_result.get("app_context", "Unknown"),
                "total_clauses": pipeline_result["execution_metadata"]["clauses_processed"],
                "total_findings": len(pipeline_result.get("findings", [])),
                "quality_score": pipeline_result["execution_metadata"].get("quality_score", 0),
                "processing_status": "COMPLETED"
            },
            "executive_summary": exec_summary,
            "category_summaries": cat_summaries,
            "compliance_mappings": framework_mappings,
            "risk_summary": {
                "risk_counts": risk_counts,
                "critical_findings": critical_findings
            },
            "remediation_recommendations": remediations,
            "explainability_chains": explainability_chains,
            "evidence_appendix": evidence_appendix,
            "visualization_datasets": vis_data
        }
        
        # If EXECUTIVE mode, strip technical chains
        if mode == "EXECUTIVE":
            del report["explainability_chains"]
            del report["evidence_appendix"]
            del report["compliance_mappings"]

        return report

    def export_json(self, report: dict):
        path = os.path.join(self.output_dir, "json", f"{report['report_id']}.json")
        with open(path, 'w') as f:
            json.dump(report, f, indent=2)
        return path

    def export_markdown(self, report: dict):
        path = os.path.join(self.output_dir, "markdown", f"{report['report_id']}.md")
        with open(path, 'w', encoding='utf-8') as f:
            f.write(f"# TrustText {report['report_type']} Report\n\n")
            f.write(f"**Policy:** {report['overview']['policy_name']} (ID: {report['overview']['policy_id']})\n")
            f.write(f"**Date:** {report['generated_timestamp']}\n\n")
            
            f.write("## 1. Executive Summary\n")
            f.write(f"- **Posture:** {report['executive_summary']['overall_posture']}\n")
            f.write(f"- **Risks:** {report['executive_summary']['risk_observations']}\n\n")
            
            f.write("## 2. Risk Summary\n")
            for k, v in report['risk_summary']['risk_counts'].items():
                f.write(f"- **{k}:** {v}\n")
            f.write("\n")
            
            if report['report_type'] == "TECHNICAL":
                f.write("## 3. Explainability Chains\n")
                for chain in report.get("explainability_chains", []):
                    f.write(f"### {chain['chain_id']}\n")
                    f.write(f"**Original Clause:** _{chain['original_clause']}_\n")
                    f.write(f"**Classification:** {chain['classification']} (Conf: {chain['confidence']:.2f})\n")
                    f.write(f"**Risk Determination:** {chain['risk_determination']}\n")
                    f.write(f"**Remediation Rationale:** {chain['remediation_rationale']}\n\n")
                    
        return path

    def export_html(self, report: dict):
        path = os.path.join(self.output_dir, "html", f"{report['report_id']}.html")
        html = f"<html><head><title>{report['report_id']}</title><style>body{{font-family:sans-serif;}} .critical{{color:red;}}</style></head><body>"
        html += f"<h1>TrustText {report['report_type']} Report</h1>"
        html += f"<h3>Policy: {report['overview']['policy_name']}</h3>"
        html += f"<p><b>Overall Posture:</b> {report['executive_summary']['overall_posture']}</p>"
        html += "<h3>Risk Distribution</h3><ul>"
        for k, v in report['risk_summary']['risk_counts'].items():
            html += f"<li><b>{k}:</b> {v}</li>"
        html += "</ul></body></html>"
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(html)
        return path

    def process_and_export(self, pipeline_result: dict):
        tech_report = self.assemble(pipeline_result, mode="TECHNICAL")
        exec_report = self.assemble(pipeline_result, mode="EXECUTIVE")
        
        self.export_json(tech_report)
        self.export_markdown(tech_report)
        self.export_html(tech_report)
        
        self.export_json(exec_report)
        
        return tech_report['report_id']

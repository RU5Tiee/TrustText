from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class PolicyAnalysisRequest(BaseModel):
    # Depending on how the file is passed, if we accept raw text:
    # Actually, the user says "POST /analyze Accept: PDF, TXT, HTML, XML"
    # Usually this means a multipart/form-data upload. We'll handle this in the route.
    pass

class FindingSchema(BaseModel):
    clause: str
    category: str
    confidence: float
    risk_level: str
    explanation: str
    legal_context: str
    dpdp_references: List[str]
    gdpr_references: List[str]
    triggered_rules: List[str]
    developer_action: str
    privacy_team_action: str
    immediate_remediation: str
    long_term_remediation: str

class ReviewFindingSchema(BaseModel):
    clause: str
    category: str
    confidence: float
    review_status: str
    review_explanation: str
    potential_legal_context: Optional[str] = None
    potential_references: Optional[List[str]] = None

class RiskAssessmentSchema(BaseModel):
    overall_score: int
    severity: str
    reason: str

class AnalysisSummarySchema(BaseModel):
    policy_id: str
    title: str
    app_context: str
    execution_time: float
    clauses_processed: int
    findings_generated: int
    quality_score: int

class PolicyAnalysisResponse(BaseModel):
    analysis_id: str
    summary: AnalysisSummarySchema
    findings: List[Dict[str, Any]]  # Can contain both Normal and Review findings
    risk_assessment: RiskAssessmentSchema
    compliance_mappings: Dict[str, Any]
    recommendations: List[str]

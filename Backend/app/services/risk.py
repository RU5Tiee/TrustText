import sys
from app.core.config import settings

if settings.RISK_MATRIX_DIR not in sys.path:
    sys.path.append(settings.RISK_MATRIX_DIR)

from Phase3_B_RiskScorer import RiskScorerB

class RiskAssessmentService:
    def __init__(self):
        self.scorer = RiskScorerB(settings.MAPPING_CSV)
        
    def evaluate_risk(self, clause_text: str, category: str, confidence: float, app_type: str) -> dict:
        return self.scorer.evaluate(clause_text, category, confidence, app_type)

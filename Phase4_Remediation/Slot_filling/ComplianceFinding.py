from dataclasses import dataclass, field
from typing import List

@dataclass
class NormalFinding:
    Clause: str
    Category: str
    Confidence: float
    RiskScore: float
    RiskLevel: str
    Explanation: str
    LegalContextSummary: str
    DPDP_References: List[str] = field(default_factory=list)
    GDPR_References: List[str] = field(default_factory=list)
    TriggeredRules: List[str] = field(default_factory=list)
    DeveloperAction: str = ""
    PrivacyTeamAction: str = ""
    ImmediateRemediation: str = ""
    LongTermRemediation: str = ""

@dataclass
class ReviewFinding:
    Clause: str
    PredictedCategory: str
    Confidence: float
    ReviewStatus: str
    ReviewExplanation: str
    PotentialLegalContext: str = ""
    PotentialReferences: List[str] = field(default_factory=list)
    HumanReviewRequired: bool = True
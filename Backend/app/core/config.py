import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TrustText Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    TRUSTTEXT_ROOT: str = r"D:\TrustText2"
    PARSING_ENGINE_DIR: str = os.path.join(TRUSTTEXT_ROOT, "Phase5_Pipeline", "Parsing Engine")
    RISK_MATRIX_DIR: str = os.path.join(TRUSTTEXT_ROOT, "Phase3_Classifier", "Risk_Matrix")
    SLOT_FILLING_DIR: str = os.path.join(TRUSTTEXT_ROOT, "Phase4_Remediation", "Slot_filling")
    
    CLASSIFIER_MODEL_DIR: str = os.path.join(TRUSTTEXT_ROOT, "Phase3_Classifier", "Classifier_model")
    MAPPING_CSV: str = os.path.join(TRUSTTEXT_ROOT, "Phase3_Classifier", "Classification_schema", "DPDP_GDPR_OPP_Alignment.csv")
    TEMPLATES_JSON: str = os.path.join(TRUSTTEXT_ROOT, "Phase4_Remediation", "Remediation_library", "Remediation_Templates.json")
    PATTERNS_JSON: str = os.path.join(TRUSTTEXT_ROOT, "Phase4_Remediation", "Slot_filling", "NarrativePatterns.json")

settings = Settings()

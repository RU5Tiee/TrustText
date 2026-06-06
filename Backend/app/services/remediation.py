import sys
from app.core.config import settings

if settings.SLOT_FILLING_DIR not in sys.path:
    sys.path.append(settings.SLOT_FILLING_DIR)

from SlotFiller import SlotFiller
from LegalLookup import LegalLookup

class RemediationService:
    def __init__(self, legal_lookup: LegalLookup):
        self.slot_filler = SlotFiller(settings.TEMPLATES_JSON, legal_lookup)
        
    def generate_remediation(self, category: str, risk_level: str) -> dict:
        return self.slot_filler.fill_normal(category, risk_level)

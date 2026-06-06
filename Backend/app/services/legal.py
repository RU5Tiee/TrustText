import sys
from app.core.config import settings

if settings.SLOT_FILLING_DIR not in sys.path:
    sys.path.append(settings.SLOT_FILLING_DIR)

from LegalLookup import LegalLookup

class LegalMappingService:
    def __init__(self):
        self.legal_lookup = LegalLookup(settings.MAPPING_CSV)
        
    def get_mappings(self, category: str) -> dict:
        summary = self.legal_lookup.generate_context_summary(category)
        # Note: The actual evidence per finding is fetched via SlotFiller, 
        # but we can return the summary from here.
        return {
            "summary": summary
        }

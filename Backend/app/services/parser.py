import sys
from app.core.config import settings

if settings.PARSING_ENGINE_DIR not in sys.path:
    sys.path.append(settings.PARSING_ENGINE_DIR)

from pipeline import PolicyIngestionPipeline

class ParsingService:
    def __init__(self):
        self.pipeline = PolicyIngestionPipeline()
        
    def parse_file(self, file_path: str) -> dict:
        doc = self.pipeline.process_file(file_path)
        return doc.to_dict()

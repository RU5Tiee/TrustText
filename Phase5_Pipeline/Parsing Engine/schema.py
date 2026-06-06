from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Clause:
    clause_id: str
    section_name: str
    clause_text: str
    start_offset: int
    end_offset: int
    preprocessing_tags: List[str] = field(default_factory=list)  # Lightweight hints

@dataclass
class Section:
    original_heading: str
    normalized_heading: str
    section_text: str
    start_offset: int
    end_offset: int
    clauses: List[Clause] = field(default_factory=list)

@dataclass
class Entity:
    text: str
    label: str
    start_offset: int
    end_offset: int

@dataclass
class PolicyMetadata:
    extracted_entities: List[Entity] = field(default_factory=list)
    extraction_date: str = ""
    language: str = "en"
    word_count: int = 0
    additional_info: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PolicyDocument:
    policy_id: str
    source_type: str        # e.g., "HTML", "XML", "PDF", "URL", "TXT"
    source_path: str        # Local file path or URL
    source_url: str         # Origin URL if known
    title: str              # Extracted title or fallback filename
    raw_text: str           # Unmodified extracted text
    cleaned_text: str       # Normalized and cleaned text
    sections: List[Section] = field(default_factory=list)
    clauses: List[Clause] = field(default_factory=list)
    metadata: PolicyMetadata = field(default_factory=PolicyMetadata)
    quality_score: int = 0  # 0-100
    validation_flags: List[str] = field(default_factory=list) # e.g., ["EMPTY_DOCUMENT", "LOW_WORD_COUNT"]

    def to_dict(self) -> dict:
        return {
            "policy_id": self.policy_id,
            "source_type": self.source_type,
            "source_path": self.source_path,
            "source_url": self.source_url,
            "title": self.title,
            "raw_text": self.raw_text,
            "cleaned_text": self.cleaned_text,
            "sections": [{
                "original_heading": s.original_heading,
                "normalized_heading": s.normalized_heading,
                "section_text": s.section_text,
                "start_offset": s.start_offset,
                "end_offset": s.end_offset,
                "clauses": [{
                    "clause_id": c.clause_id,
                    "section_name": c.section_name,
                    "clause_text": c.clause_text,
                    "start_offset": c.start_offset,
                    "end_offset": c.end_offset,
                    "preprocessing_tags": c.preprocessing_tags
                } for c in s.clauses]
            } for s in self.sections],
            "clauses": [{
                "clause_id": c.clause_id,
                "section_name": c.section_name,
                "clause_text": c.clause_text,
                "start_offset": c.start_offset,
                "end_offset": c.end_offset,
                "preprocessing_tags": c.preprocessing_tags
            } for c in self.clauses],
            "entities": [{
                "text": e.text,
                "label": e.label,
                "start_offset": e.start_offset,
                "end_offset": e.end_offset
            } for e in self.metadata.extracted_entities],
            "metadata": {
                "extraction_date": self.metadata.extraction_date,
                "language": self.metadata.language,
                "word_count": self.metadata.word_count,
                "additional_info": self.metadata.additional_info
            },
            "quality_score": self.quality_score,
            "validation_flags": self.validation_flags
        }

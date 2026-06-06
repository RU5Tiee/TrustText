import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from app.core.config import settings
from typing import List, Dict

class ClassificationService:
    def __init__(self, batch_size: int = 32):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.tokenizer = AutoTokenizer.from_pretrained(settings.CLASSIFIER_MODEL_DIR)
        self.model = AutoModelForSequenceClassification.from_pretrained(settings.CLASSIFIER_MODEL_DIR).to(self.device)
        self.model.eval()
        self.batch_size = batch_size
        self.target_labels = [
            "First Party Collection/Use", "Third Party Sharing/Collection", "User Choice/Control",
            "User Access, Edit and Deletion", "Data Retention", "Data Security", "Policy Change",
            "International and Specific Audiences", "Do Not Track", "Other"
        ]
        
    def classify_clauses(self, clauses: List[str]) -> List[Dict]:
        results = []
        for i in range(0, len(clauses), self.batch_size):
            batch = clauses[i:i + self.batch_size]
            inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=256).to(self.device)
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            for prob in probs:
                conf = torch.max(prob).item()
                pred = self.target_labels[torch.argmax(prob).item()]
                results.append({"category": pred, "confidence": conf})
        return results

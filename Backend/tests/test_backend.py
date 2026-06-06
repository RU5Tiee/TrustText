import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.parser import ParsingService
from app.services.classifier import ClassificationService
from app.services.risk import RiskAssessmentService
from app.services.legal import LegalMappingService
from app.services.remediation import RemediationService
from app.services.pipeline import TrustTextPipelineController
from unittest.mock import patch, MagicMock

client = TestClient(app)

@pytest.fixture
def mock_parser():
    return ParsingService()

@pytest.fixture
def mock_classifier():
    with patch("app.services.classifier.AutoModelForSequenceClassification") as mock_model:
        with patch("app.services.classifier.AutoTokenizer") as mock_tokenizer:
            yield ClassificationService()

def test_health_check():
    with patch("app.api.endpoints.get_pipeline_controller") as mock_controller:
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}

def test_version_info():
    response = client.get("/api/v1/version")
    assert response.status_code == 200
    assert "version" in response.json()

def test_parser_initialization(mock_parser):
    assert mock_parser is not None

def test_risk_scorer():
    scorer = RiskAssessmentService()
    res = scorer.evaluate_risk("We keep your data forever.", "Data Retention", 0.95, "Health")
    assert "final_risk" in res

def test_legal_mapping():
    mapper = LegalMappingService()
    res = mapper.get_mappings("Data Retention")
    assert "summary" in res

def test_remediation():
    mapper = LegalMappingService()
    remed = RemediationService(mapper.legal_lookup)
    res = remed.generate_remediation("Data Retention", "HIGH")
    assert "ImmediateRemediation" in res

def test_pipeline_controller():
    with patch("app.services.pipeline.ClassificationService.classify_clauses") as mock_classify:
        mock_classify.return_value = [{"category": "Data Retention", "confidence": 0.99}]
        # It takes time to instantiate, we are testing the class structure essentially
        with patch("app.services.pipeline.ParsingService.parse_file") as mock_parse:
            mock_parse.return_value = {
                "policy_id": "test",
                "title": "test",
                "cleaned_text": "We keep your data forever.",
                "clauses": [{"clause_text": "We keep your data forever."}]
            }
            controller = TrustTextPipelineController()
            # mock report saving path
            with patch("app.services.report.ReportGenerationService.generate_report") as mock_report:
                mock_report.return_value = {"status": "ok"}
                res = controller.process_policy("dummy.txt")
                assert res == {"status": "ok"}

def test_api_upload_invalid_type():
    with patch("app.api.endpoints.get_pipeline_controller"):
        response = client.post(
            "/api/v1/analyze",
            files={"file": ("test.png", b"dummy image data", "image/png")}
        )
        assert response.status_code == 400

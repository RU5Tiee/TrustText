# TrustText Backend

This is the FastAPI backend for the TrustText Privacy Policy Analysis platform.

## Architecture

* **FastAPI**: Provides robust API endpoints and request validation.
* **Pipeline Controller**: Orchestrates the analysis flow.
* **Service Layer**: Wrappers around the existing intelligence modules:
  * Parser Service
  * Classifier Service
  * Risk Service
  * Remediation Service
  * Legal Mapping Service
  * Report Generation Service

## Setup and Startup

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Note: You might need to install `en_core_web_sm` for spaCy: `python -m spacy download en_core_web_sm`)*

2. Start the FastAPI development server:
   ```bash
   python run.py
   ```

3. The server will start on `http://localhost:8000`. You can view the automatic API documentation at `http://localhost:8000/docs`.

## Testing

To run the test suite:
```bash
pytest tests/
```

## Logs

Execution logs and error traces are located in the `logs/` directory.

## Endpoints

* `POST /api/v1/analyze`: Upload a policy document (`.pdf`, `.txt`, `.html`, `.xml`) to receive the full JSON analysis report.
* `GET /api/v1/health`: Server health check.
* `GET /api/v1/version`: API version information.

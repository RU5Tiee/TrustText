# TrustText

TrustText is an advanced AI-driven policy and document analysis system designed for robust risk scoring, clause investigation, and compliance framework mapping. By leveraging custom ML pipelines across multiple phases, TrustText analyzes textual documents to identify vulnerabilities, suggest remediations, and map clauses to specific cybersecurity and compliance frameworks.

> **Note on Missing Model Files:**
> The highly specialized fine-tuned machine learning models (`.safetensors` files) generated during `Phase2` and `Phase3` exceed GitHub's standard 100MB file limit (they are >400MB each) and have been excluded from this repository via `.gitignore` to enable a smooth clone and push experience. To run the full analysis pipeline locally, you will need to download the models externally and place them in their respective `Domian_Model` and `Classifier_model` directories.

---

## Project Structure

The project is structured into modular phases for maintainability and scalability:

*   **`Frontend/`**: The web interface dashboard featuring a modern glassmorphism design. It displays real-time analysis, document risk scores, category breakdowns, and historical data.
*   **`Backend/`**: The core API server handling document ingestion, history tracking, and coordinating the ML pipeline.
*   **`Phase2_Domain_Adaptation/`**: Models fine-tuned and adapted for specific cybersecurity and compliance terminology.
*   **`Phase3_Classifier/`**: Clause classification engine that identifies and categorizes textual risks.
*   **`Phase4_Remediation/`**: Generates natural-language remediation suggestions and maps clauses to specific framework articles, rules, and controls.
*   **`Phase5_Pipeline/`**: The orchestration layer that connects adaptation, classification, and remediation into a single continuous analysis pipeline.
  <img width="1007" height="793" alt="Final" src="https://github.com/user-attachments/assets/8ba11490-7392-48ba-83b8-e1df6536eff4" />


---

## Core Features & Supported Frameworks

### 🌟 Key Features
*   **Risk Scoring & Dashboarding:** Real-time automated calculation of document risk, presented on a modern glassmorphism UI.
*   **Clause Investigation:** Deep-dive analysis into specific clauses with context-aware, natural-language remediation suggestions.
*   **Framework Mapping:** Automatically links offending text/clauses to exact Articles, Sections, and Controls.
*   **Analysis History:** Stores historical document analyses for auditing and comparative review.

### 🏛️ Supported Compliance Frameworks
TrustText's knowledge base and classification layers are explicitly mapped to:
*   **GDPR** (General Data Protection Regulation)
*   **DPDP** (Digital Personal Data Protection Act)
*   *(Includes mapping for concepts like First Party Collection, Third Party Sharing, User Consent, Data Security, and Data Retention)*

---

## Model Metrics & Classification Categories

### Phase 2: Domain Adaptation
The underlying language model was fine-tuned for specialized compliance terminology. Following 3 epochs of training (2160 steps), the model achieved:
*   **Training Loss:** `0.9388`
*   **Evaluation Loss:** `0.9094`
*   **Perplexity:** `2.483`

### Phase 3: Clause Classification Metrics
The classifier categorizes document clauses into 10 distinct privacy and security categories. 

*(Internal Validation Results - 557 segments)*

| Classification Category | Precision | Recall | F1-Score | Support (N) |
| :--- | :--- | :--- | :--- | :--- |
| **First Party Collection/Use** | 0.86 | 0.84 | **0.85** | 164 |
| **Third Party Sharing/Collection** | 0.82 | 0.79 | **0.80** | 114 |
| **User Choice/Control** | 0.79 | 0.74 | **0.76** | 50 |
| **User Access, Edit and Deletion** | 0.50 | 0.83 | **0.62** | 18 |
| **Data Retention** | 0.33 | 0.60 | **0.43** | 5 |
| **Data Security** | 0.77 | 0.92 | **0.84** | 26 |
| **Policy Change** | 0.88 | 0.94 | **0.91** | 16 |
| **International and Specific Audiences** | 0.68 | 0.89 | **0.77** | 38 |
| **Do Not Track** | 1.00 | 0.67 | **0.80** | 3 |
| **Other** | 0.83 | 0.68 | **0.75** | 123 |
| **Macro Avg** | **0.75** | **0.79** | **0.75** | 557 |

**Overall Accuracy:** `79.0%`

*Evaluation Methodology Note:* The metrics reported above are derived from an internal validation set of 557 sequence segments. The input data was heavily structured, appropriately chunked, and preprocessed to align with the model's sequence length and distribution mapping. Evaluation scores will naturally vary when deploying zero-shot inference against raw, unstructured, or uncleaned HTML/text documents. 

**Architectural Safeguards:**
1. **Focal Loss:** The adversarial architecture utilizes focal loss to force the network to map severely underrepresented minority classes (e.g., Data Retention) rather than defaulting to majority classes, ensuring compliance-ready recall rates.
2. **Confidence Thresholding:** The model is calibrated with a strict 60% confidence threshold. If the softmax probability of a prediction falls below 0.60, the model actively rejects the classification and routes the segment to the "Other" category. This fail-safe mechanism intentionally sacrifices raw recall to strictly minimize False Positives and preserve elite Precision on critical security clauses.

---

## Setup & Execution

### Backend
1. Navigate to the `Backend/` directory.
2. Install necessary dependencies via `pip install -r requirements.txt`.
3. Ensure the `logs/` and `History/` directories are correctly routed within the backend configuration.
4. Run the API server.

### Frontend
1. Navigate to the `Frontend/` directory.
2. Install dependencies via `npm install`.
3. Start the development server via `npm run dev`.
4. Ensure the backend API URL is correctly configured in your frontend context.

---

## License
MIT License

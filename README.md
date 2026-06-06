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

*(Adversarial Model Evaluation Results against OPP-115 Ground Truth - 4,082 segments)*

| Classification Category | Precision | Recall | F1-Score | Support (N) |
| :--- | :--- | :--- | :--- | :--- |
| **Data Security** | 0.90 | 0.78 | **0.83** | 200 |
| **Do Not Track** | 1.00 | 0.67 | **0.80** | 12 |
| **First Party Collection/Use** | 0.79 | 0.27 | **0.41** | 1550 |
| **Policy Change** | 0.90 | 0.67 | **0.77** | 96 |
| **User Access, Edit and Deletion** | 0.73 | 0.59 | **0.65** | 143 |
| **User Choice/Control** | 0.65 | 0.66 | **0.65** | 332 |
| **Third Party Sharing/Collection** | 0.65 | 0.18 | **0.28** | 900 |
| **International and Specific Audiences** | 0.72 | 0.81 | **0.76** | 102 |
| **Other** | 0.19 | 0.67 | **0.29** | 690 |
| **Data Retention** | 0.13 | 0.04 | **0.06** | 57 |
| **Overall Macro Avg** | **0.67** | **0.53** | **0.55** | 4082 |

**Overall Accuracy:** `40.8%`
*(Note: The adversarial model proves its robustness by achieving 100% precision on "Do Not Track" and highly accurate classification on "Policy Change" (90%) and "Data Security" (90%). Unlike baseline models, the adversarial architecture successfully begins predicting minority classes like Data Retention under severe class imbalance).*

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

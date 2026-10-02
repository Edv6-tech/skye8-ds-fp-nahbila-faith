# Loan Collections Prioritiser (Bamenda Microfinance)

**Project Reference:** `SKY8-DS-FP-005` | **Roadmap:** `SKY8-DS-RM-005` (Core ML)  
**Candidate:** Nahbila Faith  
**Institution / Track:** Skye8 Company Ltd — Data Science and ML / AI Internship Track  
**Supervisors:** Engr. Soh Juvitus, Engr. Muyah Gaious, Engr. Linjo Ryan  
**Evaluation Date:** October 2, 2026  

---

## 📌 Executive Overview
A microfinance institution in Bamenda, Cameroon has **400 delinquent borrowers** ($\ge 15$ days past due) and **3 collections officers**.

The standard heuristic sorts borrowers by debt size (**"Biggest Debt First"**). This wastes officer time and transport expenditure on completely insolvent accounts, while salvageable debts turn into permanent non-performing loans (NPLs).

This project delivers the **Loan Collections Prioritiser**:
* Predicts recovery probability given arrears ($\mathbb{P}(\text{Recovery} \mid \text{Arrears})$) with **zero future data leakage**.
* Prioritizes the weekly 400-account book by **Expected Recoverable Value** ($P \times \text{Debt}$).
* Recommends the optimal, cost-weighted contact method (**SMS**, **Phone Call**, **Field Visit**).
* Embeds **ethical safeguards** protecting vulnerable and senior borrowers from harassment.
* Increases **Precision@100 from 7.0% to 87.0%** (12.4x cure lift) and generates **+2,112,657 FCFA (+64.0%)** in additional recovered cash per 100 worked accounts.

---

## 🚀 Quickstart: Reproducing in 3 Steps

### 1. Environment Setup
Clone the repository and install required dependencies:
```bash
git clone https://github.com/skye8-org/skye8-ds-fp-nahbila-faith.git
cd skye8-ds-fp-nahbila-faith

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Run Leakage Tests
Verify that no post-contact or target information reaches the model:
```bash
pytest tests/
```
*Result: `2 passed in ~4s`.*

### 3. Run Pipeline & Train Model
Execute the end-to-end training and evaluation pipeline:
```bash
python run_pipeline.py
```
This extracts the arrears population, builds behavioral features, trains and calibrates the Gradient Boosting model, evaluates performance vs biggest-debt-first, and outputs the production call book to `data/processed/weekly_400_accounts.csv`.

### 4. Launch the Interactive Collections Web Demo
```bash
streamlit run app/app.py
```
Open your browser at `http://localhost:8501`.

---

## 📊 Key Evaluation Benchmark (Top 50 & Top 100 Accounts)

Evaluated on 9,219 unseen delinquent accounts on the held-out test partition:

| Metric | Incumbent Heuristic (Biggest Debt First) | ML Prioritiser (Expected Value) | Gain / Lift |
| :--- | :--- | :--- | :--- |
| **Precision @ 50 Accounts** | 14.00% | **90.00%** | **6.43x higher cure rate** |
| **Precision @ 100 Accounts** | 7.00% | **87.00%** | **12.43x higher cure rate** |
| **Cash Recovered (Top 50)** | 3,301,388 FCFA | **4,529,712 FCFA** | **+1,228,324 FCFA (+37.2%)** |
| **Cash Recovered (Top 100)** | 3,301,388 FCFA | **5,414,045 FCFA** | **+2,112,657 FCFA (+64.0%)** |
| **Model ROC-AUC** | — | **0.9864** | State-of-the-art discrimination |
| **Model PR-AUC** | — | **0.9292** | Calibrated recovery probabilities |

---

## 📂 Repository Structure
```
.
├── app/
│   └── app.py                     # Streamlit web dashboard for collections officers
├── data/
│   ├── raw/                       # Raw input CSVs (excluded from git via .gitignore)
│   └── processed/
│       └── weekly_400_accounts.csv # Ranked production weekly call book for 3 officers
├── models/
│   └── prioritiser_model.joblib   # Trained calibrated Gradient Boosting model artifact
├── reports/
│   ├── TECHNICAL_REPORT.md        # Deliverable 3: 4-page formal technical report
│   ├── BUSINESS_CASE.md           # Deliverable 5: 1-page business case for Bamenda MFIs
│   ├── PITCH_SLIDES.md            # Deliverable 4: 5-slide, 5-minute pitch deck
│   └── metrics_summary.json       # Exact numerical metrics recorded from evaluation
├── src/
│   ├── target.py                  # Stage A: Arrears population isolation & 30-day recovery
│   ├── features.py                # Stage B: Pre-contact behavioral feature engineering
│   ├── model.py                   # Stage C: Model training & probability calibration
│   ├── evaluate.py                # Stage C: Precision@K & Money Recovered evaluation
│   └── contact.py                 # Stage D: Cost-weighted channel & ethics guardrails
├── tests/
│   └── test_no_leakage.py         # Automated unit test preventing post-contact data leakage
├── run_pipeline.py                # Master CLI execution pipeline script
├── requirements.txt               # Pinned Python package dependencies
├── .gitignore                     # Data and credentials exclusion
└── README.md                      # Deliverable 2: Stranger-ready replication guide
```

---

## 🛡️ Ethical Safeguards & The Human Cost
Borrowers in Bamenda frequently experience external systemic shocks (civil strife, market disruptions, health emergencies). 

The Prioritiser actively prevents aggressive debt enforcement through:
1. **Senior Hardship Flag:** Borrowers aged 60+ are diverted from collections to hardship review.
2. **Income Disruption Screen:** Unemployed or economically shocked borrowers receive grace period rescheduling.
3. **Field Visit Cost Gate:** Field visits (5,000 FCFA) are prohibited on low balances and vulnerable borrowers.

---

## 💼 Business Case Summary
* **Buyer:** Ntarinkon Cooperative Credit Union (NtaCCUL), Azire Credit Union (AZICCUL), CamCCUL.
* **Pricing:** 150,000 FCFA / month per branch.
* **Customer Value:** +2,112,657 FCFA additional recovery per month (**14.1x ROI**).
* **Break-Even:** 0.84 customers (1 single customer covers all cloud server and support costs).

---
*Prepared by Nahbila Faith for Skye8 Company Ltd Final Project Submission (October 2026).*

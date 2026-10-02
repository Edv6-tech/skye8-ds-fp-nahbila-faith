# Loan Collections Prioritiser (Bamenda Microfinance)

**Project Reference:** `SKY8-DS-FP-005` | **Roadmap:** `SKY8-DS-RM-005` (Core ML)  
**Candidate:** Nahbila Faith  
**Institution / Track:** Skye8 Company Ltd — Data Science and ML / AI Internship Track  
**Supervisors:** Engr. Soh Juvitus, Engr. Muyah Gaious, Engr. Linjo Ryan  
**Evaluation Date:** October 2, 2026  

---

## 📌 Executive Overview
A microfinance institution in Bamenda, Cameroon has **400 delinquent borrowers** ($\ge 15$ days past due) and **3 collections officers** (John, Beatrice, Emmanuel).

The incumbent heuristic sorts borrowers by debt size (**"Biggest Debt First"**). This wastes officer time and transport expenditure on completely insolvent accounts, while salvageable debts turn into permanent non-performing loans (NPLs).

This project delivers the **Loan Collections Prioritiser**:
* Predicts recovery probability given arrears ($\mathbb{P}(\text{Recovery} \mid \text{Arrears})$) with **zero future data leakage**.
* Estimates **Time-to-Cure** (Survival hazard regressor) and **Partial Settlement Ratio** ($\hat{r}$).
* Prioritizes the weekly 400-account book by **Expected Recoverable Value** ($P \times \hat{r} \times \text{Debt}$).
* Recommends the optimal, cost-weighted contact method (**SMS**, **Phone Call**, **Field Visit**).
* Clusters field visits across 5 Bamenda Quarters, cutting motorcycle (**benskin**) fuel by ~60%.
* Features **Bilingual Outreach Scripts** (Formal English & Cameroon Pidgin English) and **Printable Field Dockets** with tear-off pledge slips.
* Houses an **Adaptable Engine (`AdaptablePrioritiser`)** featuring branch archetype shifting, live Bayesian online field feedback, and macroeconomic fuel/airtime shock recalibration.
* Embeds **ethical safeguards** protecting vulnerable and senior borrowers from harassment (18.5% protected).
* Increases **Precision@100 from 7.0% to 88.0%** (12.57x cure lift) and generates **+2,164,156 FCFA (+65.6%)** in additional net cash per 100 worked accounts.

---

## 🚀 Quickstart: Reproducing in 4 Steps

### 1. Environment Setup
Clone the repository and install dependencies:
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

### 2. Run Automated Test Suite (Leakage & Adaptability)
Verify zero post-contact data leakage and test multi-task model adaptation:
```bash
pytest tests/
```
*Result: `8 passed in ~10s` (100% green).*

### 3. Run Pipeline & Train All Models
Execute the end-to-end multi-task training, survival regression, and evaluation pipeline:
```bash
python run_pipeline.py
```
This ingests multi-source data, builds behavioral features, trains and calibrates the Gradient Boosting classifier, fits the survival regressor and partial recovery regressor, computes causal uplift and XAI waterfalls, and outputs the production call book to `data/processed/weekly_400_accounts.csv`.

### 4. Launch the Interactive Collections Web Demo
```bash
streamlit run app/app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 📊 Key Evaluation Benchmark (Top 50 & Top 100 Accounts)

Evaluated on 9,219 unseen delinquent accounts on the held-out test partition:

| Metric | Incumbent Heuristic (Biggest Debt First) | ML Prioritiser (Expected Value) | Gain / Lift |
| :--- | :--- | :--- | :--- |
| **Precision @ 50 Accounts** | 14.00% | **90.00%** | **6.43x higher cure rate** |
| **Precision @ 100 Accounts** | 7.00% | **88.00%** | **12.57x higher cure rate** |
| **Cash Recovered (Top 50)** | 3,301,388 FCFA | **4,557,608 FCFA** | **+1,256,220 FCFA (+38.1%)** |
| **Cash Recovered (Top 100)** | 3,301,388 FCFA | **5,465,544 FCFA** | **+2,164,156 FCFA (+65.6%)** |
| **Model ROC-AUC** | — | **0.9864** | State-of-the-art discrimination |
| **Model PR-AUC** | — | **0.9288** | Calibrated recovery probabilities |
| **Average Settlement Ratio** | — | **66.2%** | Partial recovery regressor ($\hat{r}$) |
| **Mean Time-to-Cure** | — | **14.6 days** | Survival hazard estimation |

---

## 🎛️ Model Adaptability Architecture (`AdaptablePrioritiser`)

The core machine learning engine is built for continuous operational adaptation:
1. **Branch Archetype Adaptation:** Adjusts baseline prior log-odds intercepts across *Urban Commercial* (Mankon), *Agrarian Rural* (Coffee farming outskirts), and *Civil Servant Payroll* (Up Station).
2. **Online Bayesian Field Feedback:** As officers log contact outcomes in the app (*"Promise to Pay"*, *"Cured & Settled"*, *"Severe Hardship"*), the engine recalibrates the borrower's probability in real time.
3. **Macroeconomic Unit Cost Recalibration:** Recalculates channel economics live when motorcycle fuel (*essence*) or phone call airtime costs fluctuate.
4. **Missing Modality Resilience:** Graceful domain fallback when new credit unions lack Credit Bureau or POS Cash records.
5. **Multi-Objective Policy Re-ranking:** Instantly re-ranks the book for *Max Cash*, *Max Cure Volume*, *Balanced Sustainability*, or *Vulnerable First*.

---

## 📂 Repository Structure
```
.
├── app/
│   └── app.py                     # Streamlit Haute-Elegance dashboard (8 interactive tabs)
├── data/
│   ├── raw/                       # Raw input CSVs (excluded from git via .gitignore)
│   └── processed/
│       └── weekly_400_accounts.csv # Production weekly call book with quarters, XAI & scripts
├── models/
│   ├── prioritiser_model.joblib   # Calibrated Gradient Boosting classifier
│   ├── time_to_cure_regressor.joblib # Survival hazard time-to-cure regressor
│   └── partial_recovery_regressor.joblib # Settlement ratio regressor
├── reports/
│   ├── TECHNICAL_REPORT.md        # Deliverable 3: 4-page formal technical report
│   ├── BUSINESS_CASE.md           # Deliverable 5: 1-page financial model for Bamenda MFIs
│   ├── PITCH_SLIDES.md            # Deliverable 4: 5-slide, 5-minute executive pitch deck
│   └── metrics_summary.json       # Exact numerical validation metrics
├── src/
│   ├── target.py                  # Stage A: Arrears isolation & 30-day cure window
│   ├── features.py                # Stage B: Pre-contact behavioral & seasonal features
│   ├── model.py                   # Stage C: Multi-task ML, XAI waterfall & AdaptablePrioritiser
│   ├── evaluate.py                # Stage C: Precision@K & Money Recovered evaluation
│   └── contact.py                 # Stage D: Channel economics, quarter clustering & bilingual scripts
├── tests/
│   ├── test_no_leakage.py         # Automated unit test preventing post-contact data leakage
│   └── test_models_and_clustering.py # Unit tests for AdaptablePrioritiser & route clustering
├── run_pipeline.py                # Master CLI execution pipeline script
├── requirements.txt               # Pinned Python package dependencies
├── .gitignore                     # Data and credentials exclusion
└── README.md                      # Deliverable 2: Stranger-ready replication guide
```

---

## 🛡️ Ethical Safeguards & The Human Cost
Borrowers in Bamenda frequently experience external systemic disruptions (regional economic headwinds, health emergencies, crop failures). 

The Prioritiser actively prevents aggressive debt enforcement through:
1. **Senior Hardship Shield:** Borrowers aged 60+ are diverted from collections to cooperative restructuring.
2. **Income Disruption Screen:** Unemployed or economically shocked borrowers receive grace period rescheduling.
3. **Field Visit Cost Gate:** Field visits (5,000 FCFA) are prohibited on low balances and vulnerable borrowers.
4. **Welfare Audit:** In the active 400-account book, **74 borrowers (18.5%)** are flagged as vulnerable.

---

## 💼 Business Case Summary
* **Target Buyers:** Ntarinkon Cooperative Credit Union (NtaCCUL), Azire Credit Union (AZICCUL), CamCCUL network.
* **Pricing:** 150,000 FCFA / month per branch.
* **Customer Value:** **+2,164,156 FCFA** additional net cash recovered per month (**14.4x ROI**).
* **Payback Horizon:** Just **2.1 days** of monthly collections.

---
*Prepared by Nahbila Faith for Skye8 Company Ltd Final Project Submission (October 2026).*

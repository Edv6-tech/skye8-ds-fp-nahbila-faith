# Pitch Deck: Loan Collections Prioritiser
**Presenter:** Nahbila Faith | **Track:** Data Science and ML / AI Internship Track  
**Skye8 Reference:** SKY8-DS-FP-005 | **Duration:** 5 Minutes (5 Slides)  

---

## Slide 1: The Collections Crisis in Bamenda

### Subtitle: Why Chasing the Biggest Debt is Losing Money for Credit Unions
* **The Reality on Commercial Avenue:**
  * An average Bamenda microfinance branch (e.g. NtaCCUL, AZICCUL) has **400 delinquent loans** in arrears each week.
  * Only **3 collections officers** are available to make calls and field visits.
  * **The Incumbent Mistake:** Officers sort accounts by debt size ("Biggest Debt First").
* **The Fatal Flaw:**
  * Borrowers with the largest debts are often completely insolvent (business failure, relocation).
  * Officers burn motorcycle fuel and hours traveling to unrecoverable accounts, while small/medium loans that could be recovered turn into write-offs.
  * **Current Result:** Only **7% of contacts successfully cure** at the top 100 accounts.

---

## Slide 2: What We Built

### Subtitle: An AI Decision Engine for Weekly Delinquency Recovery
* **Not Default Prediction — Recovery Prediction:**
  * Standard credit scoring asks: *"Will they default?"* at origination.
  * We ask: *"Given that they are 15+ days late, will they cure if contacted this week?"*
* **The Core Features:**
  * **Calibrated Gradient Boosting Engine:** Trained on historical repayment behaviour with **zero future data leakage**.
  * **Ranked Call Book:** Prioritizes accounts by **Expected Recovered Value** ($P(\text{recovery}) \times \text{Debt}$).
  * **Action Recommender:** Recommends the cost-optimal channel: **SMS (50 FCFA)**, **Call (500 FCFA)**, or **Field Visit (5,000 FCFA)**.
  * **Ethical Guardrails:** Automatically flags senior and distressed borrowers for restructuring, preventing abusive harassment.

---

## Slide 3: The Proof — Numbers, Not Adjectives

### Subtitle: Validated Performance vs Incumbent Biggest-Debt-First
Across 9,200+ unseen delinquent test accounts:

| Metric | Incumbent (Biggest Debt First) | Skye8 AI Prioritiser | Improvement / Lift |
| :--- | :--- | :--- | :--- |
| **Precision @ 50 (First 2 Weeks)** | 14.0% | **90.0%** | **6.4x Higher Cure Rate** |
| **Precision @ 100 (Monthly Capacity)** | 7.0% | **87.0%** | **12.4x Higher Cure Rate** |
| **Cash Recovered (Top 100)** | 3,301,388 FCFA | **5,414,045 FCFA** | **+2,112,657 FCFA** |
| **Model Discrimination** | — | **ROC-AUC: 0.986** | **PR-AUC: 0.929** |

* **Key Takeaway:** By working the Skye8 ranked list, the three officers recover **2.11 Million FCFA MORE** every single month from the same 100 accounts.

---

## Slide 4: Who Buys It & Pricing

### Subtitle: Direct B2B Revenue in the North West Region
* **Target Customers in Bamenda:**
  * **NtaCCUL** (15 branches)
  * **AZICCUL** (Azire headquarters & regional network)
  * **CBC Mbingo Credit Union** & **CamCCUL affiliates**
* **Simple, High-ROI Subscription Model:**
  * **Price:** **150,000 FCFA / month** per branch.
* **Customer Value Proposition:**
  * Customer spends: **150,000 FCFA**.
  * Customer gains: **+2,112,657 FCFA** in cash recovered.
  * **Net Gain to Customer:** **+1,962,657 FCFA / month (14x ROI)**.
  * A no-brainer purchase for any MFI credit committee.

---

## Slide 5: Unit Economics & Execution

### Subtitle: Immediate Profitability at Scale
* **Monthly Operating Costs:**
  * Cloud Server & Database: 29,400 FCFA ($49)
  * SMS Gateway: 30,000 FCFA ($50)
  * Local Support in Bamenda: 60,000 FCFA ($100)
  * **Total Monthly Cost: 126,000 FCFA ($210)**.
* **Break-Even:**
  * **1 Single Customer Branch** covers 100% of operational costs.
  * At 5 credit union branches: **750,000 FCFA revenue**, **83% gross profit margin**.
* **Current Status:**
  * ✅ End-to-end ML pipeline fully trained and validated.
  * ✅ Automated leakage tests passing (`100% pass`).
  * ✅ Interactive mobile-friendly Streamlit web app deployed and ready for field use.

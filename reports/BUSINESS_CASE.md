# Business Case: Loan Collections Prioritiser
**Product:** Skye8 Collections Prioritiser SaaS  
**Target Market:** Microfinance Institutions (MFIs) & Credit Unions in Bamenda, Cameroon  
**Prepared by:** Nahbila Faith (SKY8-DS-FP-005)  
**Date:** October 2, 2026  

---

## 1. Executive Summary & Customer Identification

### Target Customers in Bamenda
The primary target market consists of licensed Category 1 and Category 2 Microfinance Institutions (MFIs) and cooperative credit unions headquartered in Bamenda, North West Region, Cameroon:
1. **Ntarinkon Cooperative Credit Union Ltd (NtaCCUL):** ~15 branches across Bamenda (Commercial Avenue, Nkwen, Up Station) managing over 80,000 members.
2. **Azire Cooperative Credit Union Ltd (AZICCUL):** Headquartered in Azire, Bamenda; one of Cameroon's largest credit unions.
3. **Mbingo Baptist Credit Union / CBC Health Services MFI:** Serves healthcare and educational workers in Mezam division.
4. **Community Credit Unions (CamCCUL network affiliates):** 18 affiliated union branches in the greater Bamenda metropolitan area.

---

## 2. Customer Problem & Quantified Value Proposition

### The Problem
A standard branch holds ~400 delinquent loans ($\ge 15$ days overdue) worth roughly **4,920,000 FCFA** in overdue instalments. Three field collections officers work the arrears book by descending debt size ("biggest debt first"). Because massive debts are predominantly insolvent, officers achieve only a **7.0% precision** at top-100 accounts, recovering **3.30M FCFA** while incurring significant transport expenditures on fruitless field visits.

### The Value Delivered (In Francs CFA)
Using the Skye8 Prioritiser:
* **Precision at Top 100 Accounts:** Increases from **7.0% to 87.0%** (12.4x more recovered accounts).
* **Cash Recovered (Top 100 Accounts):** Increases from **3,301,388 FCFA to 5,414,045 FCFA**.
* **Net Value Added per Month:** **+2,112,657 FCFA** in cash collections per branch per month.
* **Annual Recovered Gain:** Over **25,000,000 FCFA** in prevented write-offs per branch.

---

## 3. Product Pricing & Revenue Model

* **Licensing Model:** B2B Software-as-a-Service (SaaS), billed monthly per institution branch.
* **Subscription Price:** **150,000 FCFA / month** per MFI branch (includes 3 officer accounts + 1 supervisor portal).
* **ROI for Buyer:**
  $$\text{Monthly Customer Net Gain} = 2,112,657\text{ FCFA} - 150,000\text{ FCFA} = \mathbf{+1,962,657\text{ FCFA/month}}$$
  **Return on Investment (ROI): 14.1x** the subscription fee in direct recovered liquidity.

---

## 4. Cost Structure & Break-Even Analysis

### Monthly Operating Costs (Hosting & Operations)
| Expense Item | Provider / Specification | Monthly Cost (USD) | Monthly Cost (FCFA) |
| :--- | :--- | :--- | :--- |
| Cloud Server & Database | DigitalOcean Droplet (2 vCPU, 4GB RAM) | $24.00 | 14,400 FCFA |
| Managed PostgreSQL | Supabase Pro Tier | $25.00 | 15,000 FCFA |
| SMS Gateway (Orange / MTN API) | Bulk SMS Cameroon (~2,000 SMS @ 15 FCFA) | $50.00 | 30,000 FCFA |
| Maintenance & Support | Part-time technical support in Bamenda | $100.00 | 60,000 FCFA |
| Domain, SSL & Monitoring | Cloudflare & Sentry | $11.00 | 6,600 FCFA |
| **Total Monthly Operating Cost** | | **$210.00** | **126,000 FCFA** |

*(Exchange rate: 1 USD = 600 FCFA)*

### Break-Even Point
$$\text{Break-Even Customers} = \frac{\text{Fixed Monthly Operational Costs}}{\text{Subscription Price}} = \frac{126,000\text{ FCFA}}{150,000\text{ FCFA}} = \mathbf{0.84\text{ Customers}}$$

* **Just ONE customer (e.g. NtaCCUL Main Branch) achieves immediate cash-flow profitability (119% cost coverage).**
* With **5 credit union branches signed** (e.g., 3 NtaCCUL branches + 2 AZICCUL branches):
  * **Monthly Revenue:** $5 \times 150,000 = \mathbf{750,000\text{ FCFA/month}}$
  * **Monthly Margin:** $750,000 - 126,000 = \mathbf{624,000\text{ FCFA/month}}$ (**83.2% net margin**).

# Thesis Research Guide
## The Trade-off Between AML/KYC Compliance Stringency and Financial Inclusion in Mobile Financial Services (MFS): Evidence from Bangladesh

---

## 1. What This Research Is About

Mobile Financial Services (MFS) like bKash, Nagad, and Rocket have become the primary gateway to formal financial access for millions of unbanked and underbanked people in Bangladesh — especially in rural areas. At the same time, regulators (Bangladesh Bank, BFIU) and MFS providers themselves impose Anti-Money Laundering (AML) and Know-Your-Customer (KYC) compliance controls — identity verification, transaction limits, account monitoring, freezing suspicious accounts — to prevent fraud, money laundering, and terrorist financing.

These two forces pull in opposite directions:

- **Stricter compliance** (more KYC documentation, lower transaction limits, more frequent account freezes/verification) → reduces fraud/laundering risk, but can create friction that discourages usage, especially for less digitally literate or lower-income users.
- **Looser compliance** → easier access and higher usage/inclusion, but higher risk of the platform being misused for illicit activity.

This research empirically tests that trade-off: **does higher perceived compliance stringency reduce MFS usage/financial inclusion (measured through actual transaction behavior), controlling for demographic factors like income, age, education, and location?**

The core method is a **multiple regression model**, where:
- **Dependent variable:** a financial/usage measure of inclusion — monthly MFS transaction volume (BDT) and/or transaction frequency
- **Independent variables:** compliance stringency proxies — KYC burden, transaction limit restrictiveness, freeze/block frequency, KYC method (paper vs e-KYC), perceived monitoring intensity
- **Control variables:** income, age, education, urban/rural, years of MFS usage, number of providers used

The output should let you conclude something like: *"KYC friction and transaction limit restrictiveness are significant negative predictors of MFS transaction volume, even after controlling for income and education — suggesting a measurable inclusion cost to strict AML/KYC enforcement."* (Your actual result may differ — that's fine, the finding matters less than the rigor.)

This is valuable and original because most Bangladeshi BBA/finance theses either study AML compliance *or* financial inclusion separately — very few quantitatively connect the two using primary survey data, and your bKash AML/Governance internship gives you real practitioner insight to interpret the results credibly.

---

## 2. What Content You Need to Include (Paper Structure)

### Chapter 1 — Introduction (3–4 pages)
- Background of MFS growth in Bangladesh
- Background of AML/CFT regulatory framework for MFS
- Problem statement: the inclusion-compliance tension
- Research objectives (general + specific)
- Research questions
- Significance of the study
- Scope and limitations

### Chapter 2 — Literature Review (6–8 pages)
- Theories of financial inclusion (access, usage, quality dimensions)
- Global literature on AML/KYC compliance and its effect on access to financial services
- MFS-specific studies (Bangladesh and comparable markets — Kenya's M-Pesa, India's Paytm, etc.)
- Regulatory literature: FATF standards, risk-based approach to AML
- Research gap — why this specific trade-off, using primary quantitative data, hasn't been well studied in Bangladesh

### Chapter 3 — Bangladesh MFS & Regulatory Context (4–5 pages)
- Overview of the MFS industry in Bangladesh (market size, players, growth trends — cite Bangladesh Bank MFS statistics)
- Bangladesh Bank's MFS regulatory guidelines
- BFIU's AML/CFT requirements applicable to MFS (KYC tiers, STR/SAR obligations, transaction monitoring rules)
- This is where your bKash Governance/AML experience is most useful — you can describe real processes (goAML STR/SAR submission, CR monitoring, e-KYC vs paper KYC) to ground the paper in practice

### Chapter 4 — Methodology (4–5 pages)
- Research design (quantitative, cross-sectional survey)
- Conceptual framework / hypotheses (state formally, e.g., H1: KYC burden is negatively associated with MFS transaction volume)
- Population and sampling method (random/convenience sampling of MFS users)
- Sample size justification (~180–220 for 10 predictors)
- Questionnaire design and variable operationalization
- Data collection method (Google Form, distribution channels)
- Data analysis method (multiple regression, diagnostic tests: VIF for multicollinearity, normality, heteroskedasticity)

### Chapter 5 — Data Analysis & Results (8–10 pages)
- Respondent demographic profile (descriptive statistics, tables/charts)
- Reliability check (Cronbach's alpha for Likert items)
- Correlation matrix
- Multiple regression results (coefficients, significance, R², adjusted R²)
- Diagnostic test results (VIF, residual plots)
- Hypothesis testing outcomes (which hypotheses supported/rejected)

### Chapter 6 — Discussion (4–5 pages)
- Interpret each significant/non-significant variable
- Compare findings to literature reviewed in Chapter 2
- Explain unexpected results
- Practical implications for MFS providers and regulators

### Chapter 7 — Conclusion & Recommendations (3–4 pages)
- Summary of key findings
- Policy recommendations (e.g., risk-based KYC tiering, streamlined e-KYC, balancing STR thresholds)
- Limitations of the study
- Suggestions for future research

### References
- APA or your university's required citation style

### Appendices
- Full questionnaire (English + Bangla)
- SPSS/Stata output tables
- Any supporting documents

---

## 3. What Type of Content You Need to Read

To write a credible literature review and justify your methodology, you need roughly these categories of sources:

### A. Academic journal articles (most important — aim for 25–40 citations)
- Search terms: "financial inclusion mobile money", "AML compliance financial inclusion trade-off", "KYC and financial access developing countries", "mobile financial services Bangladesh", "risk-based approach AML", "regulatory burden fintech adoption"
- Good sources: Google Scholar, ResearchGate, SSRN, Emerald Insight, ScienceDirect, JSTOR (check if your university library gives free access)
- Look especially for studies on **M-Pesa (Kenya)**, **Paytm/UPI (India)**, and **other South Asian/African MFS markets** — these are the closest comparable cases to Bangladesh and are heavily studied

### B. Regulatory and policy documents (primary sources for Chapter 3)
- Bangladesh Bank MFS regulatory guidelines and circulars
- BFIU (Bangladesh Financial Intelligence Unit) AML/CFT guidelines for MFS/banks
- FATF (Financial Action Task Force) recommendations, especially on risk-based approach and financial inclusion
- Bangladesh Bank quarterly MFS statistics reports (for industry data/context)

### C. Industry & market reports
- bKash, Nagad annual reports or sustainability reports (public versions)
- GSMA "State of the Industry Report on Mobile Money" (annual, global, very well respected — good for global context and comparisons)
- LightCastle Partners, LIRNEasia — Bangladesh-focused fintech/MFS market research
- World Bank Global Findex Database (financial inclusion data by country, very citable)

### D. Theoretical/foundational texts
- Financial inclusion frameworks (e.g., Sarma's Index of Financial Inclusion, Beck & Demirgüç-Kunt's work on access to finance)
- AML/CFT theory — risk-based approach literature (FATF-aligned academic writing)

### E. Methodology references
- A stats/research methods textbook or article on multiple regression assumptions and diagnostics (for correctly writing your methodology and justifying your diagnostic tests)
- Examples: Field's "Discovering Statistics," or any accessible multiple regression guide — useful to cite proper procedure (VIF thresholds, normality tests, etc.)

### Practical tip on reading volume
You don't need to read every source cover-to-cover. For most journal articles: read abstract, introduction, and conclusion first, skim methodology/results only if directly relevant to your variables. Aim to build a working list of 30-40 sources, but only 15-20 need deep reading — the rest can be cited for specific facts/figures you pull from their abstracts or summaries.

---

## Suggested Order of Work
1. Finalize hypotheses (I can draft these next)
2. Start survey distribution now (takes time to reach 180+ responses)
3. Read/write Literature Review + Bangladesh Context chapters while survey responses come in
4. Once you have enough responses, run regression and write Chapters 5–7

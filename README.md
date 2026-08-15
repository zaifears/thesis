# Bangladesh MFS AML/KYC Inclusion Study

<div align="center">

  <img src="https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python" alt="Python 3.13" />
  <img src="https://img.shields.io/badge/Research-Thesis-0A66C2?style=for-the-badge" alt="Research thesis" />
  <img src="https://img.shields.io/badge/Data-Analysis-28A745?style=for-the-badge" alt="Data analysis" />
  <img src="https://img.shields.io/badge/Status-Active-FF6B35?style=for-the-badge" alt="Status active" />

</div>

A thesis-based data analysis project examining the balance between AML/KYC compliance and financial inclusion in Bangladesh’s Mobile Financial Services (MFS) ecosystem.

## Overview

This research explores how stricter Anti-Money Laundering (AML) and Know-Your-Customer (KYC) requirements affect the use of mobile financial services such as bKash, Nagad, and Rocket. The project analyzes whether greater compliance stringency creates friction for users and reduces access, adoption, or transaction behavior — even after accounting for demographic and socio-economic factors.

The study is designed around a quantitative survey-based approach, combining respondent data with statistical testing to assess whether KYC burden, transaction restrictions, monitoring intensity, and related compliance measures are associated with lower MFS usage and weaker financial inclusion.

## Research Objective

To examine whether perceived compliance stringency — including KYC burden, transaction-limit restrictions, verification requirements, and monitoring intensity — is negatively associated with MFS participation and inclusion in Bangladesh, while controlling for income, age, education, residence, and prior MFS experience.

## Why this project matters

- Bangladesh’s digital financial ecosystem is growing rapidly, but access and trust remain sensitive to user experience and regulatory friction.
- Strong AML/KYC controls are necessary for security and legitimacy, yet excessive burden may reduce adoption among underserved groups.
- This project contributes to the discussion on how financial regulation can balance compliance, inclusion, and consumer experience in emerging mobile finance markets.

## Project Workflow

This repository supports the full thesis workflow:

- data cleaning and coding for survey responses
- descriptive statistical analysis
- reliability and correlation checks
- regression analysis for key hypotheses
- chart generation for reporting and final presentation

## Repository Structure

- `01_clean.py` — cleans and codes raw survey data
- `02_analysis.py` — performs analysis, diagnostics, and hypothesis testing
- `03_chart.py` — generates professional charts and figures
- `figures_out/` — exported visual outputs
- `dataset.xlsx` — raw dataset
- `coded_dataset.xlsx` — processed coded dataset
- `analysis_tables.xlsx` — analysis tables produced for reporting
- `Thesis_Research_Guide.md` — research and methodology guide
- `BUP Thesis Paper.md` — thesis write-up and notes
- `MFS_Thesis_Questionnaire.md` — survey instrument

## Tech Stack

This project uses the following Python packages:

- Python 3.13
- pandas
- numpy
- scipy
- matplotlib
- tabulate
- openpyxl

## Getting Started

### 1. Install Python on Windows

```powershell
winget install --id Python.Python.3.13 -e
```

### 2. Create a virtual environment

```powershell
cd A:\Thesis_Paper
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install pandas numpy scipy matplotlib tabulate openpyxl
```

### 4. Run the analysis pipeline

```powershell
python 01_clean.py
python 02_analysis.py
python 03_chart.py
```

If PowerShell blocks script execution, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

## Notes

This repository is intended for academic and research use. Large PDF documents and institutional reference files are excluded from version control using the project `.gitignore` file to keep the GitHub repository clean and focused on the analysis work.

## License

This project is provided under an unlicensed/public-domain-style setup for academic sharing. See [LICENSE](LICENSE) for details.

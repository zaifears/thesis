"""
CLEAN AND CODE (v2 — real data, friction direction fixed)
==========================================================
Converts the real Google Forms export into an analysis-ready coded dataset.

Changes from v1:
- kyc_friction / limit_friction added (reverse-coded so ALL compliance
  variables point the same direction: higher = more friction/stringency).
  kyc_ease and limit_restriction are still kept in their original direction
  too, in case you want to report the raw items descriptively.
- INPUT_PATH now points at the real response file, not synthetic data.
- Quality flags unchanged in logic, but now actually meaningful since this
  runs on real responses.

Coding scheme:
- Income, transaction volume, transaction frequency -> bracket midpoints
  (kept ONLY for the secondary/robustness OLS model — see 03_analysis.py.
  The PRIMARY model uses the ordinal category directly, not the midpoint.)
- e-KYC method -> dummy (1 = e-KYC, 0 = paper, NaN if "Not sure")
- Freeze/block frequency -> ordinal count scale (0-3)
- Likert items (ease, limit restriction, monitoring, satisfaction) -> 1-5 as-is
- kyc_friction = 6 - kyc_ease            (higher = harder KYC)
- limit_friction = 6 - limit_restriction (higher = more restricted)
- Number of providers -> numeric (3+ coded as 3)
- Years using MFS -> ordinal midpoint in years

Data-quality flags (not silently dropped, just flagged):
- straight_line_flag: identical value across all 4 raw attitude items
- income_volume_mismatch_flag: "No income" but top transaction bracket
- freeze_limit_mismatch_flag: "Never frozen" but "very frequently restricted"
"""

import pandas as pd
import numpy as np

INPUT_PATH = "dataset.xlsx"           # <-- real Google Forms export
OUTPUT_PATH = "coded_dataset.xlsx"

df = pd.read_excel(INPUT_PATH, sheet_name="Form responses 1")
cols = df.columns.tolist()


def find_col(prefix):
    matches = [c for c in cols if c.strip().startswith(prefix)]
    if not matches:
        raise ValueError(f"Could not find a column starting with '{prefix}'.")
    return matches[0]


COL_ELIGIBLE_USE = find_col("Q0.1")
COL_ELIGIBLE_AGE = find_col("Q0.2")
COL_AGE = find_col("Q1.1")
COL_GENDER = find_col("Q1.2")
COL_EDU = find_col("Q1.3")
COL_RES = find_col("Q1.4")
COL_INCOME = find_col("Q1.5")
COL_YEARS = find_col("Q1.6")
COL_PROVIDERS = find_col("Q1.7")
COL_VOLUME = find_col("Q2.1")
COL_FREQ = find_col("Q2.2")
COL_SERVICES = find_col("Q2.3")
COL_KYCMETHOD = find_col("Q3.1")
COL_EASE = find_col("Q3.2")
COL_LIMIT = find_col("Q3.3")
COL_FREEZE = find_col("Q3.4")
COL_MONITOR = find_col("Q3.5")
COL_SAT = find_col("Q3.6")

# ---- Eligibility filter (should already be enforced by Form skip logic,
#      but confirm here rather than assume) ----
n_before = len(df)
df = df[df[COL_ELIGIBLE_USE].astype(str).str.strip().eq("Yes")]
df = df[df[COL_ELIGIBLE_AGE].astype(str).str.contains("Yes", na=False)]
n_after = len(df)
print(f"Eligibility filter: {n_before} rows -> {n_after} rows "
      f"({n_before - n_after} excluded as non-MFS-user or under-18)")

out = pd.DataFrame()
out["age_bracket"] = df[COL_AGE]
out["gender"] = df[COL_GENDER]
out["education"] = df[COL_EDU]
out["residence"] = df[COL_RES]
out["urban"] = df[COL_RES].astype(str).str.contains("Urban", na=False).astype(int)

INCOME_MID = {
    "No income / কোনো আয় নেই": 0, "Below 15,000": 7500, "15,000 – 30,000": 22500,
    "30,001 – 50,000": 40000, "50,001 – 100,000": 75000, "Above 100,000": 125000,
}
out["income_bdt"] = df[COL_INCOME].astype(str).str.strip().map(INCOME_MID)

YEARS_MID = {
    "Less than 1 year / ১ বছরের কম": 0.5, "1–3 years / ১-৩ বছর": 2,
    "3–5 years / ৩-৫ বছর": 4, "More than 5 years / ৫ বছরের বেশি": 6,
}
out["years_using_mfs"] = df[COL_YEARS].map(YEARS_MID)

PROVIDERS_NUM = {"1": 1, "2": 2, "3 or more / ৩ বা তার বেশি": 3}
out["num_providers"] = df[COL_PROVIDERS].astype(str).str.strip().map(PROVIDERS_NUM)

# --- Ordinal category codes (PRIMARY dv encoding — ordered, 1 = lowest) ---
VOLUME_ORDER = ["Below 2,000 Taka", "2,000 – 5,000 Taka", "5,001 – 10,000 Taka",
                "10,001 – 25,000 Taka", "25,001 – 50,000 Taka", "Above 50,000 Taka"]
VOLUME_MID = {"Below 2,000 Taka": 1000, "2,000 – 5,000 Taka": 3500,
              "5,001 – 10,000 Taka": 7500, "10,001 – 25,000 Taka": 17500,
              "25,001 – 50,000 Taka": 37500, "Above 50,000 Taka": 65000}
out["txn_volume_cat"] = df[COL_VOLUME].astype(str).str.strip().map(
    {v: i + 1 for i, v in enumerate(VOLUME_ORDER)})
out["txn_volume_bdt"] = df[COL_VOLUME].astype(str).str.strip().map(VOLUME_MID)  # secondary model only

FREQ_ORDER = ["1–5", "6–10", "11–20", "More than 20 / ২০ এর বেশি"]
FREQ_MID = {"1–5": 3, "6–10": 8, "11–20": 15, "More than 20 / ২০ এর বেশি": 25}
out["txn_frequency_cat"] = df[COL_FREQ].astype(str).str.strip().map(
    {v: i + 1 for i, v in enumerate(FREQ_ORDER)})
out["txn_frequency"] = df[COL_FREQ].astype(str).str.strip().map(FREQ_MID)  # secondary model only

out["num_services_used"] = df[COL_SERVICES].astype(str).apply(
    lambda x: len([s for s in x.split(",") if s.strip()]))

out["ekyc_dummy"] = df[COL_KYCMETHOD].apply(
    lambda x: 1 if isinstance(x, str) and "e-KYC" in x
    else (0 if isinstance(x, str) and "Paper" in x else np.nan))

FREEZE_SCALE = {"Never / কখনো না": 0, "Once / একবার": 1,
                "2–3 times / ২-৩ বার": 2, "More than 3 times / ৩ বারের বেশি": 3}
out["freeze_count"] = df[COL_FREEZE].astype(str).str.strip().map(FREEZE_SCALE)

out["kyc_ease"] = pd.to_numeric(df[COL_EASE], errors="coerce")
out["limit_restriction"] = pd.to_numeric(df[COL_LIMIT], errors="coerce")
out["monitoring_perception"] = pd.to_numeric(df[COL_MONITOR], errors="coerce")
out["satisfaction"] = pd.to_numeric(df[COL_SAT], errors="coerce")

# ---- Friction-direction harmonization (THE FIX) ----
# After this: kyc_friction, limit_friction, freeze_count, monitoring_perception
# ALL point the same way -- higher value = more compliance friction/stringency.
out["kyc_friction"] = 6 - out["kyc_ease"]
out["limit_friction"] = 6 - out["limit_restriction"]

# ---- Data quality flags ----
likert_cols = ["kyc_ease", "limit_restriction", "monitoring_perception", "satisfaction"]
out["straight_line_flag"] = out[likert_cols].nunique(axis=1).eq(1).astype(int)
out["income_volume_mismatch_flag"] = (
    (out["income_bdt"] == 0) & (out["txn_volume_bdt"] >= 65000)).astype(int)
out["freeze_limit_mismatch_flag"] = (
    (out["freeze_count"] == 0) & (out["limit_restriction"] <= 1)).astype(int)
out["any_quality_flag"] = out[
    ["straight_line_flag", "income_volume_mismatch_flag", "freeze_limit_mismatch_flag"]
].max(axis=1)

n_missing_total = out.isna().sum().sum()
n_missing_ekyc = out["ekyc_dummy"].isna().sum()
n_missing_unexpected = n_missing_total - n_missing_ekyc
n_flagged = out["any_quality_flag"].sum()

print(f"\nRows retained: {len(out)}")
print(f"Missing ekyc_dummy (EXPECTED -- 'Not sure' responses): {n_missing_ekyc}")
print(f"Missing values elsewhere (UNEXPECTED if not 0): {n_missing_unexpected}")
if n_missing_unexpected > 0:
    print(out.isna().sum()[out.isna().sum() > 0].drop("ekyc_dummy", errors="ignore"))
print(f"Rows flagged for >=1 data-quality issue: {n_flagged} ({n_flagged/len(out)*100:.1f}%)")
print(f"  - straight-lining: {out['straight_line_flag'].sum()}")
print(f"  - income/volume mismatch: {out['income_volume_mismatch_flag'].sum()}")
print(f"  - freeze/limit mismatch: {out['freeze_limit_mismatch_flag'].sum()}")
print(f"\ne-KYC method distribution:\n{df[COL_KYCMETHOD].value_counts()}")
print(f"\nTransaction-volume category distribution:\n{out['txn_volume_cat'].value_counts().sort_index()}")

out.to_excel(OUTPUT_PATH, index=False, sheet_name="Coded Data")
print(f"\nSaved coded dataset to {OUTPUT_PATH}")

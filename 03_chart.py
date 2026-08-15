"""
GENERATE CHARTS (v2 — aligned with 02_clean.py v2 / 03_analysis.py v2)
=========================================================================
Produces every chart Chapter 6 needs as a standalone PNG.

Changes from v1:
- Uses kyc_friction / limit_friction (harmonized direction) in the
  correlation heatmap instead of raw kyc_ease / limit_restriction, so
  Figure 2 matches the sign convention used in Tables 4-11 of 03_analysis.py.
- Path is now relative ("coded_dataset.xlsx"), matching 02_clean.py v2.
- Figures 3-5 (residual diagnostics) now import SimpleOLS's exact logic from
  the same regression spec used in 03_analysis.py's SECONDARY model, so the
  residual plots match the robustness-check table instead of a third,
  slightly different ad hoc model.
- NEW Figure 6: odds-ratio bar chart from the PRIMARY ordinal logistic
  model, since that's now the headline result, not the OLS residuals.

Run AFTER 02_clean.py has produced coded_dataset.xlsx from the real export.

Output (in FIG_DIR):
  fig1_demographics.png          - age/gender/education/residence bar charts
  fig2_correlation_heatmap.png   - Pearson correlation matrix heatmap (friction-coded)
  fig3_residual_histogram.png    - histogram of OLS residuals (secondary model)
  fig4_qq_plot.png                - normal Q-Q plot of residuals
  fig5_residuals_vs_fitted.png    - residuals vs. fitted values scatter
  fig6_odds_ratios.png            - odds ratios from primary ordinal logit model
"""

import numpy as np
import pandas as pd
from scipy import stats
from scipy.optimize import minimize
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import os

DATA_PATH = "coded_dataset.xlsx"
FIG_DIR = "figures_out"
os.makedirs(FIG_DIR, exist_ok=True)

df = pd.read_excel(DATA_PATH)


def english_only(text):
    """Strip to English portion before '/' -- matplotlib's default font
    can't render Bengali glyphs (renders as empty boxes)."""
    return str(text).split("/")[0].strip()


plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.edgecolor": "#333333",
    "axes.linewidth": 0.8,
})

# ============================================================================
# Figure 1: Demographic profile (4-panel)
# ============================================================================
demo_specs = [
    ("age_bracket", "Age"), ("gender", "Gender"),
    ("education", "Education"), ("residence", "Residence"),
]
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, (col, label) in zip(axes.flat, demo_specs):
    counts = df[col].value_counts()
    ax.barh(range(len(counts)), counts.values, color="#4472C4")
    ax.set_yticks(range(len(counts)))
    ax.set_yticklabels([english_only(c) for c in counts.index], fontsize=9)
    ax.set_title(label, fontsize=11, fontweight="bold")
    ax.set_xlabel("n")
    ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig1_demographics.png", dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {FIG_DIR}/fig1_demographics.png")

# ============================================================================
# Figure 2: Correlation heatmap (FRICTION-CODED, matches Table 4)
# ============================================================================
corr_cols = ["income_bdt", "years_using_mfs", "num_providers", "kyc_friction",
             "limit_friction", "freeze_count", "monitoring_perception",
             "ekyc_dummy", "txn_volume_bdt", "txn_frequency"]
corr_labels = ["Income", "Years Using MFS", "# Providers", "KYC Friction", "Limit Friction",
               "Freeze Count", "Monitoring", "e-KYC Dummy", "Txn Volume", "Txn Frequency"]
corr = df[corr_cols].corr(method="pearson")

fig, ax = plt.subplots(figsize=(9, 7.5))
im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr_labels))); ax.set_xticklabels(corr_labels, rotation=45, ha="right", fontsize=9)
ax.set_yticks(range(len(corr_labels))); ax.set_yticklabels(corr_labels, fontsize=9)
for i in range(len(corr_labels)):
    for j in range(len(corr_labels)):
        ax.text(j, i, f"{corr.values[i, j]:.2f}", ha="center", va="center",
                 fontsize=7.5, color="white" if abs(corr.values[i, j]) > 0.5 else "black")
plt.colorbar(im, ax=ax, shrink=0.8, label="Pearson r")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig2_correlation_heatmap.png", dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {FIG_DIR}/fig2_correlation_heatmap.png")

# ============================================================================
# Shared regression setup (IDENTICAL to 03_analysis.py's secondary model)
# ============================================================================
class SimpleOLS:
    def __init__(self, y, X):
        self.y = np.asarray(y, dtype=float)
        self.X = np.asarray(X, dtype=float)
        self.n, self.k = self.X.shape
        XtX_inv = np.linalg.inv(self.X.T @ self.X)
        self.beta = XtX_inv @ self.X.T @ self.y
        self.fitted = self.X @ self.beta
        self.resid = self.y - self.fitted


reg_df = df.dropna(subset=["ekyc_dummy", "txn_volume_cat"]).copy()
AGE_MID = {"18–24": 21, "25–34": 29.5, "35–44": 39.5, "45–54": 49.5,
           "55 or above / ৫৫ বা তার বেশি": 58}
reg_df["age_num"] = reg_df["age_bracket"].map(AGE_MID)

X_cols = ["kyc_friction", "limit_friction", "freeze_count", "monitoring_perception",
          "ekyc_dummy", "income_bdt", "age_num", "years_using_mfs",
          "num_providers", "urban"]
X_labels = ["KYC Friction", "Limit Friction", "Freeze Count", "Monitoring Perception",
            "e-KYC Dummy", "Income (BDT)", "Age", "Years Using MFS",
            "# Providers", "Urban"]
reg_df = reg_df.dropna(subset=X_cols + ["txn_volume_bdt"])
X_raw = reg_df[X_cols].astype(float).values
X = np.column_stack([np.ones(len(X_raw)), X_raw])
y = reg_df["txn_volume_bdt"].astype(float).values
model = SimpleOLS(y, X)

# ============================================================================
# Figure 3: Histogram of OLS residuals (secondary/robustness model)
# ============================================================================
fig, ax = plt.subplots(figsize=(7, 5))
ax.hist(model.resid, bins=25, color="#4472C4", edgecolor="white")
ax.set_xlabel("Residual"); ax.set_ylabel("Frequency")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig3_residual_histogram.png", dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {FIG_DIR}/fig3_residual_histogram.png")

# ============================================================================
# Figure 4: Q-Q plot
# ============================================================================
fig, ax = plt.subplots(figsize=(7, 5))
stats.probplot(model.resid, dist="norm", plot=ax)
ax.get_lines()[0].set_markerfacecolor("#4472C4")
ax.get_lines()[0].set_markeredgecolor("#4472C4")
ax.get_lines()[1].set_color("#C00000")
ax.set_title("")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig4_qq_plot.png", dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {FIG_DIR}/fig4_qq_plot.png")

# ============================================================================
# Figure 5: Residuals vs fitted
# ============================================================================
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(model.fitted, model.resid, alpha=0.6, color="#4472C4", edgecolor="white", s=40)
ax.axhline(0, color="#C00000", linestyle="--", linewidth=1)
ax.set_xlabel("Fitted Values"); ax.set_ylabel("Residuals")
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig5_residuals_vs_fitted.png", dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {FIG_DIR}/fig5_residuals_vs_fitted.png")

# ============================================================================
# Figure 6 (NEW): Odds ratios from the PRIMARY ordinal logistic model
# ============================================================================
class OrdinalLogit:
    """Same proportional-odds model as 03_analysis.py -- duplicated here so
    this script can run standalone without importing 03_analysis.py."""

    def __init__(self, y, X):
        self.y = np.asarray(y, dtype=int)
        self.X = np.asarray(X, dtype=float)
        self.n, self.p = self.X.shape
        self.k = int(self.y.max())
        self.n_thresh = self.k - 1

    def _thresholds(self, a):
        thresh = np.empty(self.n_thresh)
        thresh[0] = a[0]
        for j in range(1, self.n_thresh):
            thresh[j] = thresh[j - 1] + np.exp(a[j])
        return thresh

    def _neg_loglik(self, params):
        a = params[:self.n_thresh]
        beta = params[self.n_thresh:]
        thresh = self._thresholds(a)
        eta = self.X @ beta
        ll = 0.0
        for j in range(1, self.k + 1):
            mask = self.y == j
            if not mask.any():
                continue
            lower = thresh[j - 2] - eta[mask] if j > 1 else -np.inf * np.ones(mask.sum())
            upper = thresh[j - 1] - eta[mask] if j < self.k else np.inf * np.ones(mask.sum())
            p_upper = np.where(np.isinf(upper), 1.0, 1 / (1 + np.exp(-upper)))
            p_lower = np.where(np.isinf(lower), 0.0, 1 / (1 + np.exp(-lower)))
            prob = np.clip(p_upper - p_lower, 1e-10, 1.0)
            ll += np.sum(np.log(prob))
        return -ll

    def fit(self):
        x0 = np.concatenate([np.linspace(-1, 1, self.n_thresh), np.zeros(self.p)])
        res = minimize(self._neg_loglik, x0, method="BFGS", options={"maxiter": 2000})
        self.beta = res.x[self.n_thresh:]
        return self


y_ord = reg_df["txn_volume_cat"].values
X_scaled = X_raw.copy()
for i, label in enumerate(X_labels):
    if label in ["Income (BDT)", "Age", "Years Using MFS"]:
        mu, sd = X_scaled[:, i].mean(), X_scaled[:, i].std()
        X_scaled[:, i] = (X_scaled[:, i] - mu) / sd

ol_model = OrdinalLogit(y_ord, X_scaled).fit()
or_values = np.exp(ol_model.beta)

fig, ax = plt.subplots(figsize=(8, 5.5))
colors = ["#C00000" if v < 1 else "#4472C4" for v in or_values]
ax.barh(X_labels, or_values, color=colors)
ax.axvline(1, color="black", linestyle="--", linewidth=1)
ax.set_xlabel("Odds Ratio (< 1 = supports hypothesized negative effect)")
ax.invert_yaxis()
plt.tight_layout()
plt.savefig(f"{FIG_DIR}/fig6_odds_ratios.png", dpi=200, bbox_inches="tight")
plt.close()
print(f"Saved {FIG_DIR}/fig6_odds_ratios.png")

print(f"\nDone. 6 charts saved to {FIG_DIR}/")

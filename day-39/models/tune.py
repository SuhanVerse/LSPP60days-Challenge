#!/usr/bin/env python3
"""
day-39/models/tune.py

Train & tune regression & classification pipelines
on the “Most Streamed Spotify Songs 2024” dataset
(adapting to its actual column names), with improved targets:
  - regression on log10(streams)
  - classification by “top50” instead of “top10”
"""

import warnings
from sklearn.exceptions import ConvergenceWarning

# ─── SILENCE KNOWN WARNINGS ────────────────────────────────────────────────
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge, LogisticRegression
from sklearn.model_selection import GridSearchCV, train_test_split

# ─── PATHS ─────────────────────────────────────────────────────────────────
DATA_PATH = "/home/xlegion/RUST/LSPP60days-Challenge/day-39/data/smusic.csv"
PLOTS_DIR = "/home/xlegion/RUST/LSPP60days-Challenge/day-39/plots"

def ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)

# ─── DATA LOADING & CLEANING ────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(
        DATA_PATH,
        encoding="latin1",
        engine="python",
        on_bad_lines="skip"
    )

    # rename to internal names
    column_map = {
        "All Time Rank":   "position",
        "Spotify Streams": "streams"
    }
    missing = [c for c in column_map if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in CSV: {missing}")
    df = df.rename(columns=column_map)

    # strip non-digits, coerce empties → NaN → drop
    for col in ("position","streams"):
        df[col] = (
            df[col].astype(str)
                  .str.replace(r"[^\d]", "", regex=True)
                  .replace("", np.nan)
                  .astype(float)
        )
    df = df.dropna(subset=["position","streams"])
    df["position"] = df["position"].astype(int)
    df["streams"]  = df["streams"].astype(int)

    # -- print original class balance for is_top10
    df["is_top10"] = (df["position"] <= 10).astype(int)
    print("Original is_top10 balance:\n", df["is_top10"].value_counts(), "\n")

    # -- define improved classification target at median split ("top50")
    median_pos = df["position"].median()
    df["is_top50"] = (df["position"] <= median_pos).astype(int)
    print(f"Median position = {median_pos}")
    print("New is_top50 balance:\n", df["is_top50"].value_counts(), "\n")

    # -- regression target: log of streams
    df["log_streams"] = np.log10(df["streams"])

    return df

# ─── REGRESSION PIPELINE ───────────────────────────────────────────────────
def tune_regression(df):
    X = df[["position"]]
    y = df["log_streams"]                  # use log-scale target
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline([("scale", StandardScaler()), ("reg", Ridge())])
    param_grid = {"reg__alpha": [0.1, 1.0, 10.0, 100.0]}

    grid = GridSearchCV(pipe, param_grid, cv=5, scoring="neg_mean_squared_error")
    grid.fit(Xtr, ytr)

    best_alpha = grid.best_params_["reg__alpha"]
    best_mse   = -grid.best_score_
    print(f"[Regression] Best alpha: {best_alpha}, CV MSE (log-scale): {best_mse:.2f}")

    # Plot CV MSE vs alpha
    results = pd.DataFrame(grid.cv_results_)
    viz = pd.DataFrame({
        "alpha": results["param_reg__alpha"].astype(float),
        "MSE":   -results["mean_test_score"]
    }).sort_values("alpha")

    plt.figure(figsize=(5,3))
    sns.barplot(x="alpha", y="MSE", data=viz, palette="viridis")
    plt.title("Ridge CV MSE (log-streams) by α")
    plt.xlabel("α")
    plt.ylabel("MSE")
    out = os.path.join(PLOTS_DIR, "ridge_cv_mse_logstreams.png")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")

# ─── CLASSIFICATION PIPELINE ───────────────────────────────────────────────
def tune_classification(df):
    X = df[["position"]]
    y = df["is_top50"]                    # use new top50 label
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline([("scale", StandardScaler()),
                     ("clf", LogisticRegression(solver="liblinear"))])
    param_grid = {
        "clf__C":       [0.01, 0.1, 1, 10, 100],
        "clf__penalty": ["l1", "l2"]
    }

    grid = GridSearchCV(pipe, param_grid, cv=5, scoring="accuracy")
    grid.fit(Xtr, ytr)

    best_params = grid.best_params_
    best_acc    = grid.best_score_
    print(f"[Classification] Best params: {best_params}, CV Acc (top50): {best_acc:.2f}")

    results = pd.DataFrame(grid.cv_results_)
    pivot = results.pivot(index="param_clf__penalty",
                          columns="param_clf__C",
                          values="mean_test_score")

    plt.figure(figsize=(6,3))
    sns.heatmap(pivot, annot=True, fmt=".2f", cmap="plasma", cbar_kws={"label":"Accuracy"})
    plt.title("LogReg CV Acc by penalty & C (top50)")
    plt.xlabel("C")
    plt.ylabel("Penalty")
    out = os.path.join(PLOTS_DIR, "logreg_cv_acc_top50.png")
    plt.tight_layout()
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")

# ─── MAIN ───────────────────────────────────────────────────────────────────
def main():
    ensure_plots_dir()
    df = load_data()
    print(f"Loaded {len(df)} rows from Spotify dataset.\n")

    print("→ Tuning Regression Pipeline")
    tune_regression(df)
    print("\n→ Tuning Classification Pipeline")
    tune_classification(df)

if __name__ == "__main__":
    main()

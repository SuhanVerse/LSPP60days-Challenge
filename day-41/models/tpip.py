#!/usr/bin/env python3
"""
day-41/models/tfidf_pipeline.py

Create a pipeline for TF-IDF vectorization and train a Logistic Regression
model to classify if a Spotify song title is in the top 10.

Steps:
- Load `smusic.csv`, treating first column as track_name
- Extract `track_name` and `is_top10` (target)
- Create pipeline: TfidfVectorizer + LogisticRegression
- Fit, evaluate accuracy, classification report, confusion matrix, ROC AUC
- Plot top words and ROC curve
"""

import warnings
from sklearn.exceptions import ConvergenceWarning

warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    roc_curve,
    auc
)

# ─── Paths ───────────────────────────────────────────────────────────────────
DATA_PATH = "/home/xlegion/RUST/LSPP60days-Challenge/day-41/data/smusic.csv"
PLOTS_DIR = "/home/xlegion/RUST/LSPP60days-Challenge/day-41/plots"

# ─── Setup ───────────────────────────────────────────────────────────────────
def ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)

# ─── Load Data ───────────────────────────────────────────────────────────────
def load_data():
    df = pd.read_csv(
        DATA_PATH,
        encoding="latin1",
        engine="python",
        on_bad_lines="skip",
        index_col=0
    )
    df.index.name = "track_name"
    df = df.reset_index()
    df.columns = df.columns.str.strip()
    if "All Time Rank" not in df.columns:
        raise ValueError("Required column 'All Time Rank' not found in dataset")
    df = df.rename(columns={"All Time Rank": "rank"})
    df = df.dropna(subset=["rank", "track_name"]);
    df["rank"] = df["rank"].astype(str).str.extract(r"(\d+)").astype(float)
    df["is_top10"] = (df["rank"] <= 10).astype(int)
    return df[["track_name", "is_top10"]]

# ─── Train & Evaluate ───────────────────────────────────────────────────────
def train_evaluate_pipeline(df):
    X = df["track_name"]
    y = df["is_top10"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    pipe = Pipeline([
        ("tfidf", TfidfVectorizer(stop_words="english", max_features=1000)),
        ("clf", LogisticRegression(solver="liblinear"))
    ])
    pipe.fit(Xtr, ytr)
    yprob = pipe.predict_proba(Xte)[:,1]
    ypred = (yprob >= 0.5).astype(int)

    acc = accuracy_score(yte, ypred)
    print(f"TF-IDF + LogReg Accuracy: {acc:.2f}")

    print("\nClassification Report:")
    print(classification_report(yte, ypred, digits=2))

    cm = confusion_matrix(yte, ypred)
    plt.figure(figsize=(4,3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Not Top10","Top10"],
                yticklabels=["Not Top10","Top10"])
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    fn_cm = os.path.join(PLOTS_DIR, "confusion_matrix.png")
    plt.tight_layout(); plt.savefig(fn_cm); plt.close()
    print(f"Saved {fn_cm}")

    # ROC Curve
    fpr, tpr, _ = roc_curve(yte, yprob)
    roc_auc = auc(fpr, tpr)
    plt.figure(figsize=(5,4))
    plt.plot(fpr, tpr, label=f"ROC curve (AUC = {roc_auc:.2f})")
    plt.plot([0,1],[0,1], linestyle='--', color='gray')
    plt.title("ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    fn_roc = os.path.join(PLOTS_DIR, "roc_curve.png")
    plt.tight_layout(); plt.savefig(fn_roc); plt.close()
    print(f"Saved {fn_roc}")

    return pipe

def plot_top_tfidf_words(pipe, top_n=15):
    vec = pipe.named_steps["tfidf"]
    clf = pipe.named_steps["clf"]
    words = vec.get_feature_names_out()
    coef = clf.coef_[0]
    top_idx = coef.argsort()[-top_n:][::-1]
    plt.figure(figsize=(6,4))
    sns.barplot(x=coef[top_idx], y=np.array(words)[top_idx], palette="flare")
    plt.title(f"Top {top_n} TF-IDF Words")
    plt.xlabel("Coefficient")
    fn = os.path.join(PLOTS_DIR, "top_tfidf_words.png")
    plt.tight_layout(); plt.savefig(fn); plt.close()
    print(f"Saved {fn}")


def main():
    ensure_plots_dir()
    df = load_data()
    print(f"Loaded {len(df)} songs.")
    pipe = train_evaluate_pipeline(df)
    plot_top_tfidf_words(pipe)

if __name__ == "__main__":
    main()

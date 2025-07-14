#!/usr/bin/env python3
"""
day-44/models/evaluate.py

Evaluate the content-based recommender using Precision@K, Recall@K, and MRR.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
DATA_PATH  = os.path.join(DAY_DIR, "data", "music.csv")
PLOTS_DIR  = os.path.join(DAY_DIR, "plots")
OUTPUTS    = os.path.join(DAY_DIR, "outputs")

# ─── Helpers ─────────────────────────────────────────────────────────────────
def ensure_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(OUTPUTS, exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)
    df.fillna("", inplace=True)
    # Combine metadata for vectorization
    df["combined"] = df["genre"] + " " + df["artist"] + " " + df["track_name"]
    return df

def build_similarity(df):
    vect = TfidfVectorizer(stop_words="english")
    tfidf = vect.fit_transform(df["combined"])
    return cosine_similarity(tfidf)

def get_recommendations(idx, sim_matrix, top_k=10):
    # return indices of top_k most similar (excluding self)
    scores = list(enumerate(sim_matrix[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_k+1]
    return [i for i,_ in scores]

# ─── Metric Computations ─────────────────────────────────────────────────────
def precision_at_k(relevant, recommended, k):
    # fraction of recommended[:k] in relevant
    return len(set(recommended[:k]) & relevant) / k

def recall_at_k(relevant, recommended, k):
    # fraction of relevant items retrieved in recommended[:k]
    return len(set(recommended[:k]) & relevant) / len(relevant) if relevant else 0

def reciprocal_rank(relevant, recommended):
    for rank, idx in enumerate(recommended, start=1):
        if idx in relevant:
            return 1.0 / rank
    return 0.0

# ─── Evaluation ───────────────────────────────────────────────────────────────
def evaluate(df, sim_matrix, ks=[1,5,10]):
    n = len(df)
    metrics = {f"P@{k}": [] for k in ks}
    metrics.update({f"R@{k}": [] for k in ks})
    metrics["MRR"] = []

    # Precompute relevant sets: same-genre indices (minus self)
    genre_to_indices = {}
    for idx, genre in enumerate(df["genre"]):
        genre_to_indices.setdefault(genre, set()).add(idx)

    for idx in range(n):
        relevant = genre_to_indices.get(df.at[idx, "genre"], set()) - {idx}
        recs = get_recommendations(idx, sim_matrix, top_k=max(ks))
        # record metrics
        for k in ks:
            metrics[f"P@{k}"].append(precision_at_k(relevant, recs, k))
            metrics[f"R@{k}"].append(recall_at_k(relevant, recs, k))
        metrics["MRR"].append(reciprocal_rank(relevant, recs))

    # aggregate
    summary = {m: np.mean(vals) for m, vals in metrics.items()}
    return summary

# ─── Plotting ─────────────────────────────────────────────────────────────────
def plot_metrics(summary):
    # Bar chart for P@K and R@K
    dfm = pd.DataFrame({
        m: v for m, v in summary.items() if m.startswith(("P@","R@"))
    }, index=[0]).T.reset_index()
    dfm.columns = ["metric", "value"]
    plt.figure(figsize=(6,4))
    import seaborn as sns
    sns.barplot(x="metric", y="value", data=dfm, palette="mako")
    plt.title("Precision@K & Recall@K")
    plt.ylim(0,1)
    plt.ylabel("Average")
    plt.xlabel("")
    fn = os.path.join(PLOTS_DIR, "precision_recall_at_k.png")
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved {fn}")

    # MRR as single bar
    plt.figure(figsize=(3,3))
    plt.bar(["MRR"], [summary["MRR"]], color="teal")
    plt.ylim(0,1)
    plt.title("Mean Reciprocal Rank")
    fn2 = os.path.join(PLOTS_DIR, "mrr.png")
    plt.tight_layout()
    plt.savefig(fn2)
    plt.close()
    print(f"Saved {fn2}")

# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    ensure_dirs()
    df = load_data()
    print(f"Loaded {len(df)} songs for evaluation.")

    sim_matrix = build_similarity(df)
    summary    = evaluate(df, sim_matrix, ks=[1,5,10])

    # Save numeric summary
    out_txt = os.path.join(OUTPUTS, "metrics_summary.txt")
    with open(out_txt, "w") as f:
        for m, v in summary.items():
            f.write(f"{m}: {v:.4f}\n")
    print(f"Saved metrics summary to {out_txt}")

    plot_metrics(summary)
    print("Day 44 evaluation complete.")

if __name__=="__main__":
    main()

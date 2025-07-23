#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
"""
day-53/models/evaluate_cf.py

Evaluate SVD collaborative‐filtering recommender using:
  - Precision@K, Recall@K
  - Mean Reciprocal Rank (MRR)
Plots metrics for K = [1,5,10] and saves per-user scores.
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
DATA_PATH  = os.path.join(DAY_DIR, "../day-52/data/user_plays.csv")
OUTPUT_DIR = os.path.join(DAY_DIR, "../day-53/outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Metrics ─────────────────────────────────────────────────────────────────
def precision_recall_at_k(predictions, k=10, threshold=1.0):
    """
    Return precision and recall at K for each user.
    threshold: minimal play_count to be considered 'relevant'
    """
    # Map user -> list of (est, true) pairs
    user_pred = {}
    for pred in predictions:
        user_pred.setdefault(pred.uid, []).append((pred.est, pred.r_ui))

    precisions = []
    recalls    = []
    for uid, scores in user_pred.items():
        # Sort descending by estimated score
        scores.sort(key=lambda x: x[0], reverse=True)
        topk = scores[:k]
        n_rel = sum((true >= threshold) for (_, true) in scores)
        n_rec_k = sum((true >= threshold) for (_, true) in topk)
        precisions.append( n_rec_k / k )
        recalls.append(    n_rec_k / n_rel if n_rel>0 else np.nan )
    return precisions, recalls

def mean_reciprocal_rank(predictions, threshold=1.0):
    """
    Compute Reciprocal Rank per user and return list.
    """
    user_pred = {}
    for pred in predictions:
        user_pred.setdefault(pred.uid, []).append((pred.est, pred.r_ui))

    mrrs = []
    for uid, scores in user_pred.items():
        # sort by est desc
        scores.sort(key=lambda x: x[0], reverse=True)
        rr = 0.0
        for rank, (_, true) in enumerate(scores, start=1):
            if true >= threshold:
                rr = 1.0 / rank
                break
        mrrs.append(rr)
    return mrrs

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    # Load and split data
    df = pd.read_csv(DATA_PATH)
    reader = Reader(rating_scale=(df.play_count.min(), df.play_count.max()))
    data = Dataset.load_from_df(df[['user_id','track_name','play_count']], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    # Train SVD
    algo = SVD(n_factors=20, n_epochs=15, random_state=42)
    algo.fit(trainset)
    preds = algo.test(testset)

    # Evaluate at K = 1, 5, 10
    ks = [1,5,10]
    metrics = []
    for k in ks:
        precs, recs = precision_recall_at_k(preds, k=k)
        metrics.append({
            'K': k,
            'Precision@K': np.nanmean(precs),
            'Recall@K':    np.nanmean(recs)
        })

    # Compute MRR
    mrrs = mean_reciprocal_rank(preds)
    metrics.append({
        'K': 'MRR',
        'Precision@K': np.nan,
        'Recall@K':    np.nan,
        'MRR': np.mean(mrrs)
    })

    # Save summary
    mdf = pd.DataFrame(metrics)
    mdf.to_csv(os.path.join(OUTPUT_DIR, 'cf_metrics.csv'), index=False)
    print("Saved cf_metrics.csv")

    # Plot Precision & Recall
    plt.figure(figsize=(5,3))
    plt.plot(ks, [m['Precision@K'] for m in metrics[:3]], marker='o', label='Precision@K')
    plt.plot(ks, [m['Recall@K']    for m in metrics[:3]], marker='s', label='Recall@K')
    plt.title('CF SVD Precision & Recall@K')
    plt.xlabel('K'); plt.ylabel('Score')
    plt.legend(); plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'cf_precision_recall.png'))
    plt.close()
    print("Saved cf_precision_recall.png")

    # Plot MRR
    plt.figure(figsize=(3,3))
    plt.bar(['MRR'], [metrics[3]['MRR']], color='skyblue')
    plt.title('Mean Reciprocal Rank')
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR,'cf_mrr.png'))
    plt.close()
    print("Saved cf_mrr.png")

if __name__ == "__main__":
    main()

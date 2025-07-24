#!/usr/bin/env python3
import matplotlib
matplotlib.use("Agg")
"""
day-54/models/knn_cf.py

Item‑based collaborative filtering via kNN on user_plays.csv:
 - Load user×track play counts
 - Build user–item matrix
 - Fit NearestNeighbors on item vectors
 - Generate top‑10 item recommendations for a sample user
 - Compute Precision@K (requires held‑out testset)
 - Plot similarity distribution and save outputs
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.neighbors import NearestNeighbors
from sklearn.model_selection import train_test_split

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
DATA_PATH  = os.path.join(DAY_DIR, "..", "data", "user_plays.csv")
PLOTS_DIR  = os.path.join(DAY_DIR, "..", "plots")
OUTPUT_CSV = os.path.join(DAY_DIR, "..", "outputs", "knn_recs.csv")

# ─── Helpers ─────────────────────────────────────────────────────────────────
def ensure_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

def load_data():
    df = pd.read_csv(DATA_PATH)
    df.dropna(subset=["user_id","track_name","play_count"], inplace=True)
    return df

def train_test_split_df(df, test_size=0.2):
    """Split by having some play events in test for each user."""
    train_rows, test_rows = [], []
    for uid, grp in df.groupby("user_id"):
        tr, te = train_test_split(grp, test_size=test_size, random_state=42)
        train_rows.append(tr); test_rows.append(te)
    return pd.concat(train_rows), pd.concat(test_rows)

def build_item_matrix(train_df):
    """Return item_vectors: items × users play-count matrix (sparse)"""
    pivot = train_df.pivot_table(index="track_name",
                                 columns="user_id",
                                 values="play_count",
                                 fill_value=0)
    return pivot, pivot.values

def fit_knn(item_vectors, k=10):
    knn = NearestNeighbors(metric="cosine", n_neighbors=k+1, algorithm="brute")
    knn.fit(item_vectors)
    return knn

def get_item_recs(knn, item_index, item_names, top_n=10):
    """Return top_n most similar items to the given item_index."""
    dists, idxs = knn.kneighbors(item_vectors[item_index].reshape(1,-1),
                                  n_neighbors=top_n+1)
    recs = [(item_names[i], 1 - dists[0][j])   # similarity = 1-cosine_distance
            for j,i in enumerate(idxs[0]) if i!=item_index]
    return recs[:top_n]

def precision_at_k(recs, test_df, user_id, k=10):
    """Compute P@k: fraction of recommended in user's test set."""
    true_items = set(test_df[test_df.user_id==user_id].track_name)
    pred_items = [t for t,_ in recs][:k]
    if not true_items: return np.nan
    return len(set(pred_items) & true_items) / k

# ─── Main ────────────────────────────────────────────────────────────────────
if __name__=="__main__":
    ensure_dirs()
    df = load_data()
    train_df, test_df = train_test_split_df(df)
    print(f"Train events: {len(train_df)}, Test events: {len(test_df)}")

    # Build item × user matrix
    item_df, item_vectors = build_item_matrix(train_df)
    item_names = item_df.index.tolist()

    # Fit kNN
    knn = fit_knn(item_vectors, k=10)
    print("kNN model trained on item vectors.")

    # Plot similarity distribution (pairwise on a sample of items)
    sample_idxs = np.random.choice(len(item_vectors), size=min(100, len(item_vectors)), replace=False)
    sims = []
    for idx in sample_idxs:
        recs = get_item_recs(knn, idx, item_names, top_n=10)
        sims.extend([sim for _,sim in recs])
    plt.figure(figsize=(5,3))
    sns.histplot(sims, bins=20, kde=True, color="teal")
    plt.title("Distribution of Item–Item Similarities")
    plt.xlabel("Cosine similarity")
    plt.tight_layout()
    sim_plot = os.path.join(PLOTS_DIR, "item_similarity_dist.png")
    plt.savefig(sim_plot); plt.close()
    print(f"Saved {sim_plot}")

    # Generate recommendations & compute Precision@10
    sample_user = train_df.user_id.unique()[0]
    user_seen = set(train_df[train_df.user_id==sample_user].track_name)
    recs = []
    for item in user_seen:
        idx = item_names.index(item)
        recs.extend(get_item_recs(knn, idx, item_names, top_n=5))
    # dedupe and keep top by similarity
    recs = sorted(dict(recs).items(), key=lambda x: x[1], reverse=True)[:10]
    rec_df = pd.DataFrame(recs, columns=["track_name","sim_score"])
    rec_df.insert(0, "user_id", sample_user)
    rec_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Recommendations saved to {OUTPUT_CSV}")

    p10 = precision_at_k(recs, test_df, sample_user, k=10)
    print(f"Precision@10 for user {sample_user}: {p10:.2f}")

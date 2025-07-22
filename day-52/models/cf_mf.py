#!/usr/bin/env python3
# ── Force non-interactive Agg backend to avoid Qt/_Stack errors ──
import matplotlib
matplotlib.use("Agg")

"""
day-52/models/cf_mf.py

Collaborative Filtering via SVD matrix factorization on user_plays.csv:
 - Load user x track play counts
 - Train–test split (80/20)
 - Fit Surprise SVD model
 - Evaluate RMSE on test set
 - Generate top-10 recommendations for a sample user
 - Save metrics and CSV output
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
from surprise import accuracy

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
DATA_PATH  = os.path.join(DAY_DIR, "data", "user_plays.csv")
PLOTS_DIR  = os.path.join(DAY_DIR, "plots")
OUTPUTS    = os.path.join(DAY_DIR, "outputs", "user_recs.csv")

# ... rest of your code unchanged ...

def ensure_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUTS), exist_ok=True)

def load_data():
    # Expect columns: user_id, track_name, play_count
    df = pd.read_csv(DATA_PATH)
    df = df.dropna(subset=['user_id','track_name','play_count'])
    return df

def train_svd(df):
    # Surprise needs a "rating scale"; we'll treat play_count as rating
    reader = Reader(rating_scale=(df.play_count.min(), df.play_count.max()))
    data   = Dataset.load_from_df(df[['user_id','track_name','play_count']], reader)
    trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

    algo = SVD(n_factors=50, n_epochs=20, verbose=False, random_state=42)
    algo.fit(trainset)
    preds = algo.test(testset)
    rmse  = accuracy.rmse(preds, verbose=False)
    return algo, preds, rmse

def plot_rmse(rmse):
    plt.figure(figsize=(4,3))
    sns.barplot(x=['SVD'], y=[rmse], palette='Blues_d')
    plt.ylabel('RMSE')
    plt.title('SVD Test RMSE')
    fn = os.path.join(PLOTS_DIR, 'svd_rmse.png')
    plt.tight_layout()
    plt.savefig(fn); plt.close()
    print(f"Saved {fn}")

def get_recommendations(algo, df, user_id, top_n=10):
    # All unique items
    all_tracks = df.track_name.unique()
    # Items user has already played
    seen = set(df[df.user_id==user_id].track_name)
    recs = []
    for track in all_tracks:
        if track in seen: continue
        recs.append((track, algo.predict(user_id, track).est))
    recs.sort(key=lambda x: x[1], reverse=True)
    return recs[:top_n]

def main():
    ensure_dirs()
    df = load_data()
    print(f"Loaded {len(df)} play events ({df.user_id.nunique()} users × {df.track_name.nunique()} tracks)")

    print("→ Training SVD model…")
    algo, preds, rmse = train_svd(df)
    print(f"Test RMSE: {rmse:.2f}")
    plot_rmse(rmse)

    # Generate recommendations for a sample user (first in list)
    sample_user = df.user_id.unique()[0]
    recs = get_recommendations(algo, df, sample_user, top_n=10)
    rec_df = pd.DataFrame(recs, columns=['track_name','predicted_play'])
    rec_df.insert(0, 'user_id', sample_user)
    rec_df.to_csv(OUTPUTS, index=False)
    print(f"Sample recommendations saved to {OUTPUTS}")

if __name__ == "__main__":
    main()

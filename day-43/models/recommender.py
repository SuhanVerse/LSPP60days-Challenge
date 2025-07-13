#!/usr/bin/env python3
"""
day-43/models/recommender.py

Build a content-based music recommender:
- Load cleaned metadata (genre, artist, track_name)
- Combine features into a text corpus
- Vectorize with TF-IDF
- Compute cosine similarity matrix
- Expose get_recommendations() function and CLI
- Save sample recommendations to CSV
- Visualize similarity heatmap for top songs
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ─── Paths ──────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
DATA_PATH  = os.path.join(DAY_DIR, "data", "music.csv")
OUTPUT_CSV = os.path.join(DAY_DIR, "outputs", "sample_recs.csv")
PLOTS_DIR  = os.path.join(DAY_DIR, "plots")

# ─── Core Functions ──────────────────────────────────────────────────────────

def load_data():
    df = pd.read_csv(DATA_PATH)
    for col in ("track_name","artist","genre"):
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    df[["track_name","artist","genre"]] = df[["track_name","artist","genre"]].fillna("")
    return df

def build_tfidf_matrix(df):
    df["combined"] = df["genre"] + " " + df["artist"] + " " + df["track_name"]
    vect = TfidfVectorizer(stop_words="english")
    tfidf = vect.fit_transform(df["combined"])
    return tfidf, vect

def compute_similarity(tfidf):
    return cosine_similarity(tfidf, tfidf)

def get_recommendations(title, df, sim_matrix, top_n=10):
    matches = df.index[df["track_name"].str.lower() == title.lower()]
    if len(matches)==0:
        print(f"Title '{title}' not found.")
        return df.iloc[0:0][["track_name","artist","genre"]].copy()
    idx = matches[0]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    rec_indices = [i for i,_ in sim_scores]
    recs = df.iloc[rec_indices][["track_name","artist","genre"]].copy()
    recs["score"] = [s for _,s in sim_scores]
    return recs

# ─── Visualization ───

def plot_similarity_heatmap(df, sim_matrix):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    top_songs = df["track_name"].head(10)
    subset_sim = sim_matrix[:10,:10]
    plt.figure(figsize=(8,6))
    sns.heatmap(subset_sim, xticklabels=top_songs, yticklabels=top_songs, 
                cmap="YlGnBu", annot=True, fmt=".2f")
    plt.title("Similarity Heatmap (Top 10 Songs)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plot_path = os.path.join(PLOTS_DIR, "similarity_heatmap_top10.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Saved plot to {plot_path}")

# ─── CLI & Sample Generation ─────────────────────────────────────────

def main():
    os.makedirs(os.path.join(DAY_DIR,"outputs"), exist_ok=True)
    df = load_data()
    tfidf, _ = build_tfidf_matrix(df)
    sim = compute_similarity(tfidf)

    if len(sys.argv)>1:
        title = " ".join(sys.argv[1:])
        recs = get_recommendations(title, df, sim, top_n=10)
        if not recs.empty:
            print(f"\nRecommendations for '{title}':\n")
            print(recs.to_string(index=False))
    else:
        samples = []
        for idx in range(min(5,len(df))):
            title = df.at[idx,"track_name"]
            recs  = get_recommendations(title, df, sim, top_n=5)
            recs.insert(0, "query", [title]*len(recs))
            samples.append(recs)
        all_samples = pd.concat(samples, ignore_index=True)
        all_samples.to_csv(OUTPUT_CSV, index=False)
        print(f"Sample recommendations saved to {OUTPUT_CSV}")
        plot_similarity_heatmap(df, sim)

if __name__=="__main__":
    main()

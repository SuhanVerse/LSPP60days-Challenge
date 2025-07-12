#!/usr/bin/env python3
"""
day-42/models/sentiment_analysis.py

Perform sentiment analysis on Spotify song titles (smusic.csv) using VADER:
- Compute compound sentiment scores for each title
- Plot distribution of sentiment
- Show top 10 most positive & negative titles
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.sentiment import SentimentIntensityAnalyzer

# ─── Paths ───────────────────────────────────────────────────────────────────
DATA_PATH = "/home/xlegion/RUST/LSPP60days-Challenge/day-42/data/smusic.csv"
PLOTS_DIR = "/home/xlegion/RUST/LSPP60days-Challenge/day-42/plots"

# ─── Setup ───────────────────────────────────────────────────────────────────
def ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)

def load_titles():
    # Read CSV, first col is track_name
    df = pd.read_csv(DATA_PATH, index_col=0, encoding="latin1", engine="python", on_bad_lines="skip")
    df.index.name = "track_name"
    df = df.reset_index()[["track_name"]]
    return df

def analyze_sentiment(df):
    sia = SentimentIntensityAnalyzer()
    df["compound"] = df["track_name"].apply(lambda t: sia.polarity_scores(str(t))["compound"])
    return df

# ─── Plotting ─────────────────────────────────────────────────────────────────
def plot_sentiment_distribution(df):
    plt.figure(figsize=(6,4))
    sns.histplot(df["compound"], bins=30, kde=True, color="purple")
    plt.title("Distribution of Title Sentiment (VADER Compound)")
    plt.xlabel("Compound Sentiment Score")
    plt.ylabel("Number of Songs")
    fn = os.path.join(PLOTS_DIR, "sentiment_distribution.png")
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved {fn}")

def show_top_extremes(df, n=10):
    top_pos = df.nlargest(n, "compound")
    top_neg = df.nsmallest(n, "compound")
    print(f"\nTop {n} Positive Titles:")
    print(top_pos[["track_name","compound"]].to_string(index=False))
    print(f"\nTop {n} Negative Titles:")
    print(top_neg[["track_name","compound"]].to_string(index=False))
    # Also save to CSV
    top_pos.to_csv(os.path.join(PLOTS_DIR,"top_positive_titles.csv"), index=False)
    top_neg.to_csv(os.path.join(PLOTS_DIR,"top_negative_titles.csv"), index=False)
    print(f"Saved top_positive_titles.csv & top_negative_titles.csv")

# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    ensure_plots_dir()
    df = load_titles()
    print(f"Loaded {len(df)} titles for sentiment analysis.")
    df = analyze_sentiment(df)
    plot_sentiment_distribution(df)
    show_top_extremes(df, n=10)
    print("Day 42 sentiment analysis complete.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
day-40/models/eda_analysis.py

Perform a meaningful exploratory analysis on smusic.csv:
- Top artists & albums
- Distribution of streams (linear & log scale)
- Correlation heatmap of numeric features
- Scatter: streams vs. popularity
"""
import warnings
from sklearn.exceptions import ConvergenceWarning


warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


DATA_PATH = "/home/xlegion/RUST/LSPP60days-Challenge/day-40/data/smusic.csv"
PLOTS_DIR = "/home/xlegion/RUST/LSPP60days-Challenge/day-40/plots"

# ─── Setup ───────────────────────────────────────────────────────────────────
def ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)

def load_data():
    # Read with latin1 to handle special chars
    df = pd.read_csv(
        DATA_PATH,
        encoding="latin1",
        engine="python",
        on_bad_lines="skip"
    )

    # Standardize column names
    df.columns = df.columns.str.strip()

    # Rename for convenience
    df = df.rename(columns={
        "All Time Rank":      "rank",
        "Spotify Streams":    "streams",
        "Spotify Popularity": "popularity",
        "Artist":             "artist",
        "Album Name":         "album",
        "Release Date":       "release_date"
    })

    # CLEAN 'streams': strip non-digits, replace empty → NaN, drop, then int
    df["streams"] = (
        df["streams"].astype(str)
                    .str.replace(r"[^\d]", "", regex=True)
                    .replace("", np.nan)
                    .astype(float)
    )
    df = df.dropna(subset=["streams"])
    df["streams"] = df["streams"].astype(int)

    # CLEAN 'popularity' if string
    if df["popularity"].dtype == object:
        df["popularity"] = (
            df["popularity"].astype(str)
                        .str.replace(r"[^\d]", "", regex=True)
                        .replace("", np.nan)
                        .astype(float)
        )
        df = df.dropna(subset=["popularity"])
        df["popularity"] = df["popularity"].astype(int)

    # Parse release year
    df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year

    return df

# ─── EDA Functions ───────────────────────────────────────────────────────────
def plot_top_counts(df, column, top_n=10):
    counts = df[column].value_counts().head(top_n)
    plt.figure(figsize=(6,4))
    sns.barplot(y=counts.index, x=counts.values, palette="crest")
    plt.title(f"Top {top_n} {column.title()}")
    plt.xlabel("Count")
    plt.ylabel(column.title())
    fn = os.path.join(PLOTS_DIR, f"top_{column}.png")
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved {fn}")

def plot_streams_distribution(df):
    # Linear scale
    plt.figure(figsize=(6,4))
    sns.histplot(df["streams"], bins=30, kde=False)
    plt.title("Streams Distribution (linear)")
    plt.xlabel("Streams")
    plt.ylabel("Count")
    fn1 = os.path.join(PLOTS_DIR, "streams_dist_linear.png")
    plt.tight_layout()
    plt.savefig(fn1)
    plt.close()
    print(f"Saved {fn1}")

    # Log scale
    plt.figure(figsize=(6,4))
    sns.histplot(np.log10(df["streams"]), bins=30, kde=False, color="orange")
    plt.title("Streams Distribution (log10)")
    plt.xlabel("log10(Streams)")
    plt.ylabel("Count")
    fn2 = os.path.join(PLOTS_DIR, "streams_dist_log.png")
    plt.tight_layout()
    plt.savefig(fn2)
    plt.close()
    print(f"Saved {fn2}")

def plot_correlation_heatmap(df):
    num_cols = ["streams", "popularity", "year"]
    corr = df[num_cols].corr()
    plt.figure(figsize=(4,3))
    sns.heatmap(corr, annot=True, cmap="vlag", center=0)
    plt.title("Correlation Heatmap")
    fn = os.path.join(PLOTS_DIR, "correlation_heatmap.png")
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved {fn}")

def plot_streams_vs_popularity(df):
    plt.figure(figsize=(6,4))
    sns.scatterplot(x="popularity", y="streams", data=df, alpha=0.6)
    plt.yscale("log")
    plt.title("Streams vs. Popularity")
    plt.xlabel("Popularity")
    plt.ylabel("Streams (log scale)")
    fn = os.path.join(PLOTS_DIR, "streams_vs_popularity.png")
    plt.tight_layout()
    plt.savefig(fn)
    plt.close()
    print(f"Saved {fn}")

# ─── Main ────────────────────────────────────────────────────────────────────
def main():
    ensure_plots_dir()
    df = load_data()
    print(f"Dataset loaded: {len(df)} rows, columns: {list(df.columns)}")

    # 1. Top artists & albums
    plot_top_counts(df, "artist", top_n=10)
    plot_top_counts(df, "album", top_n=10)

    # 2. Streams distribution
    plot_streams_distribution(df)

    # 3. Correlation among numeric features
    plot_correlation_heatmap(df)

    # 4. Streams vs. popularity
    plot_streams_vs_popularity(df)

    print("Day 40 EDA complete. Check the plots folder.")

if __name__ == "__main__":
    main()

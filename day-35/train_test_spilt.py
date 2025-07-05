#!/usr/bin/env python3
"""
day-35/train_test_baseline.py

Load MusicOSet (TSV) metadata and features, merge, then run baseline
regression and classification with visualizations.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyRegressor, DummyClassifier
from sklearn.metrics import mean_squared_error, accuracy_score, confusion_matrix

def load_musicoset():
    """Load & merge only the required columns from MusicOSet TSVs."""
    base = os.path.dirname(__file__)
    meta_dir = os.path.join(base, "data", "musicoset_metadata")
    feat_dir = os.path.join(base, "data", "musicoset_songfeatures")

    # Inspect columns
    print("Metadata columns:", pd.read_csv(os.path.join(meta_dir, "songs.csv"), sep='\t', nrows=0).columns.tolist())
    print("Feature columns:", pd.read_csv(os.path.join(feat_dir, "acoustic_features.csv"), sep='\t', nrows=0).columns.tolist())

    # Read only needed columns (TSV)
    meta_cols = ["song_id", "song_name", "artists", "popularity", "song_type"]
    meta = pd.read_csv(
        os.path.join(meta_dir, "songs.csv"),
        sep='\t',
        usecols=meta_cols,
        on_bad_lines="skip"
    ).rename(columns={
        "song_id": "track_id",
        "song_name": "track_name",
        # no release_year here, we'll treat 'popularity' or derive year from elsewhere
    })

    # Read features (TSV)
    feat_cols = ["song_id", "tempo", "danceability", "energy"]
    feats = pd.read_csv(
        os.path.join(feat_dir, "acoustic_features.csv"),
        sep='\t',
        usecols=feat_cols,
        on_bad_lines="skip"
    ).rename(columns={"song_id": "track_id"})

    # Merge
    df = pd.merge(meta, feats, on="track_id", how="inner")

    # For demonstration, create a synthetic 'year' column from popularity
    # (replace or drop as needed)
    df["year"] = 2000 + (df["popularity"] // 10)  # example mapping

    return df[["track_id","track_name","year","tempo","danceability","energy"]]

def regression_baseline(df):
    df = df.copy()
    df["title_length"] = df["track_name"].str.len()
    X = df[["year"]]
    y = df["title_length"]

    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=0.2,random_state=42)
    reg = DummyRegressor(strategy="mean").fit(Xtr,ytr)
    ypr = reg.predict(Xte)
    mse = mean_squared_error(yte,ypr)
    print(f"Regression Baseline MSE: {mse:.2f}")

    plt.figure(figsize=(6,4))
    sns.histplot(yte - ypr, kde=True)
    plt.title("Residuals: Actual–Predicted Title Length")
    plt.xlabel("Residual")
    plt.tight_layout()
    plt.savefig("plots/regression_residuals.png")
    plt.close()
    print("Saved plots/regression_residuals.png")

def classification_baseline(df):
    df = df.copy()
    df["is_recent"] = (df["year"]>=2000).astype(int)
    X = df[["year"]]
    y = df["is_recent"]

    Xtr, Xte, ytr, yte = train_test_split(X,y,test_size=0.2,random_state=42)
    clf = DummyClassifier(strategy="most_frequent").fit(Xtr,ytr)
    ypr = clf.predict(Xte)
    acc = accuracy_score(yte,ypr)
    print(f"Classification Baseline Accuracy: {acc:.2f}")

    cm = confusion_matrix(yte,ypr)
    plt.figure(figsize=(4,3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Not Recent","Recent"],
                yticklabels=["Not Recent","Recent"])
    plt.title("Confusion Matrix – Baseline")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()
    plt.savefig("plots/classification_cm.png")
    plt.close()
    print("Saved plots/classification_cm.png")

def main():
    os.makedirs("plots", exist_ok=True)
    df = load_musicoset()
    print("\n=== Regression Baseline ===")
    regression_baseline(df)
    print("\n=== Classification Baseline ===")
    classification_baseline(df)

if __name__=="__main__":
    main()

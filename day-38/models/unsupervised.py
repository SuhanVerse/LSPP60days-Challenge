#!/usr/bin/env python3
"""
day-38/models/unsupervised.py

Train & visualize K‑Means clusters and PCA on music.csv
(using only the numeric columns present in day-37/data/music.csv).
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Hardcode day-37 paths per your request
DATA_PATH = "/home/xlegion/RUST/LSPP60days-Challenge/day-38/data/music.csv"
PLOTS_DIR = "/home/xlegion/RUST/LSPP60days-Challenge/day-38/plots"

def ensure_plots_dir():
    os.makedirs(PLOTS_DIR, exist_ok=True)

def load_data():
    """
    Load music.csv and extract only the numeric features available:
    - year
    - title_length (computed from track_name)
    """
    df = pd.read_csv(DATA_PATH)
    if "track_name" not in df.columns or "year" not in df.columns:
        raise ValueError("music.csv must contain 'track_name' and 'year' columns")
    
    df["title_length"] = df["track_name"].astype(str).str.len()
    # We only have 'year' and 'title_length' as numeric features
    features = ["year", "title_length"]
    return df, df[features]

def run_kmeans(X, n_clusters=3):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    km = KMeans(n_clusters=n_clusters, random_state=42)
    labels = km.fit_predict(X_scaled)
    return X_scaled, labels, km

def plot_clusters_2d(X_scaled, labels, km):
    """
    Project to 2D via PCA and plot clusters + centroids.
    """
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)

    plt.figure(figsize=(6,5))
    sns.scatterplot(x=X_pca[:,0], y=X_pca[:,1], hue=labels, palette="tab10", s=50)
    centers = pca.transform(km.cluster_centers_)
    plt.scatter(centers[:,0], centers[:,1], c="black", s=200, marker="X", label="Centroids")
    plt.title("K‑Means Clusters in PCA Space")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.legend(title="Cluster", loc="best")
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "kmeans_pca_clusters.png")
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")

def plot_pca_variance(X_scaled):
    """
    Plot explained variance ratio for each PCA component.
    """
    n_features = X_scaled.shape[1]
    pca = PCA(n_components=n_features, random_state=42)
    pca.fit(X_scaled)
    var_ratio = pca.explained_variance_ratio_

    plt.figure(figsize=(6,4))
    sns.barplot(x=list(range(1, n_features+1)), y=var_ratio, color="skyblue")
    plt.plot(range(1, n_features+1), var_ratio.cumsum(), marker="o", color="orange")
    plt.title("PCA Explained Variance Ratio")
    plt.xlabel("Principal Component")
    plt.ylabel("Variance Ratio")
    plt.tight_layout()
    out = os.path.join(PLOTS_DIR, "pca_variance_ratio.png")
    plt.savefig(out)
    plt.close()
    print(f"Saved {out}")

def main():
    print()
    ensure_plots_dir()
    df, X = load_data()
    print(f"Loaded {len(df)} songs for clustering.")

    # Run K‑Means
    X_scaled, labels, km = run_kmeans(X, n_clusters=3)
    df["cluster"] = labels
    print("Cluster counts:\n", df["cluster"].value_counts())

    # Visualizations
    plot_clusters_2d(X_scaled, labels, km)
    plot_pca_variance(X_scaled)

    # Save assignments
    assignments = df[["track_name", "cluster"]]
    out_csv = os.path.join(PLOTS_DIR, "cluster_assignments.csv")
    assignments.to_csv(out_csv, index=False)
    print(f"Saved {out_csv}")
    print()
if __name__ == "__main__":
    main()

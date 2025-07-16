#!/usr/bin/env python3
"""
day-46/models/iris_dt.py

Train and evaluate a Decision Tree on the Iris dataset:
- Load data from sklearn.datasets
- Split into train/test
- Train DecisionTreeClassifier
- Evaluate with classification report & confusion matrix
- Plot the tree structure and feature pairplot
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
PLOTS_DIR  = os.path.join(DAY_DIR, "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

def load_data():
def load_data():
    iris = load_iris(as_frame=True)
    df = iris['frame']
    feature_names = iris['feature_names']
    target_names = iris['target_names']
    df.columns = list(feature_names) + ["target"]
    df["target_name"] = df["target"].map(lambda i: target_names[i])
    return df, feature_names, target_names
def train_and_evaluate(df, features):
    X = df[features]
    y = df["target"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    clf = DecisionTreeClassifier(max_depth=3, random_state=42)
    clf.fit(Xtr, ytr)
    ypred = clf.predict(Xte)

    # Metrics
    print("Classification Report:")
    print(classification_report(yte, ypred, target_names=df["target_name"].unique()))

    cm = confusion_matrix(yte, ypred)
    plt.figure(figsize=(4,3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=df["target_name"].unique(),
                yticklabels=df["target_name"].unique())
    plt.title("Confusion Matrix")
    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    out_cm = os.path.join(PLOTS_DIR, "iris_confusion_matrix.png")
    plt.tight_layout(); plt.savefig(out_cm); plt.close()
    print(f"Saved {out_cm}")

    return clf, Xte, yte

def plot_tree_structure(clf, feature_names, class_names):
    plt.figure(figsize=(8,6))
    plot_tree(clf,
              feature_names=feature_names,
              class_names=class_names,
              filled=True,
              rounded=True,
              fontsize=10)
    out_tree = os.path.join(PLOTS_DIR, "iris_decision_tree.png")
    plt.tight_layout(); plt.savefig(out_tree); plt.close()
    print(f"Saved {out_tree}")

def plot_pairplot(df, features):
    sns.pairplot(df, vars=features, hue="target_name", corner=True)
    out_pp = os.path.join(PLOTS_DIR, "iris_pairplot.png")
    plt.savefig(out_pp); plt.close()
    print(f"Saved {out_pp}")

def main():
    df, feature_names, target_names = load_data()
    print(f"Loaded Iris dataset: {len(df)} samples, features: {feature_names}")
    clf, _, _ = train_and_evaluate(df, feature_names)
    plot_tree_structure(clf, feature_names, target_names)
    plot_pairplot(df, feature_names)
    plot_pairplot(df, feature_names)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Train & evaluate Decision Tree and Random Forest models
for regression and classification on clean_music.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_squared_error,
    accuracy_score,
    roc_auc_score,
    roc_curve,
    confusion_matrix,
)

def load_data():
    path = ("/home/xlegion/RUST/LSPP60days-Challenge/day-37/data/music.csv")
    df = pd.read_csv(path)
    df["title_length"] = df["track_name"].str.len()
    df["is_recent"] = (df["year"] >= 2000).astype(int)
    return df

def plot_feature_importances(importances, feature_names, outpath, title):
    df_imp = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values("importance", ascending=False)
    plt.figure(figsize=(6,4))
    sns.barplot(x="importance", y="feature", data=df_imp, palette="viridis")
    plt.title(title)
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    print(f"Saved {outpath}")

def regression_trees(df):
    X = df[["year"]]
    y = df["title_length"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    # Decision Tree Regressor
    dt = DecisionTreeRegressor(max_depth=5, random_state=42)
    dt.fit(Xtr, ytr)
    ydt = dt.predict(Xte)
    mse_dt = mean_squared_error(yte, ydt)
    print(f"Decision Tree Regressor MSE: {mse_dt:.2f}")
    plot_feature_importances(
        dt.feature_importances_,
        X.columns,
        "/home/xlegion/RUST/LSPP60days-Challenge/day-37/plots/dt_reg_feature_importances.png",
        "DT Regressor Feature Importances"
    )

    # Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(Xtr, ytr)
    yrf = rf.predict(Xte)
    mse_rf = mean_squared_error(yte, yrf)
    print(f"Random Forest Regressor MSE: {mse_rf:.2f}")
    plot_feature_importances(
        rf.feature_importances_,
        X.columns,
        "/home/xlegion/RUST/LSPP60days-Challenge/day-37/plots/rf_reg_feature_importances.png",
        "RF Regressor Feature Importances"
    )

def classification_trees(df):
    X = df[["year"]]
    y = df["is_recent"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)

    # Decision Tree Classifier
    dtc = DecisionTreeClassifier(max_depth=5, random_state=42)
    dtc.fit(Xtr, ytr)
    ydt = dtc.predict(Xte)
    import numpy as np
    ydtp = np.array(dtc.predict_proba(Xte))[:,1]
    acc_dt = accuracy_score(yte, ydt)
    auc_dt = roc_auc_score(yte, ydtp)
    print(f"Decision Tree Classifier Accuracy: {acc_dt:.2f}, ROC AUC: {auc_dt:.2f}")
    plot_feature_importances(
        dtc.feature_importances_,
        X.columns,
        "/home/xlegion/RUST/LSPP60days-Challenge/day-37/plots/dt_clf_feature_importances.png",
        "DT Classifier Feature Importances"
    )
    # Confusion matrix
    cm = confusion_matrix(yte, ydt)
    plt.figure(figsize=(4,3))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=["Old","Recent"], yticklabels=["Old","Recent"])
    plt.title("DT Classifier Confusion Matrix")
    plt.tight_layout()
    plt.savefig("/home/xlegion/RUST/LSPP60days-Challenge/day-37/plots/dt_clf_confusion_matrix.png")
    plt.close()
    print("Saved ../plots/dt_clf_confusion_matrix.png")

    # Random Forest Classifier
    rfc = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=42)
    rfc.fit(Xtr, ytr)
    yrf = rfc.predict(Xte)
    yrfp = rfc.predict_proba(Xte)[:,1]
    acc_rf = accuracy_score(yte, yrf)
    auc_rf = roc_auc_score(yte, yrfp)
    print(f"Random Forest Classifier Accuracy: {acc_rf:.2f}, ROC AUC: {auc_rf:.2f}")
    plot_feature_importances(
        rfc.feature_importances_,
        X.columns,
        "/home/xlegion/RUST/LSPP60days-Challenge/day-37/plots/rf_clf_feature_importances.png",
        "RF Classifier Feature Importances"
    )
    # ROC curve
    fpr, tpr, _ = roc_curve(yte, yrfp)
    plt.figure(figsize=(6,4))
    plt.plot(fpr, tpr, label=f"AUC={auc_rf:.2f}")
    plt.plot([0,1],[0,1],'k--')
    plt.title("RF Classifier ROC Curve")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("/home/xlegion/RUST/LSPP60days-Challenge/day-37/plots/rf_clf_roc_curve.png")
    plt.close()
    print("Saved plots/rf_clf_roc_curve.png")
    print()

def main():
    df = load_data()
    print("\n=== Decision Tree & Random Forest Regression ===")
    regression_trees(df)
    print("\n=== Decision Tree & Random Forest Classification ===")
    classification_trees(df)

if __name__ == "__main__":
    main()

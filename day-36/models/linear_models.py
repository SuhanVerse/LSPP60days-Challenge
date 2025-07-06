#!/usr/bin/env python3
"""
Train & evaluate linear regression and logistic regression
on the clean_music dataset.
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, accuracy_score, roc_auc_score, roc_curve

def load_data():
    path = ("/home/xlegion/RUST/LSPP60days-Challenge/day-36/data/music.csv")
    df = pd.read_csv(path)
    df["title_length"] = df["track_name"].str.len()
    df["is_recent"] = (df["year"] >= 2000).astype(int)
    return df

def regression(df):
    X = df[["year"]]
    y = df["title_length"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(Xtr, ytr)
    ypr = model.predict(Xte)
    
    mse = mean_squared_error(yte, ypr)
    print(f"Linear Regression MSE: {mse:.2f}")
    
    # Plot actual vs predicted
    plt.figure(figsize=(6,4))
    sns.scatterplot(x=yte, y=ypr)
    plt.plot([yte.min(), yte.max()], [yte.min(), yte.max()], 'r--')
    plt.xlabel("Actual Title Length")
    plt.ylabel("Predicted Title Length")
    plt.title("Linear Regression: Actual vs Predicted")
    os.makedirs("../plots", exist_ok=True)
    plt.tight_layout()
    plt.savefig("/home/xlegion/RUST/LSPP60days-Challenge/day-36/plots/linreg_actual_vs_pred.png")
    plt.close()
    print("Saved plots/linreg_actual_vs_pred.png")

def classification(df):
    X = df[["year"]]
    y = df["is_recent"]
    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression(solver='liblinear')
    model.fit(Xtr, ytr)
    ypr = model.predict(Xte)
    yproba = model.predict_proba(Xte)[:,1]
    
    acc = accuracy_score(yte, ypr)
    auc = roc_auc_score(yte, yproba)
    print(f"Logistic Regression Accuracy: {acc:.2f}")
    print(f"Logistic Regression ROC AUC: {auc:.2f}")
    
    # Plot ROC curve
    fpr, tpr, _ = roc_curve(yte, yproba)
    plt.figure(figsize=(6,4))
    plt.plot(fpr, tpr, label=f"AUC={auc:.2f}")
    plt.plot([0,1],[0,1],'k--')
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.title("ROC Curve")
    plt.legend(loc="lower right")
    plt.tight_layout()
    plt.savefig("/home/xlegion/RUST/LSPP60days-Challenge/day-36/plots/logreg_roc_curve.png")
    plt.close()
    print("Saved plots/logreg_roc_curve.png")
    print()

def main():
    df = load_data()
    print("\n=== Linear Regression ===")
    regression(df)
    print("\n=== Logistic Regression ===")
    classification(df)

if __name__ == "__main__":
    main()

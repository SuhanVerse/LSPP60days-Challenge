#!/usr/bin/env python3
"""
day-45/models/neural_intro.py

Train a simple MLP to classify Top‑10 tracks using Keras:
- Inputs: normalized 'position'
- Target: is_top10 (1 if rank ≤ 10 else 0)
- Architecture: 2 hidden layers of 16 neurons with ReLU
- Visualize training loss & accuracy
- Save model and plots
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping

# ─── Paths ───────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
DATA_PATH  = os.path.join(DAY_DIR, "data", "smusic.csv")
PLOTS_DIR  = os.path.join(DAY_DIR, "plots")
MODEL_DIR  = os.path.join(DAY_DIR, "saved_models")

def ensure_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)

def load_and_preprocess():
    # Load with latin1 to handle encoding
    df = pd.read_csv(DATA_PATH, encoding="latin1", engine="python", on_bad_lines="skip")
    # Clean and rename
    df.columns = df.columns.str.strip()
    df = df.rename(columns={"All Time Rank": "position"})
    # Extract numeric rank
    df["position"] = df["position"].astype(str).str.extract(r"(\d+)").astype(float)
    df = df.dropna(subset=["position"])
    # Target: top‑10 track?
    df["is_top10"] = (df["position"] <= 10).astype(int)
    # Input feature: normalized position
    pos = df["position"].values.reshape(-1,1)
    # Min‑max normalize to [0,1]
    pos_norm = (pos - pos.min()) / (pos.max() - pos.min())
    return pos_norm, df["is_top10"].values

def build_model(input_shape):
    model = Sequential([
        Dense(16, activation="relu", input_shape=input_shape),
        Dense(16, activation="relu"),
        Dense(1, activation="sigmoid")
    ])
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model

def plot_history(hist):
    # Loss
    plt.figure(figsize=(5,3))
    plt.plot(hist.history["loss"], label="train loss")
    plt.plot(hist.history["val_loss"], label="val loss")
    plt.title("Training & Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Binary Crossentropy")
    plt.legend()
    fn = os.path.join(PLOTS_DIR, "nn_loss.png")
    plt.tight_layout(); plt.savefig(fn); plt.close()
    print(f"Saved {fn}")

    # Accuracy
    plt.figure(figsize=(5,3))
    plt.plot(hist.history["accuracy"], label="train acc")
    plt.plot(hist.history["val_accuracy"], label="val acc")
    plt.title("Training & Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    fn = os.path.join(PLOTS_DIR, "nn_accuracy.png")
    plt.tight_layout(); plt.savefig(fn); plt.close()
    print(f"Saved {fn}")

def main():
    ensure_dirs()
    X, y = load_and_preprocess()
    # Split
    idx = np.arange(len(X))
    np.random.seed(42)
    np.random.shuffle(idx)
    train_idx = idx[: int(0.8*len(idx))]
    val_idx   = idx[int(0.8*len(idx)):]
    X_train, X_val = X[train_idx], X[val_idx]
    y_train, y_val = y[train_idx], y[val_idx]

    # Build & train
    model = build_model(input_shape=(1,))
    es = EarlyStopping(monitor="val_loss", patience=5, restore_best_weights=True)
    hist = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=50,
        batch_size=8,
        callbacks=[es],
        verbose=2
    )

    loss, acc = model.evaluate(X_val, y_val, verbose=0)
    print(f"\nValidation Loss: {loss:.3f}, Accuracy: {acc:.3f}")


    plot_history(hist)


    model_path = os.path.join(MODEL_DIR, "top10_classifier.h5")
    model.save(model_path)
    print(f"Saved model to {model_path}")

if __name__ == "__main__":
    main()


"""
day-47/models/imdb_text_classifier.py

Train a simple neural network on the Keras IMDB sentiment dataset:
- Load IMDB reviews (top 10k words)
- Pad sequences to fixed length
- Define Embedding + 1D‑Conv + GlobalPool + Dense architecture
- Train & validate
- Evaluate on test set
- Plot loss & accuracy curves
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras import layers, models, preprocessing

# ─── Paths & Hyperparams ─────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(__file__)
DAY_DIR    = os.path.dirname(SCRIPT_DIR)
PLOTS_DIR  = os.path.join(DAY_DIR, "plots")
MODEL_PATH = os.path.join(DAY_DIR, "models", "imdb_cnn.h5")

VOCAB_SIZE    = 10000    # top 10k words
MAX_LEN       = 200      # max words per review
EMBED_DIM     = 128
BATCH_SIZE    = 64
EPOCHS        = 5

def ensure_dirs():
    os.makedirs(PLOTS_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

def load_and_preprocess():
    # Load IMDB data
    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.imdb.load_data(num_words=VOCAB_SIZE)
    # Pad/truncate reviews
    x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=MAX_LEN, padding="post", truncating="post")
    x_test  = preprocessing.sequence.pad_sequences(x_test,  maxlen=MAX_LEN, padding="post", truncating="post")
    return (x_train, y_train), (x_test, y_test)

def build_model():
    model = models.Sequential([
        layers.Embedding(VOCAB_SIZE, EMBED_DIM, input_length=MAX_LEN),
        layers.Conv1D(128, 5, activation="relu"),
        layers.GlobalMaxPooling1D(),
        layers.Dense(64, activation="relu"),
        layers.Dense(1, activation="sigmoid")
    ])
    model.compile(optimizer="adam",
                  loss="binary_crossentropy",
                  metrics=["accuracy"])
    return model

def plot_history(hist):
    # Loss
    plt.figure(figsize=(5,3))
    plt.plot(hist.history["loss"], label="train_loss")
    plt.plot(hist.history["val_loss"], label="val_loss")
    plt.title("Loss")
    plt.xlabel("Epoch"); plt.ylabel("Loss")
    plt.legend()
    fn = os.path.join(PLOTS_DIR, "imdb_loss.png")
    plt.savefig(fn); plt.close()
    print(f"Saved {fn}")

    # Accuracy
    plt.figure(figsize=(5,3))
    plt.plot(hist.history["accuracy"], label="train_acc")
    plt.plot(hist.history["val_accuracy"], label="val_acc")
    plt.title("Accuracy")
    plt.xlabel("Epoch"); plt.ylabel("Acc")
    plt.legend()
    fn = os.path.join(PLOTS_DIR, "imdb_acc.png")
    plt.savefig(fn); plt.close()
    print(f"Saved {fn}")

def main():
    ensure_dirs()
    (x_train, y_train), (x_test, y_test) = load_and_preprocess()
    print(f"Training samples: {len(x_train)}, Test samples: {len(x_test)}")

    model = build_model()
    model.summary()

    # Train
    hist = model.fit(
        x_train, y_train,
        epochs=EPOCHS,
        batch_size=BATCH_SIZE,
        validation_split=0.2,
        verbose=2
    )

    # Evaluate
    loss, acc = model.evaluate(x_test, y_test, verbose=0)
    print(f"\nTest Accuracy: {acc:.3f}, Loss: {loss:.3f}")

    # Visualize
    plot_history(hist)

    # Save model
    model.save(MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")

if __name__ == "__main__":
    main()

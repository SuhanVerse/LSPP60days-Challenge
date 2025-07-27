
# models/day56_ncf_model.py
import warnings
warnings.filterwarnings(
    "ignore",
    message="A NumPy version.*required for this version of SciPy",
    category=UserWarning
)
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # TensorFlow only errors

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import layers, Model
from sklearn.metrics import roc_auc_score, accuracy_score
from data_prep import load_and_binarize, train_test_implicit
import pickle
import matplotlib
matplotlib.use("Agg")

# 1) Load & prepare data
raw_df = load_and_binarize('data/ratings.csv', threshold=4.0)
train_df, test_df = train_test_implicit(raw_df, test_size=0.2)

# Map user/item IDs to contiguous indices
def create_id_mappings(df):
    user_ids = df.user_id.unique()
    item_ids = df.track_id.unique()
    return {u:i for i,u in enumerate(user_ids)}, {i:j for j,i in enumerate(item_ids)}

user2idx, item2idx = create_id_mappings(raw_df)

train_df['u_idx'] = train_df.user_id.map(user2idx)
train_df['i_idx'] = train_df.track_id.map(item2idx)
test_df ['u_idx'] = test_df.user_id.map(user2idx)
test_df ['i_idx'] = test_df.track_id.map(item2idx)

n_users = len(user2idx)
n_items = len(item2idx)

# 2) Build the NCF model
EMB_SIZE = 32
user_input = layers.Input(shape=(), name='user')
item_input = layers.Input(shape=(), name='item')
user_emb = layers.Embedding(n_users, EMB_SIZE, name='user_emb')(user_input)
item_emb = layers.Embedding(n_items, EMB_SIZE, name='item_emb')(item_input)
u_flat = layers.Flatten()(user_emb)
i_flat = layers.Flatten()(item_emb)
x = layers.Multiply()([u_flat, i_flat])
x = layers.Dense(64, activation='relu')(x)
x = layers.Dense(32, activation='relu')(x)
output = layers.Dense(1, activation='sigmoid')(x)
model = Model(inputs=[user_input, item_input], outputs=output)
model.compile(optimizer='adam', loss='binary_crossentropy')
model.summary()

# 3) Train with history
history = model.fit(
    x=[train_df.u_idx, train_df.i_idx],
    y=train_df.interaction,
    batch_size=1024,
    epochs=5,
    validation_split=0.1,
    verbose=2
)

# Plot training & validation loss
plt.figure()
plt.plot(history.history['loss'], label='train_loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.title('Training and Validation Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.tight_layout()
plt.savefig('models/ncf_loss.png')
plt.close()

# 4) Evaluate on test set
preds = model.predict([test_df.u_idx, test_df.i_idx]).flatten()
# Handle single-class case
unique_labels = np.unique(test_df.interaction)
if len(unique_labels) < 2:
    print("Only one class present in test labels; skipping ROC AUC.")
    auc = None
    # Fallback: report accuracy at threshold 0.5
    bin_preds = (preds >= 0.5).astype(int)
    acc = accuracy_score(test_df.interaction, bin_preds)
    print(f"Test Accuracy: {acc:.4f}")
else:
    auc = roc_auc_score(test_df.interaction, preds)
    print(f"Test AUC: {auc:.4f}")

# Plot ROC AUC if available
if auc is not None:
    from sklearn.metrics import roc_curve
    fpr, tpr, _ = roc_curve(test_df.interaction, preds)
    plt.figure()
    plt.plot(fpr, tpr)
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.tight_layout()
    plt.savefig('models/ncf_roc_curve.png')
    plt.close()

# 5) Save model & mappings
model.save('models/ncf_implicit.h5')
with open('models/user2idx.pkl','wb') as f: pickle.dump(user2idx, f)
with open('models/item2idx.pkl','wb') as f: pickle.dump(item2idx, f)

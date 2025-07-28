# models/day57_ncf_ranking.py

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
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pickle
import random  # for safe negative sampling
from tensorflow.keras.models import load_model
from data_prep import load_and_binarize, train_test_implicit


def predict_score(model, user2idx, item2idx, u, i):
    return model.predict([
        np.array([user2idx[u]]),
        np.array([item2idx[i]])
    ], verbose=0).flatten()[0]


def hit_rate_at_k(ranked, true_i, k):
    return int(true_i in ranked[:k])


def ndcg_at_k(ranked, true_i, k):
    if true_i in ranked[:k]:
        rank = ranked.index(true_i) + 1
        return 1 / np.log2(rank + 1)
    return 0


def evaluate_ranking(model, user2idx, item2idx, samples, K_list=[5,10,20]):
    results = {K: {'hr': [], 'ndcg': []} for K in K_list}
    for uid, pos_iid, negs in samples:
        candidates = [pos_iid] + negs
        scores = {
            iid: predict_score(model, user2idx, item2idx, uid, iid)
            for iid in candidates
        }
        ranked = sorted(scores, key=scores.get, reverse=True)
        for K in K_list:
            results[K]['hr'].append(hit_rate_at_k(ranked, pos_iid, K))
            results[K]['ndcg'].append(ndcg_at_k(ranked, pos_iid, K))

    return {
        K: {
            f'HR@{K}': np.mean(results[K]['hr']),
            f'NDCG@{K}': np.mean(results[K]['ndcg'])
        }
        for K in K_list
    }


def main():
    print("🔥 Starting ranking evaluation…")
    # 1) Load & prepare test interactions
    raw = load_and_binarize('data/ratings.csv', threshold=4.0)
    _, test_df = train_test_implicit(raw, test_size=0.2)

    print("Stating load mappings and model")

    # 2) Load mappings and model
    with open('models/user2idx.pkl', 'rb') as f:
        user2idx = pickle.load(f)
    with open('models/item2idx.pkl', 'rb') as f:
        item2idx = pickle.load(f)
    model = load_model('models/ncf_implicit.h5')
    print("Stating negative sampling")

    # 3) Negative sampling
    all_item_ids = list(item2idx.keys())
    neg_samples = []
    for uid, iid in test_df[['user_id','track_id']].itertuples(index=False):
        user_interacted = set(raw[raw.user_id == uid]['track_id'])
        neg_candidates = list(set(all_item_ids) - user_interacted)
        M = min(99, len(neg_candidates))
        negs = random.sample(neg_candidates, M)
        neg_samples.append((uid, iid, negs))
    print("Stating evaluation of ranking metrics")

    # 4) Evaluate ranking metrics
    K_list = [5, 10, 20]
    metrics = evaluate_ranking(model, user2idx, item2idx, neg_samples, K_list)
    print("Print evaluation of ranking metrics")

    # 5) Print and save metrics
    print("Ranking Metrics:")
    for K, vals in metrics.items():
        print(f" K={K}: HR={vals[f'HR@{K}']:.4f}, NDCG={vals[f'NDCG@{K}']:.4f}")

    pd.DataFrame(metrics).T.to_csv('models/ncf_ranking_metrics.csv')

    # 6) Plot HR@K & NDCG@K vs K
    hr_vals = [metrics[K][f'HR@{K}'] for K in K_list]
    ndcg_vals = [metrics[K][f'NDCG@{K}'] for K in K_list]
    print("plot")
    plt.figure()
    plt.plot(K_list, hr_vals, marker='o', label='HR@K')
    plt.plot(K_list, ndcg_vals, marker='o', label='NDCG@K')
    plt.title('Ranking Metrics vs K')
    plt.xlabel('K')
    plt.ylabel('Score')
    plt.legend()
    plt.tight_layout()
    plt.savefig('models/ncf_ranking_plot.png')
    plt.close()


if __name__ == "__main__":
    main()
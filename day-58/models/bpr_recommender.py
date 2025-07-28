import pandas as pd
import numpy as np
from scipy.sparse import coo_matrix
from implicit.bpr import BayesianPersonalizedRanking
from data_prep_bpr import build_sparse_interaction
import matplotlib.pyplot as plt
import pickle
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Custom NDCG implementation since sklearn.metrics.ndcg_score is unavailable
def ndcg_score(y_true, y_score):
    dcg = 0.0
    for i, rel in enumerate(y_score):
        dcg += rel / np.log2(i + 2)
    ideal = sorted(y_true, reverse=True)
    idcg = 0.0
    for i, rel in enumerate(ideal):
        idcg += rel / np.log2(i + 2)
    return dcg / idcg if idcg > 0 else 0.0

# 1) Read full ratings to get every user & item
full_ratings = pd.read_csv('data/ratings.csv')
all_user_ids = full_ratings.user_id.unique()
all_item_ids = full_ratings.track_id.unique()
user_map = {u:i for i, u in enumerate(all_user_ids)}
item_map = {i:j for j, i in enumerate(all_item_ids)}
n_users, n_items = len(user_map), len(item_map)

# 2) Extract only the “liked” interactions
interactions = full_ratings[full_ratings.rating >= 4.0][['user_id','track_id']]

# 3) Split each user's liked interactions into train/test
train_rows, train_cols = [], []
test_rows,  test_cols  = [], []

for uid, group in interactions.groupby('user_id'):
    u_idx = user_map[uid]
    item_idxs = group.track_id.map(item_map).tolist()
    if len(item_idxs) < 2:
        train_items = item_idxs
        test_items  = []
    else:
        random.shuffle(item_idxs)
        cut = max(1, int(0.5 * len(item_idxs)))   # instead of 0.2
        test_items, train_items = item_idxs[:cut], item_idxs[cut:]
    train_rows.extend([u_idx]*len(train_items))
    train_cols.extend(train_items)
    test_rows.extend([u_idx]*len(test_items))
    test_cols.extend(test_items)

# 4) Build CSR matrices (shape = n_users × n_items)
train_csr = coo_matrix(
    (np.ones(len(train_rows)), (train_rows, train_cols)),
    shape=(n_users, n_items)
).tocsr()

test_csr = coo_matrix(
    (np.ones(len(test_rows)), (test_rows, test_cols)),
    shape=(n_users, n_items)
).tocsr()

# full_csr used for filtering known positives
full_csr = build_sparse_interaction(interactions, user_map, item_map).tocsr()
# 5) Train BPR
bpr = BayesianPersonalizedRanking(factors=100, iterations=300)
bpr.fit(train_csr)

# 6) Recommendation & evaluation helpers
def get_user_recs(model, u, N, filter_mat):
    user_items = filter_mat[u]
    recs = model.recommend(u, user_items, N=N, filter_already_liked_items=True)

    # Case 1: implicit >=0.7 returns tuple (ids, scores)
    if isinstance(recs, tuple) and len(recs) == 2:
        item_ids, scores = recs
        return list(item_ids)

    # Case 2: older versions return list of (id, score)
    if isinstance(recs, list) and all(isinstance(x, tuple) for x in recs):
        return [item for item, _ in recs]

    raise ValueError(f"Unexpected recommendation structure: {recs}")

def evaluate_bpr(test_mat, model, filter_mat, Ks=[5, 10, 20]):
    results = {K: {'hr': [], 'ndcg': []} for K in Ks}
    n_users = test_mat.shape[0]
    for u in range(n_users):
        true_items = test_mat[u].indices
        if len(true_items) == 0:
            continue
        
        recs = get_user_recs(model, u, max(Ks), filter_mat)
        print(f"User {u}, true: {true_items}, recs: {recs[:10]}")  # <--- DEBUG
        
        for K in Ks:
            hr_val = int(any(i in recs[:K] for i in true_items))
            rel = np.array([1 if i in true_items else 0 for i in recs[:K]])
            ndcg_val = ndcg_score(rel, rel) if rel.sum() > 0 else 0
            results[K]['hr'].append(hr_val)
            results[K]['ndcg'].append(ndcg_val)
    return {    
        K: {
            f'HR@{K}': np.mean(results[K]['hr']),
            f'NDCG@{K}': np.mean(results[K]['ndcg'])
        } for K in Ks
    }

    

# 7) Evaluate & persist
metrics = evaluate_bpr(test_csr, bpr, full_csr, Ks=[5,10,20])

print("BPR Ranking Metrics:")
for K,m in metrics.items():
    print(f" K={K}: HR={m[f'HR@{K}']:.4f}, NDCG={m[f'NDCG@{K}']:.4f}")

pd.DataFrame(metrics).T.to_csv('models/bpr_metrics.csv', index_label='K')

# 8) Visualize
Ks = list(metrics)
hr_vals = [metrics[K][f'HR@{K}'] for K in Ks]
ndcg_vals = [metrics[K][f'NDCG@{K}'] for K in Ks]

plt.figure()
plt.bar([k-0.25 for k in Ks], hr_vals,  width=0.4, label='HR@K')
plt.bar([k+0.25 for k in Ks], ndcg_vals, width=0.4, label='NDCG@K')
plt.xticks(Ks)
plt.xlabel('K')
plt.ylabel('Score')
plt.title('BPR Ranking Metrics')
plt.legend()
plt.tight_layout()
plt.savefig('models/bpr_ranking_plot.png')
plt.close()

# 9) Save model
with open('models/bpr_model.pkl','wb') as f:
    pickle.dump(bpr,f)

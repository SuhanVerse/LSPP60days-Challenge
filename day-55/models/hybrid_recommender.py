# models/day55_hybrid_recommender.py

import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pickle
from collections import defaultdict
import matplotlib
matplotlib.use("Agg")

# Optional: suppress the SciPy/NumPy version warning
warnings.filterwarnings(
    "ignore",
    message="A NumPy version.*required for this version of SciPy",
    category=UserWarning,
)

def load_data():
    tracks = pd.read_csv('data/tracks.csv')
    ratings = pd.read_csv('data/ratings.csv')
    return tracks, ratings

tracks_df, ratings_df = load_data()

def build_tfidf(tracks):
    tfidf = TfidfVectorizer(
        analyzer='word',
        ngram_range=(1, 2),
        stop_words='english'
    )
    # Combine title and genre into a single corpus per track
    corpus = (tracks['title'].fillna('') + ' ' + tracks['genre'].fillna(''))
    tfidf_matrix = tfidf.fit_transform(corpus)
    return tfidf, tfidf_matrix

tfidf_vect, tfidf_mtx = build_tfidf(tracks_df)

# Precompute pairwise cosine similarities between all items
cosine_mtx = cosine_similarity(tfidf_mtx, tfidf_mtx)

def get_content_scores(track_id, tracks, cosine_mtx):
    idx = tracks.index[tracks['track_id'] == track_id].tolist()[0]
    sim_scores = list(enumerate(cosine_mtx[idx]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    return [(tracks.iloc[i]['track_id'], score) for i, score in sim_scores]

def train_svd(ratings, rating_scale=(1, 5), test_size=0.2, random_state=42):
    reader = Reader(rating_scale=rating_scale)
    data = Dataset.load_from_df(
        ratings[['user_id', 'track_id', 'rating']],
        reader
    )
    trainset, testset = train_test_split(
        data,
        test_size=test_size,
        random_state=random_state
    )
    algo = SVD(n_factors=50, lr_all=0.005, reg_all=0.02)
    algo.fit(trainset)
    return algo, testset

# Train the SVD and get the testset back
svd_model, testset = train_svd(ratings_df)

def get_cf_score(user_id, track_id, algo):
    """Predict a normalized CF score (0 to 1) for a given user and track."""
    return algo.predict(user_id, track_id).est / 5.0

def get_hybrid_recs(user_id, tracks, cosine_mtx, algo,
                    ratings, top_n=10, alpha=0.7):
    """
    Blend Collaborative Filtering and Content-Based scores:
      hybrid = α * CF_score + (1-α) * Content_score
    """
    rated_tids = set(ratings[ratings.user_id == user_id]['track_id'])
    candidates = [tid for tid in tracks['track_id'] if tid not in rated_tids]

    user_ratings = ratings[ratings.user_id == user_id]
    n_rated = len(user_ratings)

    recs = []
    for tid in candidates:
        content_score = 0.0
        for _, row in user_ratings.iterrows():
            sim = dict(get_content_scores(row.track_id, tracks, cosine_mtx)).get(tid, 0.0)
            content_score += sim * (row.rating / 5.0)
        if n_rated > 0:
            content_score /= n_rated

        cf_score = get_cf_score(user_id, tid, algo)
        hybrid_score = alpha * cf_score + (1 - alpha) * content_score
        recs.append((tid, hybrid_score))

    recs.sort(key=lambda x: x[1], reverse=True)
    return recs[:top_n]

# Example: print top‑10 hybrid recs for user 123
user_recs = get_hybrid_recs(
    user_id=123,
    tracks=tracks_df,
    cosine_mtx=cosine_mtx,
    algo=svd_model,
    ratings=ratings_df,
    top_n=10,
    alpha=0.7
)
print("Top‑10 hybrid recs:", user_recs)

# Plot hybrid recommendation scores for the example user
user_ids, scores = zip(*user_recs)
plt.figure()
plt.bar(range(len(scores)), scores)
plt.xticks(range(len(scores)), user_ids, rotation=45)
plt.xlabel('Track ID')
plt.ylabel('Hybrid Score')
plt.title('Top-10 Hybrid Recommendation Scores for User 123')
plt.tight_layout()
plt.savefig('models/hybrid_score_dist.png')
plt.close()

def precision_recall_at_k(predictions, k=10, threshold=4.0):
    user_true = defaultdict(set)
    user_pred = defaultdict(list)

    for uid, iid, true_r, est, _ in predictions:
        if true_r >= threshold:
            user_true[uid].add(iid)
        user_pred[uid].append((iid, est))

    precisions, recalls = [], []
    for uid, preds in user_pred.items():
        preds.sort(key=lambda x: x[1], reverse=True)
        top_k = [iid for iid, _ in preds[:k]]
        true_set = user_true.get(uid, set())

        n_rec_k = len(top_k)
        n_rel = len(true_set)
        n_rel_and_rec_k = len(set(top_k) & true_set)

        precisions.append(n_rel_and_rec_k / n_rec_k if n_rec_k else 0)
        recalls.append(n_rel_and_rec_k / n_rel if n_rel else 0)

    return np.mean(precisions), np.mean(recalls)

# Build hybrid predictions on the held‑out testset
hybrid_preds = []
for uid, iid, true_r in testset:
    full_scores = dict(get_hybrid_recs(
        user_id=uid,
        tracks=tracks_df,
        cosine_mtx=cosine_mtx,
        algo=svd_model,
        ratings=ratings_df,
        top_n=len(tracks_df),
        alpha=0.7
    ))
    est = full_scores.get(iid, svd_model.predict(uid, iid).est / 5.0) * 5.0
    hybrid_preds.append((uid, iid, true_r, est, None))

prec, rec = precision_recall_at_k(hybrid_preds, k=10)
print(f"Hybrid Precision@10: {prec:.4f}, Recall@10: {rec:.4f}")

# Plot precision and recall
plt.figure()
plt.bar(['Precision@10', 'Recall@10'], [prec, rec])
plt.title('Hybrid Precision and Recall at K=10')
plt.ylabel('Score')
plt.tight_layout()
plt.savefig('models/hybrid_pr.png')
plt.close()

# Persist models & metrics
with open('models/tfidf_vect.pkl', 'wb') as f:
    pickle.dump(tfidf_vect, f)
with open('models/cosine_mtx.npy', 'wb') as f:
    np.save(f, cosine_mtx)
with open('models/svd_model.pkl', 'wb') as f:
    pickle.dump(svd_model, f)

metrics = {'precision@10': prec, 'recall@10': rec}
pd.DataFrame.from_dict(metrics, orient='index', columns=['value']) \
    .to_csv('models/hybrid_metrics.csv')

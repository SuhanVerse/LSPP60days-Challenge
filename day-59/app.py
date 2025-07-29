import pickle
import numpy as np
import pandas as pd
import random
import logging

from fastapi import FastAPI, HTTPException
from scipy.sparse import csr_matrix
from surprise import SVD
from implicit.bpr import BayesianPersonalizedRanking
from models.data_prep_bpr import build_sparse_interaction

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import uvicorn

# ——————————————————————————————————————————
# 1) Initialize FastAPI
# ——————————————————————————————————————————
app = FastAPI(
    title="LSPP60 Recommender API",
    description="Serving Content, SVD, Hybrid & BPR recommenders",
    version="1.0"
)

# configure logging
logging.basicConfig(level=logging.INFO)


# ——————————————————————————————————————————
# 2) Load data & models once at startup
# ——————————————————————————————————————————
tracks_df = pd.read_csv("data/tracks.csv")
ratings_df = pd.read_csv("data/ratings.csv")

with open("models/tfidf_vect.pkl", "rb") as f:
    tfidf_vect = pickle.load(f)
cosine_mtx = np.load("models/cosine_mtx.npy")

with open("models/svd_model.pkl", "rb") as f:
    svd_model: SVD = pickle.load(f)

with open("models/bpr_model.pkl", "rb") as f:
    bpr_model: BayesianPersonalizedRanking = pickle.load(f)

user2idx = pickle.load(open("models/user2idx.pkl", "rb"))
item2idx = pickle.load(open("models/item2idx.pkl", "rb"))
idx2item = {v: k for k, v in item2idx.items()}



# ——————————————————————————————————————————
# 3) Recommendation functions
# ——————————————————————————————————————————
def content_recs(track_id: int, top_n: int = 10):
    if track_id not in tracks_df.track_id.values:
        raise HTTPException(404, f"Track {track_id} not found")
    idx = tracks_df.index[tracks_df.track_id == track_id][0]
    sims = list(enumerate(cosine_mtx[idx]))
    sims.sort(key=lambda x: x[1], reverse=True)
    return [tracks_df.iloc[i]['track_id'] for i, _ in sims[1:top_n+1]]

def cf_recs(user_id: int, top_n: int = 10):
    scores = [(tid, svd_model.predict(user_id, tid).est)
              for tid in tracks_df.track_id]
    scores.sort(key=lambda x: x[1], reverse=True)
    return [tid for tid, _ in scores[:top_n]]

def hybrid_recs(user_id: int, alpha: float = 0.7, top_n: int = 10):
    user_ratings = ratings_df.query("user_id==@user_id")
    rated = set(user_ratings.track_id)
    # content scores
    content_scores = {}
    for tid, rating in user_ratings[['track_id','rating']].values:
        base_idx = tracks_df.index[tracks_df.track_id == tid][0]
        for idx, sim in enumerate(cosine_mtx[base_idx]):
            track_id = tracks_df.at[idx,'track_id']
            content_scores.setdefault(track_id, 0.0)
            content_scores[track_id] += sim * (rating / 5.0)
    for k in content_scores:
        content_scores[k] /= max(1, len(rated))
    # cf scores
    cf_scores = {
        tid: svd_model.predict(user_id, tid).est/5.0
        for tid in tracks_df.track_id if tid not in rated
    }
    # blend
    combined = [(tid, alpha * cf_scores.get(tid,0) + (1-alpha) * content_scores.get(tid,0))
                for tid in cf_scores]
    combined.sort(key=lambda x: x[1], reverse=True)
    return [tid for tid, _ in combined[:top_n]]

def bpr_recs(user_id: int, top_n: int = 10):
    if user_id not in user2idx:
        raise HTTPException(404, f"User {user_id} not found")
    u_idx = user2idx[user_id]
    liked = ratings_df.query("rating>=4")[['user_id','track_id']]
    filt = build_sparse_interaction(liked, user2idx, item2idx).tocsr()
    recs = bpr_model.recommend(
        u_idx, filt, N=top_n, filter_already_liked_items=True
    )
    # handle the (ids, scores) tuple return
    if isinstance(recs, tuple) and len(recs) == 2:
        return list(recs[0])
    return [tid for tid, _ in recs]



# ——————————————————————————————————————————
# 4) FastAPI endpoints
# ——————————————————————————————————————————
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/recommend/content/{track_id}")
def api_content(track_id: int, top_n: int = 10):
    return {"track_id": track_id, "recommendations": content_recs(track_id, top_n)}
    
@app.get("/recommend/cf/{user_id}")
def api_cf(user_id: int, top_n: int = 10):
    return {"user_id": user_id, "recommendations": cf_recs(user_id, top_n)}

@app.get("/recommend/hybrid/{user_id}")
def api_hybrid(user_id: int, top_n: int = 10, alpha: float = 0.7):
    return {
        "user_id": user_id,
        "alpha": alpha,
        "recommendations": hybrid_recs(user_id, alpha, top_n)
    }

@app.get("/recommend/bpr/{user_id}")
def api_bpr(user_id: int, top_n: int = 10):
    return {"user_id": user_id, "recommendations": bpr_recs(user_id, top_n)}

# ——————————————————————————————————————————
# 5) Run with Uvicorn
# ——————————————————————————————————————————
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

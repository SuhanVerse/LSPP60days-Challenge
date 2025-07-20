import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Load & cache
def load_recommender(data_path: str):
    df = pd.read_csv(data_path)
    print(df.columns)
    df[['track_name','artist','genre']] = df[['track_name','artist','genre']].fillna('')
    df['combined'] = df['genre'] + ' ' + df['artist'] + ' ' + df['track_name']
    vect = TfidfVectorizer(stop_words='english')
    tfidf = vect.fit_transform(df['combined'])
    sim = cosine_similarity(tfidf, tfidf)
    return df, sim

def get_recommendations(title: str, df: pd.DataFrame, sim=...):  # Only valid in some contexts
    idxs = df.index[df['track_name'].str.lower()==title.lower()]
    if len(idxs)==0: return pd.DataFrame()
    idx = idxs[0]
    scores = list(enumerate(sim[idx]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    recs = df.iloc[[i for i,_ in scores]][['track_name','artist','genre']].copy()
    recs['score'] = [s for _,s in scores]
    return recs

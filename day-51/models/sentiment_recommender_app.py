import streamlit as st
import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


import os
import nltk

# Tell nltk where to find the downloaded lexicon
os.environ["NLTK_DATA"] = "/home/xlegion/nltk_data"
nltk.download("vader_lexicon")  # just to be safe

from nltk.sentiment.vader import SentimentIntensityAnalyzer

DATA_PATH = "data/smusic.csv"

@st.cache_data
def load_df():
    df = pd.read_csv(DATA_PATH, encoding="latin1")

    # 1) Rename columns to match your code’s expectations
    df = df.rename(columns={
        "Track":            "track_name",
        "Artist":           "artist",
        # add more renames here if needed...
    })

    # 2) Ensure "All Time Rank" is numeric
    df["All Time Rank"] = pd.to_numeric(df["All Time Rank"], errors="coerce")
    df["is_top10"] = (df["All Time Rank"] <= 10).astype(int)

    # 3) Fill in a blank genre column if it’s missing
    if "genre" not in df.columns:
        df["genre"] = ""

    return df

@st.cache_data
def build_sim_matrix(df):
    df["combined"] = (
        df["genre"].fillna("").str.strip() + " " +
        df["artist"].fillna("").str.strip() + " " +
        df["track_name"].fillna("").str.strip()
    )

    # Final safety: drop or fill any remaining NaNs
    df["combined"] = df["combined"].fillna("")

    vect = TfidfVectorizer(stop_words="english")
    tfidf = vect.fit_transform(df["combined"])

    return df, cosine_similarity(tfidf, tfidf)


# --------------------------
# Streamlit UI below
# --------------------------
st.title("🎵 Music Recommender & Title Sentiment")

df = load_df()
df, sim = build_sim_matrix(df)

song = st.selectbox("Choose a song to get recommendations:", df["track_name"].unique())
if st.button("Recommend"):
    idx = df.index[df["track_name"] == song][0]
    scores = list(enumerate(sim[idx]))
    top = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
    recs = df.iloc[[i for i,_ in top]][["track_name","artist","genre"]]
    recs["score"] = [s for _,s in top]
    st.write("Top 5 recommendations:")
    st.table(recs)


sia = SentimentIntensityAnalyzer()
title = st.text_input("Or enter a custom title to analyze sentiment:")
if st.button("Analyze Sentiment"):
    score = sia.polarity_scores(title)["compound"]
    st.write(f"VADER compound score: **{score:.2f}**")

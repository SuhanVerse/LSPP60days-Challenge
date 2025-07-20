import streamlit as st
import pandas as pd
from models.recommender import load_recommender, get_recommendations
from models.sentiment_analysis import analyze_titles
import os

DATA_PATH = os.path.join('data','music.csv')

@st.cache_resource
def init_models():
    return load_recommender(DATA_PATH)

df, sim = init_models()

st.title("🎵 Music Recommender & Sentiment Explorer")

# 1) Recommender
st.header("1️⃣ Music Recommendations")
song = st.text_input("Enter a song title:", "")
if st.button("Recommend"):
    recs = get_recommendations(song, df, sim)
    if recs.empty:
        st.warning("Title not found!")
    else:
        st.table(recs)

# 2) Sentiment
st.header("2️⃣ Sentiment Analyzer")
txt = st.text_area("Enter text for sentiment:", "")
if st.button("Analyze Sentiment"):
    out = analyze_titles([txt])[0]
    st.metric("Compound Score", f"{out['compound']:.2f}")

st.write("---")
st.write("Powered by TF‑IDF + cosine similarity and NLTK VADER")

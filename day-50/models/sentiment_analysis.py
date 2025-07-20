import pandas as pd
from nltk.sentiment import SentimentIntensityAnalyzer

def analyze_titles(titles: list[str]):
    sia = SentimentIntensityAnalyzer()
    return [{'text': t, 'compound': sia.polarity_scores(t)['compound']} for t in titles]

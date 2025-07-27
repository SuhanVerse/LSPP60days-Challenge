# data_prep.py
import warnings
warnings.filterwarnings(
    "ignore",
    message="A NumPy version.*required for this version of SciPy",
    category=UserWarning
)


import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np

def load_and_binarize(ratings_path, threshold=4.0):
    df = pd.read_csv(ratings_path)
    # Implicit feedback: 1 if rating >= threshold, else 0
    df['interaction'] = (df['rating'] >= threshold).astype(int)
    return df[['user_id','track_id','interaction']]

def train_test_implicit(df, test_size=0.2, random_state=42):
    # Split by user: keep some interactions per user for test
    train_list, test_list = [], []
    for uid, group in df.groupby('user_id'):
        pos = group[group.interaction==1]
        neg = group[group.interaction==0]
        # shuffle positives and negatives
        pos_shuf = pos.sample(frac=1, random_state=random_state)
        test_pos = pos_shuf.iloc[: max(1, int(len(pos)*test_size)) ]
        train_pos = pos_shuf.iloc[ max(1, int(len(pos)*test_size)) : ]
        # leave all negatives in train
        train_list.append(train_pos)
        test_list.append(test_pos)
        train_list.append(neg)
    train_df = pd.concat(train_list).sample(frac=1, random_state=random_state)
    test_df  = pd.concat(test_list).sample(frac=1, random_state=random_state)
    return train_df, test_df

if __name__ == "__main__":
    df = load_and_binarize('data/ratings.csv')
    train_df, test_df = train_test_implicit(df)
    print(f"Train interactions: {len(train_df)}, Test interactions: {len(test_df)}")

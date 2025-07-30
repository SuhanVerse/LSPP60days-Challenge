import pandas as pd
from scipy.sparse import coo_matrix

def load_implicit(ratings_path: str, threshold: float = 4.0) -> pd.DataFrame:
    """
    Load explicit ratings and filter for “liked” interactions.
    Returns DataFrame with columns ['user_id','track_id'].
    """
    df = pd.read_csv(ratings_path)
    df = df[df.rating >= threshold]
    return df[['user_id', 'track_id']]

def build_sparse_interaction(
    df: pd.DataFrame,
    user_map: dict,
    item_map: dict
) -> coo_matrix:
    """
    Construct a sparse user–item interaction matrix (COO format).
    Rows: user indices, Cols: item indices, Values: 1 for each interaction.
    """
    rows = df['user_id'].map(user_map).to_numpy()
    cols = df['track_id'].map(item_map).to_numpy()
    data = [1] * len(df)
    return coo_matrix(
        (data, (rows, cols)),
        shape=(len(user_map), len(item_map))
    )

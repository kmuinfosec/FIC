import pandas as pd
import os

def load_pickle_data(path):
    """Reads a pickle file from the specified path and returns it as a DataFrame."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Data file not found: {path}")
    print(f"Loading data: {path}")
    return pd.read_pickle(path)

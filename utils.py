from pathlib import Path
import pandas as pd
import numpy as np

def load_csv_data(path):
    """
    Load a csv file from the specified path and returns it as a DataFrame.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Data file not found: {path}")
    print(f"[load] {path}")
    df = pd.read_csv(path)
    print(f"[ok]   loaded DataFrame: rows={len(df)} cols={len(df.columns)}")
    return df

def save_sigset(path, sigset):
    """
    Save a signature set as a NumPy .npy file (uint64).
    """
    path = Path(path)
    arr = np.array(sorted(int(s) for s in sigset), dtype=np.uint64)
    print(f"[save] signature set -> {path} (size={arr.size})")
    np.save(path, arr)

def load_sigset(path):
    """
    Load a signature set from a NumPy .npy file into a Python set[int].
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"signature set file not found: {path}")
    print(f"[load] {path}")
    arr = np.load(path, allow_pickle=False)
    print(f"[ok]   loaded signature set: size={arr.size}")
    return set(int(x) for x in arr.tolist())

def save_preds(path, y_pred):
    """
    Save only predictions (y_pred) as a single-column CSV.
    """
    path = Path(path)
    pd.DataFrame({"y_pred": y_pred}).to_csv(path, index=False, encoding="utf-8")
    print(f"[save] y_pred -> {path} (rows={len(y_pred)})")
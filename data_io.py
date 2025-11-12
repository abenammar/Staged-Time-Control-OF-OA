import os
import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def load_toein():
    x_path = os.path.join(DATA_DIR, "X_TIdiff.csv")
    y_path = os.path.join(DATA_DIR, "y_TIP1diff.csv")
    if os.path.exists(x_path) and os.path.exists(y_path):
        X = pd.read_csv(x_path)
        y = pd.read_csv(y_path)
        # y may be a single column; rename to TIP1diff
        if y.shape[1] == 1:
            y.columns = ["TIP1diff"]
        return X, y["TIP1diff"]
    return None, None

def load_gait():
    g_path = os.path.join(DATA_DIR, "gait.csv")
    if os.path.exists(g_path):
        df = pd.read_csv(g_path)
        return df
    return None

def demo_dataset(n=200, seed=7):
    import numpy as np
    rng = np.random.default_rng(seed)
    A = rng.normal(0, 1, n)          # aggrecan-ish
    C = rng.normal(0, 1, n)          # collagen-ish
    load = rng.uniform(0, 1, n)      # mechanical exposure proxy
    # "benefit" when A low and early
    stage = (A < -0.2).astype(int) + (C < -0.2).astype(int)  # 0,1,2 proxy
    # synthetic "reduction" target
    y = 0.6*stage + 0.4*load + rng.normal(0,0.4,n)
    y = (y > y.mean()).astype(int)
    X = pd.DataFrame({"A_proxy":A, "C_proxy":C, "load":load})
    return X, pd.Series(y, name="response")

def build_training_frame():
    # Prefer ToeIn real dataset if present
    X_toe, y_toe = load_toein()
    if X_toe is not None:
        df = X_toe.copy()
        df["TIP1diff"] = y_toe.values
        # Binary target: positive KAM reduction considered success
        df["benefit"] = (df["TIP1diff"] > 0).astype(int)
        # Keep a small set of robust features (present in repo)
        keep = [c for c in df.columns if c not in ["TIP1diff","benefit"]]
        X = df[keep]
        y = df["benefit"]
        return X, y, {"source":"ToeInKAMReduction","n":len(df)}
    # Fallback to demo
    X, y = demo_dataset()
    return X, y, {"source":"demo_synthetic","n":len(X)}

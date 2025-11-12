from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import numpy as np

def train_eval(X, y, seed=42):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.3, random_state=seed, stratify=y)
    pipe = Pipeline([("scaler", StandardScaler()),
                     ("clf", LogisticRegression(max_iter=1000))])
    pipe.fit(X_tr, y_tr)
    p = pipe.predict_proba(X_te)[:,1]
    # monotonic recalibration (isotonic) on held-out CV might be added later
    roc = roc_auc_score(y_te, p)
    pr = average_precision_score(y_te, p)
    return {"model":pipe, "probs":p, "y_true":y_te, "roc":roc, "pr":pr}

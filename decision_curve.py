import numpy as np
import pandas as pd

def decision_curve(y_true, prob, thresholds=None):
    """
    Compute net benefit across thresholds vs treat-all/none.
    """
    if thresholds is None:
        thresholds = np.linspace(0.05, 0.95, 19)
    results = []
    y = np.asarray(y_true).astype(int)
    p = np.asarray(prob)
    N = len(y)
    for t in thresholds:
        treat = (p >= t).astype(int)
        TP = ((treat==1)&(y==1)).sum()
        FP = ((treat==1)&(y==0)).sum()
        NB = TP/N - FP/N * (t/(1-t))
        # baselines
        NB_all = y.mean() - (1-y.mean())*(t/(1-t))
        NB_none = 0.0
        results.append({"threshold":t,"net_benefit":NB,"treat_all":NB_all,"treat_none":NB_none})
    return pd.DataFrame(results)

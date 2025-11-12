import os
import pandas as pd
from src.data_io import build_training_frame
from src.simple_classifier import train_eval
from src.decision_curve import decision_curve
from src.figures import (
    plot_roc_pr, plot_calibration, plot_decision_curve,
    plot_distribution, plot_policy_timeline, plot_integrity_example
)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "figures")
os.makedirs(OUT, exist_ok=True)

X, y, meta = build_training_frame()
print(f"Data source: {meta['source']} (n={meta['n']})")

res = train_eval(X, y)
print(f"ROC AUC={res['roc']:.3f}  PR AUC={res['pr']:.3f}")

# Figures
plot_roc_pr(res["y_true"], res["probs"], OUT)
plot_calibration(res["y_true"], res["probs"], OUT, n_bins=10)
dc = decision_curve(res["y_true"], res["probs"])
dc.to_csv(os.path.join(ROOT, "figures", "decision_curve.csv"), index=False)
plot_decision_curve(dc, OUT)
plot_distribution(res["y_true"], res["probs"], OUT)
plot_policy_timeline(OUT)
plot_integrity_example(OUT)

# add two more simple exploratory figures if ToeIn data present
if meta["source"] == "ToeInKAMReduction":
    import matplotlib.pyplot as plt
    import numpy as np
    # load the merged frame again
    from src.data_io import load_toein
    X_toe, y_toe = load_toein()
    df = X_toe.copy()
    df["TIP1diff"] = y_toe.values
    # scatter of a representative feature vs TIP1diff
    feat = [c for c in df.columns if c not in ["TIP1diff"]][0]
    plt.scatter(df[feat], df["TIP1diff"], s=12)
    plt.xlabel(feat); plt.ylabel("TIP1diff (KAM change)")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "fig3_feat_vs_tip1.png"), dpi=140); plt.close()
    # histogram of TIP1diff
    plt.hist(df["TIP1diff"], bins=25)
    plt.xlabel("TIP1diff"); plt.ylabel("Count")
    plt.tight_layout(); plt.savefig(os.path.join(OUT, "fig4_tip1_hist.png"), dpi=140); plt.close()
else:
    # If demo, create placeholders so we still have 8 figs total
    import numpy as np, matplotlib.pyplot as plt
    for i in range(3,5):
        plt.plot(np.linspace(0,1,50), np.sin(i*np.linspace(0,1,50)))
        plt.tight_layout(); plt.savefig(os.path.join(OUT, f"fig{i}_placeholder.png"), dpi=140); plt.close()

print("Saved figures to:", OUT)

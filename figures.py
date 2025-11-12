import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay, PrecisionRecallDisplay, brier_score_loss
from sklearn.calibration import calibration_curve

def savefig(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=140, bbox_inches="tight")
    plt.close()

def plot_roc_pr(y_true, probs, outdir):
    RocCurveDisplay.from_predictions(y_true, probs)
    savefig(os.path.join(outdir, "fig5_roc.png"))
    PrecisionRecallDisplay.from_predictions(y_true, probs)
    savefig(os.path.join(outdir, "fig5_pr.png"))

def plot_calibration(y_true, probs, outdir, n_bins=10):
    frac_pos, mean_pred = calibration_curve(y_true, probs, n_bins=n_bins, strategy="quantile")
    plt.plot(mean_pred, frac_pos, marker="o")
    plt.plot([0,1],[0,1], linestyle="--")
    plt.xlabel("Mean predicted probability")
    plt.ylabel("Observed fraction positive")
    savefig(os.path.join(outdir, "fig6_calibration.png"))

def plot_decision_curve(df, outdir):
    plt.plot(df["threshold"], df["net_benefit"], label="Stage-timed (classifier)")
    plt.plot(df["threshold"], df["treat_all"], linestyle="--", label="Treat all")
    plt.plot(df["threshold"], df["treat_none"], linestyle=":", label="Treat none")
    plt.xlabel("Threshold probability")
    plt.ylabel("Net benefit")
    plt.legend()
    savefig(os.path.join(outdir, "fig6_decision_curve.png"))

def plot_distribution(y_true, probs, outdir):
    plt.hist(probs, bins=25)
    plt.xlabel("Predicted probability")
    plt.ylabel("Count")
    savefig(os.path.join(outdir, "fig2_prob_hist.png"))

def plot_policy_timeline(outdir):
    # simple schematic
    t = np.arange(0, 24, 1)
    A = 1.0/(1+np.exp((t-6)/1.5))  # early A emphasis
    C = 1.0/(1+np.exp(-(t-12)/1.8)) # late C emphasis
    plt.plot(t, A, label="ADAMTS-5 emphasis (early)")
    plt.plot(t, C, label="MMP-13 emphasis (late)")
    plt.xlabel("Months")
    plt.ylabel("Relative emphasis")
    plt.legend()
    savefig(os.path.join(outdir, "fig8_policy_timeline.png"))

def plot_integrity_example(outdir):
    t = np.linspace(0,24,50)
    ag = 1 - 0.4*(1-np.exp(-t/6))
    co = 1 - 0.1*np.maximum(0, t-8)/16
    integ = 0.5*ag + 0.5*co
    plt.plot(t, integ)
    plt.xlabel("Months")
    plt.ylabel("Integrity (composite)")
    savefig(os.path.join(outdir, "fig2_integrity_curve.png"))

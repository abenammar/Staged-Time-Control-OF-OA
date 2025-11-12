# OA Stage-Timed Control — Real Data Test Pack

This pack gives you **working Python code** plus one-command scripts to download **real, openly licensed datasets from the internet** and regenerate figures.

## What's inside
- `scripts/fetch_real_data.sh` / `fetch_real_data.ps1` — download real CSVs:
  - Toe-in gait dataset (ADAMTS/MMP surrogate: KAM reduction with toe-in) — **GitHub / Apache-2.0**
  - UCI **Multivariate Gait Data** (`gait.csv`, **CC BY 4.0**)
- `src/` — minimal, auditable pipeline:
  - loads real CSVs if present, else falls back to tiny built-in demo
  - trains a light classifier (logistic) to trigger stage-switches
  - computes **ROC, PR, calibration**, **decision curve net benefit**
  - exports **8 figures** in `figures/`
- `figures/` — outputs go here
- `data/` — put CSVs here (scripts will download them)

> **Note:** I cannot directly bundle third‑party files from the web in this environment. Run the fetch script below on your machine to pull the real CSVs into `data/`.

## Quick start
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
bash scripts/fetch_real_data.sh     # downloads real CSVs into data/
python src/run_pipeline.py          # builds dataset & saves 8 figures
```

Windows PowerShell:
```powershell
py -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
powershell -ExecutionPolicy Bypass -File scripts\fetch_real_data.ps1
python src\run_pipeline.py
```

## Real datasets used
- **ToeInKAMReduction** (X_TIdiff.csv, y_TIP1diff.csv), Suhlrich et al. — Apache-2.0 (GitHub).
- **Multivariate Gait Data** (`gait.csv`) — UCI Machine Learning Repository, CC BY 4.0.

See `LICENSE-3RD-PARTY.md` for sources and license notes.

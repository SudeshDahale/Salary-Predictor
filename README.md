# Salary Predictor

Predict employee salaries from job attributes using a trained Random Forest model.

## Overview

Salary Predictor is a Python‑Flask monolith that exposes a simple HTTP API for salary inference and bundles a static HTML/JS front‑end. The backend loads a pre‑trained Random Forest regressor (rf_regressor.pkl) and serves a `/predict` endpoint; a separate `train_model.py` script can rebuild the model from `data/Position_Salaries.csv`. The front‑end (`frontend/index.html`) collects user inputs, calls the API via JavaScript, and displays the predicted salary.

All components live in a single repository, making it easy to run locally or containerise for production.

## Features

- Flask API (`backend/app.py`) that loads a serialized Random Forest model and returns salary predictions as JSON.
- Training script (`backend/train_model.py`) to retrain the model on the supplied CSV dataset and persist updated artifacts.
- Pre‑trained model artifact (`models/rf_regressor.pkl`) with accompanying metadata (`models/metadata.json`).
- Lightweight static front‑end (`frontend/index.html`, CSS, JS) that demonstrates end‑to‑end usage without any build step.
- Clear separation of data (`data/Position_Salaries.csv`), model (`models/`), backend (`backend/`), and UI (`frontend/`).
- Requirements file (`backend/requirements.txt`) pinning Flask, scikit‑learn, pandas, and other runtime dependencies.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# (Optional) create a virtual environment
python -m venv venv && source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Start the Flask API (default runs on http://127.0.0.1:5000)
python backend/app.py
```

In a separate terminal, open the UI:
```bash
# Open the static page in a browser (no server needed)
open frontend/index.html   # macOS
# or on Linux
xdg-open frontend/index.html
# or simply double‑click the file in your file manager.
```

The UI will submit requests to the locally running API and display the predicted salary.
```
```

## Architecture

The project follows a monolithic, API‑first design: a single Flask service hosts the model and all HTTP endpoints, while the front‑end consists of static assets that call those endpoints directly. No separate micro‑services or external gateways are required; the API and UI are co‑located in the repository and can be served together or independently.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

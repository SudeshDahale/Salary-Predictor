# Salary Predictor

Predict employee salaries from job details using a pre‑trained RandomForest model.

## Overview

Salary Predictor is a single‑repo, monolithic web application that combines a Flask‑based prediction API with a lightweight HTML/CSS front‑end. The back‑end loads a scikit‑learn RandomForest regressor (pickled in *models/rf_regressor.pkl*) and exposes a `/predict` endpoint. The static front‑end (under *frontend/*) collects job parameters, calls the API, and displays the forecast. A training script (`backend/train_model.py` or the accompanying Jupyter notebook) reads the supplied CSV dataset, trains the model, and stores both the model file and its metadata.

## Features

- Static HTML UI for entering job attributes (e.g., years of experience, education, location) and showing predicted salary.
- Flask API (`backend/app.py`) with a `/predict` POST endpoint that returns JSON predictions.
- Model management that loads a pickled RandomForest regressor (`models/rf_regressor.pkl`) and reads accompanying metadata (`models/metadata.json`).
- Training pipeline (`backend/train_model.py` and `random_forest_regression.ipynb`) that ingests `data/Position_Salaries.csv`, fits a RandomForestRegressor, and persists the model and its metadata.
- All dependencies listed in `backend/requirements.txt` (Flask, scikit‑learn, pandas, numpy).
- API‑first design – the front‑end communicates solely through HTTP, making it easy to replace the UI or consume the API elsewhere.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up the back‑end virtual environment
python -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`

# Install Python dependencies
pip install -r backend/requirements.txt

# (Optional) Re‑train the model – this will overwrite models/rf_regressor.pkl and models/metadata.json
python backend/train_model.py

# Start the Flask API
python backend/app.py   # defaults to http://127.0.0.1:5000

# In a separate terminal, open the UI (no server needed – just open the file)
open frontend/index.html   # macOS; use `start` on Windows or `xdg-open` on Linux
```

```

## Architecture

The project follows a **monolithic, API‑first** architecture. The Flask server (`backend/app.py`) is the sole runtime process, exposing REST endpoints. The UI is a set of static assets (`frontend/index.html`, CSS, images) served directly by a browser, which calls the back‑end API via AJAX. Model artifacts live in the `models/` directory; the training script updates these artifacts, and the running API reloads them on start‑up.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

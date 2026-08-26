# Salary Predictor

Predict employee salaries using a trained Random Forest model via a simple web interface.

## Overview

Salary Predictor is a Python‑based application that trains a scikit‑learn RandomForestRegressor on the *Position_Salaries.csv* dataset and serves the model through a Flask API. A lightweight static HTML front‑end collects user inputs (e.g., position, degree, years of experience) and displays the model’s salary prediction. The repository contains the full training pipeline, the serialized model artifacts, and the client‑server code needed to run the service locally.

## Features

- End‑to‑end training pipeline (`train_model.py` & notebook) that reads `data/Position_Salaries.csv`, preprocesses data, trains a RandomForestRegressor, and saves the model and metadata.
- Flask API (`/predict`) that accepts JSON input, performs inference with the persisted model, and returns the predicted salary.
- Static HTML UI (`frontend/index.html`) for interactive salary predictions without any JavaScript frameworks.
- Model versioning via `models/metadata.json` to track training parameters and data source.
- Docker‑ready requirements (`backend/requirements.txt`) for reproducible environment setup.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up the backend environment (Python 3.9+ recommended)
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r backend/requirements.txt

# (Optional) Re‑train the model – will overwrite models/rf_regressor.pkl
python backend/train_model.py

# Start the Flask server
python backend/app.py
# Server runs at http://127.0.0.1:5000

# Open the UI in a browser (no server needed for static files)
open frontend/index.html   # macOS
# or use your file explorer to open `frontend/index.html`
```
```

## Architecture

The project follows a monolithic client‑server architecture. The **backend** (`backend/app.py`) runs a Flask web service exposing a `/predict` endpoint that loads the pickled `rf_regressor.pkl` model and returns JSON predictions. The **frontend** (`frontend/index.html`) is a static HTML page that posts user data to the Flask endpoint and renders the returned salary. Model training lives in `backend/train_model.py` (and the Jupyter notebook) and produces the serialized model (`models/rf_regressor.pkl`) and accompanying `metadata.json`.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

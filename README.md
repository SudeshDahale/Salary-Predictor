# Salary Predictor

Predict employee salaries based on position data using a Flask API and a trained RandomForest model.

## Overview

The Salary Predictor project provides a simple web interface and an API to estimate salaries for given job titles, locations, and experience levels. The backend, built with Flask, loads a pre‑trained scikit‑learn RandomForestRegressor (stored in `models/rf_regressor.pkl`) and exposes a `/predict` endpoint. The frontend (`frontend/index.html`) gathers user input, calls the API via JavaScript, and displays the predicted salary. The model is trained on the CSV dataset `data/Position_Salaries.csv` using the `backend/train_model.py` script, which also generates `models/metadata.json` for reference.

## Features

- Flask API (`backend/app.py`) that loads a serialized RandomForest model and returns JSON predictions.
- Static HTML/CSS/JS UI (`frontend/index.html`) for user-friendly salary estimation.
- Training script (`backend/train_model.py`) that preprocesses the CSV dataset and saves the model artifact (`models/rf_regressor.pkl`).
- Model metadata (`models/metadata.json`) documenting training parameters and feature schema.
- All dependencies declared in `backend/requirements.txt` for reproducible environment setup.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment and install backend dependencies
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r backend/requirements.txt

# (Optional) Retrain the model if you modify the data
python backend/train_model.py

# Start the Flask prediction service
export FLASK_APP=backend/app.py
flask run  # defaults to http://127.0.0.1:5000

# In a separate terminal, open the frontend UI
# You can serve the static files with any simple HTTP server, e.g.:
python -m http.server 8080 --directory frontend
# Then navigate to http://localhost:8080 in your browser.
```
```

## Architecture

The project follows a monolithic, API‑first design. The Flask backend acts as the single source of truth, exposing REST endpoints that load the pre‑trained RandomForestRegressor and perform inference. The frontend is a static client that consumes these endpoints via AJAX, keeping the UI decoupled from model logic while still residing in the same repository. Model training is isolated in a separate script, producing a serialized artifact and accompanying metadata stored under `models/`.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

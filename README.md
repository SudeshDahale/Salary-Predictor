# Salary Predictor

Predict software engineer salaries using a trained Random Forest model via a simple Flask API and web UI.

## Overview

This repository provides an end‑to‑end salary prediction service built with Python, Flask, and scikit‑learn. Raw salary data is ingested from a CSV, a Random Forest regressor is trained and persisted, and a Flask API serves predictions to a static HTML frontend. The project follows a monolithic, API‑first architecture, keeping model training, serving, and UI in a single codebase for easy deployment and experimentation.

## Features

- Data ingestion from `data/Position_Salaries.csv` using pandas.
- Model training script (`backend/train_model.py`) that builds a RandomForestRegressor and saves it to `models/rf_regressor.pkl` with accompanying metadata.
- Flask API (`backend/app.py`) that loads the pickled model and exposes a `/predict` endpoint returning JSON predictions.
- Responsive static frontend (`frontend/index.html`) that collects user inputs and calls the `/predict` endpoint via JavaScript.
- Requirements pinning in `backend/requirements.txt` for reproducible environments.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a Python virtual environment
python3 -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Train the model from scratch
python backend/train_model.py

# Start the Flask API server
export FLASK_APP=backend/app.py
flask run   # defaults to http://127.0.0.1:5000

# Open the frontend UI in a browser
# The HTML page uses the running API at http://127.0.0.1:5000/predict
open frontend/index.html   # macOS; use `xdg-open` on Linux or double‑click the file on Windows
```
```

## Architecture

Monolithic, API‑First design: a single Flask application (`backend/app.py`) hosts the prediction endpoint, loads the pre‑trained RandomForest model (`models/rf_regressor.pkl`), and serves static assets from the `frontend/` directory. Data ingestion and model training live in the same repository, enabling a straightforward end‑to‑end workflow from raw CSV to live predictions.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

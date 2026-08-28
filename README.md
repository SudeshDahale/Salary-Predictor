# Salary Predictor

Predict employee salaries using a trained Random Forest model via a Flask API and web UI.

## Overview

The Salary Predictor project demonstrates a full‑stack machine‑learning pipeline built with Python. A raw CSV of job positions and salaries is ingested, pre‑processed, and used to train a Random Forest regressor (scikit‑learn). The trained model is serialized with pickle and accompanied by metadata. A Flask application loads the model at runtime, exposing a `/predict` API that accepts JSON payloads and returns salary predictions. A lightweight HTML/JS frontend posts user input to this API and displays the result, all packaged as a single monolithic, API‑first codebase.

## Features

- Data Ingestion: Reads `data/Position_Salaries.csv` and prepares features for model training.
- Model Training: `backend/train_model.py` trains a Random Forest regressor and saves `models/rf_regressor.pkl` plus `models/metadata.json`.
- Prediction Service: Flask app (`backend/app.py`) deserialises the model and provides a `/predict` endpoint returning JSON predictions.
- Frontend UI: Static `frontend/index.html` collects user inputs, calls the prediction API via JavaScript, and renders the salary forecast.
- Model Persistence: Model artifact and training metadata are versioned in the `models/` directory for reproducible loading.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a Python virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install -r backend/requirements.txt

# Train the model (creates `models/rf_regressor.pkl` and `models/metadata.json`)
python backend/train_model.py

# Start the Flask prediction service
python backend/app.py

# In a separate terminal, open the UI (no server needed for static files)
# e.g., using Python's built‑in HTTP server:
cd frontend
python -m http.server 8000
# Then navigate to http://localhost:8000 in a browser.

```

## Architecture

Monolithic, API‑First design: the Flask server hosts both the RESTful prediction API and the static frontend assets. Model loading occurs once at startup, keeping inference latency low. All components live under a single repository, enabling straightforward end‑to‑end execution.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

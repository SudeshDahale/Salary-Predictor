# Salary Predictor

Instantly estimate salaries using a pre‑trained Random Forest model via a simple web UI.

## Overview

Salary Predictor is a Python‑Flask application that predicts a candidate's expected salary based on input factors such as job title, years of experience, and location. The project ships a pre‑trained `RandomForestRegressor` model (pickled in `models/`) and provides a lightweight HTML front‑end that calls a `/predict` API endpoint. The repository also includes a training script and the original CSV dataset, making it easy to retrain or fine‑tune the model.

## Features

- Static HTML UI (`frontend/index.html`) that collects user inputs and displays the predicted salary.
- Flask API (`backend/app.py`) exposing a `/predict` endpoint which loads the serialized Random Forest model (`models/rf_regressor.pkl`).
- Pre‑trained model and accompanying metadata (`models/metadata.json`) ready for immediate inference.
- Training pipeline (`backend/train_model.py`) that reads the historic salary dataset (`data/Position_Salaries.csv`) and produces a new model pickle.
- Jupyter notebook (`random_forest_regression.ipynb`) demonstrating data exploration, feature engineering, and model evaluation.
- All Python dependencies listed in `backend/requirements.txt` for reproducible environments.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up the backend (Flask API)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r backend/requirements.txt

# Run the Flask server
python backend/app.py &

# Open the frontend (no server required for static HTML)
# You can either open the file directly in a browser or serve it with a simple HTTP server:
cd frontend
python -m http.server 8000   # then navigate to http://localhost:8000

```

## Architecture

The repository follows a monolithic, API‑first design: a single Flask service (`backend/app.py`) loads the persisted Random Forest model and provides a `/predict` REST endpoint. The static HTML front‑end (`frontend/index.html`) gathers user input and calls this endpoint via JavaScript `fetch`. Model training lives alongside the API in `backend/train_model.py`, using the CSV data in `data/`. All components coexist in one repo, simplifying deployment and local development.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

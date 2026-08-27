# Salary Predictor

Predict software engineer salaries using a trained Random Forest model via a Flask API and simple web UI.

## Overview

The Salary Predictor repository provides an end‑to‑end pipeline that ingests a CSV of historical salary data, trains a Random Forest regression model with scikit‑learn, and serves predictions through a Flask API. A lightweight static HTML/JavaScript front‑end consumes the API, allowing users to input job characteristics and receive an estimated salary instantly.

## Features

- Data ingestion from `data/Position_Salaries.csv` for reproducible model training.
- Model training script (`backend/train_model.py`) that builds a Random Forest regressor and serialises it to `models/rf_regressor.pkl`.
- Flask API (`backend/app.py`) that loads the persisted model and exposes a `/predict` endpoint returning JSON predictions.
- Static front‑end (`frontend/index.html`) with a form that posts user input to the API and displays the predicted salary.
- All dependencies locked in `backend/requirements.txt` (Flask, pandas, scikit‑learn, etc.).
- Model metadata (`models/metadata.json`) documenting training parameters and feature schema.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment and install backend dependencies
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
pip install -r backend/requirements.txt

# (Optional) Re‑train the model if you modify the data
python backend/train_model.py

# Start the Flask server (will serve the API and static UI)
export FLASK_APP=backend/app.py
export FLASK_ENV=development   # enables hot‑reload
flask run

# Open a browser and navigate to http://127.0.0.1:5000 to use the UI.
```
```

## Architecture

Monolithic API‑first design: the Flask backend hosts both the model inference endpoint and the static UI assets, while the training pipeline lives alongside the service. Data lives under `data/`, the trained model and its metadata under `models/`, and the user‑facing interface under `frontend/`.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

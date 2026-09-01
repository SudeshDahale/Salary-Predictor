# Salary Predictor

Predict employee salaries based on position and experience using a trained Random Forest model.

## Overview

The Salary Predictor is a monolithic, API‑first application that trains a Random Forest regression model on a curated salary dataset, serializes the model, and serves predictions via a Flask API. A lightweight static HTML/JS frontend collects user input and calls the `/predict` endpoint to display estimated salaries.

## Features

- Data ingestion from `data/Position_Salaries.csv` for model training.
- Model training script (`backend/train_model.py`) that builds and pickles a Random Forest regressor.
- Model storage with metadata (`models/rf_regressor.pkl` & `models/metadata.json`).
- Flask API (`backend/app.py`) that loads the serialized model and exposes a `/predict` endpoint.
- Static frontend (`frontend/index.html`) that gathers user input and displays predictions via JavaScript fetch calls.
- All dependencies isolated in `backend/requirements.txt` for reproducible environments.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a Python virtual environment
python3 -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain the model – generates `models/rf_regressor.pkl`
python backend/train_model.py

# Start the Flask API server
python backend/app.py   # Server runs at http://127.0.0.1:5000

# Open the frontend UI in a browser
open frontend/index.html   # Or manually open the file in any web browser
```
```

## Architecture

The project follows a monolithic, API‑first design: a single Flask application (`backend/app.py`) houses the model loading, inference logic, and REST endpoint, while the static frontend (`frontend/index.html`) interacts with this API. Model training is decoupled into `backend/train_model.py`, producing a pickled Random Forest model stored under `models/`. All components reside in the same repository, making the stack straightforward for local development and deployment.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

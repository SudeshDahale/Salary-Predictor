# Salary Predictor

Predict job salaries using a trained Random Forest model via a Flask API and simple web UI.

## Overview

Salary Predictor is a Python monolith that combines a Flask backend API with a lightweight HTML frontend. Users can input job attributes (e.g., education, years of experience, location) and receive a salary prediction powered by a pre‑trained scikit‑learn RandomForestRegressor. The repository also includes a training script and dataset for re‑training the model.

## Features

- RESTful `/predict` endpoint that accepts JSON job features and returns a salary estimate.
- Static HTML UI (`frontend/index.html`) for interactive salary predictions without writing code.
- Training script (`backend/train_model.py`) that reads `data/Position_Salaries.csv`, fits a RandomForestRegressor, and stores the model (`models/rf_regressor.pkl`) plus metadata (`models/metadata.json`).
- Model versioning – the serialized model and its metadata are version‑controlled in the `models/` directory.
- All dependencies pinned in `backend/requirements.txt` for reproducible environments.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment and install backend dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt

# (Optional) Retrain the model
python backend/train_model.py

# Run the Flask API
python backend/app.py
```

# Open the UI in a browser
Open `frontend/index.html` in your favorite browser and point the form to `http://127.0.0.1:5000/predict`.
```

## Architecture

The monolithic, API‑first design places the Flask service (`backend/app.py`) at the core, exposing a `/predict` route. The frontend is a static HTML page that calls this API via JavaScript. Model artifacts (`rf_regressor.pkl` and `metadata.json`) reside in the `models/` folder, while training data lives in `data/`. All components run in the same process space, simplifying deployment and local development.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

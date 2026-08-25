# Salary Predictor

Predict salaries from job details using a trained Random Forest model via a simple Flask API and web UI.

## Overview

Salary Predictor is a monolithic, API‑first application that lets users input job attributes (title, location, experience, etc.) through a static web page and receive a salary estimate. The backend Flask service loads a pre‑trained Random Forest regressor (stored in `models/rf_regressor.pkl`) and exposes a `/predict` endpoint. Model training is performed separately via `backend/train_model.py` on the historical dataset `data/Position_Salaries.csv`, producing the serialized model and metadata.

## Features

- Interactive HTML/CSS/JS frontend (`frontend/index.html`) for data entry and result display.
- Flask API (`backend/app.py`) that loads the Random Forest model and serves real‑time salary predictions.
- Standalone training script (`backend/train_model.py`) that builds and serializes the model from `data/Position_Salaries.csv`.
- Persisted model artifacts (`models/rf_regressor.pkl`, `models/metadata.json`) for reproducible inference.
- All dependencies listed in `backend/requirements.txt` (Flask, scikit-learn, pandas, etc.).

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment and install backend dependencies
python -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`
pip install -r backend/requirements.txt

# (Optional) Retrain the model – this will update `models/rf_regressor.pkl` and `models/metadata.json`
python backend/train_model.py

# Start the Flask API server
python backend/app.py
```
Then open `frontend/index.html` in a browser and use the form to get salary predictions.
```

## Architecture

The application is a single monolith where the Flask backend provides a JSON‑based prediction API consumed by a static HTML/JS frontend. Model training is a separate offline step that produces a serialized Random Forest model stored under `models/`. The API loads this artifact at startup, keeping inference fast and decoupled from the training pipeline.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

# Salary-Predictor

Predict employee salaries from job attributes via a Flask API and simple web UI.

## Overview

Salary-Predictor is a monolithic, API‑first application that trains a Random Forest regression model on a public salary dataset and serves predictions through a Flask backend. The backend exposes a `/predict` endpoint consumed by a static HTML/JavaScript frontend, allowing users to input job details and receive an estimated salary in real time. Model training, serialization, and metadata are managed in the `backend/` and `models/` directories, while the raw dataset lives in `data/`.

## Features

- Web UI (`frontend/index.html`) with a simple form for job title, location, experience, and other relevant fields.
- Flask API (`backend/app.py`) exposing a `POST /predict` endpoint that returns JSON `{ "salary": <float> }`.
- End‑to‑end training script (`backend/train_model.py`) and Jupyter notebook for exploratory data analysis and model experimentation.
- Serialized scikit‑learn Random Forest model (`models/rf_regressor.pkl`) with accompanying `metadata.json` describing training parameters and data version.
- Requirements file (`backend/requirements.txt`) pinning Flask, scikit‑learn, pandas, and other dependencies.
- Sample dataset (`data/Position_Salaries.csv`) used for reproducible training and testing.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a Python virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain the model – ensures you have the latest artifacts
python backend/train_model.py

# Start the Flask API
python backend/app.py
# The API will be available at http://127.0.0.1:5000

# In another terminal, open the frontend
open frontend/index.html   # macOS
# or double‑click the file on Windows/Linux and use the form to submit predictions.
```
```

## Architecture

Monolith – API‑first: a single Flask service hosts both the prediction API and static assets, keeping the codebase simple while cleanly separating request handling from model logic.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

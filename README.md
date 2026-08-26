# Salary Predictor

Predict employee salaries using a trained Random Forest model via a simple web interface.

## Overview

The Salary Predictor project provides an end‑to‑end solution for estimating salaries based on job position data. It ingests the `Position_Salaries.csv` dataset, trains a Random Forest regression model, serialises the model to `rf_regressor.pkl`, and serves predictions through a Flask‑based API. A static HTML frontend collects user inputs and displays the predicted salary, making the tool accessible without any local Python setup beyond the backend server.

## Features

- Data Ingestion: Loads and preprocesses `data/Position_Salaries.csv` to create training features and targets.
- Model Training: `backend/train_model.py` trains a scikit‑learn Random Forest regressor and saves the model artifact (`models/rf_regressor.pkl`).
- Prediction API: `backend/app.py` implements a Flask API endpoint (`/predict`) that accepts JSON payloads and returns salary predictions.
- Frontend UI: `frontend/index.html` provides a user‑friendly form that posts data to the API and renders the result.
- Model Metadata: `models/metadata.json` stores training parameters and feature schema for reproducibility.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a Python virtual environment
python -m venv venv
source venv/bin/activate  # on Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Train the model from scratch
python backend/train_model.py

# Start the Flask API server
python backend/app.py
# The API will be available at http://127.0.0.1:5000/predict

# Open the UI in a browser (no additional server needed)
open frontend/index.html  # macOS
# or use any file explorer to open `frontend/index.html`
```
```

## Architecture

The repository follows a monolithic, API‑first architecture: a single Flask application houses both the model loading logic and the prediction endpoint, while a separate static HTML page acts as the client. All components live in the same repository, enabling straightforward development, testing, and deployment.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

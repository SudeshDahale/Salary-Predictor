# Salary Predictor

Predict future salaries based on historical position data using a trained Random Forest model.

## Overview

The Salary Predictor repository provides a simple web‑based tool that estimates a candidate's expected salary given role, experience, and location. A Flask API (backend) loads a pre‑trained Random Forest regressor stored as a pickle file and serves prediction endpoints, while a static HTML page (frontend) collects user input and displays the results. The model is trained from the CSV dataset in the `data/` folder using the training script `backend/train_model.py`.

## Features

- Static HTML frontend (`frontend/index.html`) that captures user inputs and renders salary predictions.
- Flask API (`backend/app.py`) exposing `/predict` endpoint for real‑time inference.
- Pre‑trained Random Forest regressor (`models/rf_regressor.pkl`) with accompanying metadata (`models/metadata.json`).
- Training script (`backend/train_model.py`) to retrain the model on `data/Position_Salaries.csv` and export the updated pickle and metadata.
- All dependencies listed in `backend/requirements.txt` for reproducible environment setup.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain the model
python backend/train_model.py

# Start the Flask API server
python backend/app.py &

# Open the frontend in a browser
open frontend/index.html   # macOS; use `xdg-open` on Linux or double‑click on Windows
```
```

## Architecture

The project follows a monolithic, API‑first design: a single Flask service implements the business logic and prediction API, while the static frontend directly calls this API. Model artifacts and training data reside within the repository, making the entire stack self‑contained and easy to deploy.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

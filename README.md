# Salary Predictor

Predict employee salaries based on job position, experience, and other factors using a trained RandomForest model.

## Overview

Salary Predictor is a monolithic, API‑first web application that lets users enter job details via a simple HTML/JavaScript UI and receive a salary estimate instantly. The backend, built with Flask, loads a pre‑trained RandomForestRegressor (pickled in `models/rf_regressor.pkl`) and serves a `/predict` REST endpoint. A separate training script (`backend/train_model.py`) can re‑train the model on the provided CSV dataset (`data/Position_Salaries.csv`).

## Features

- Web UI for entering job position, years of experience, and other attributes.
- RESTful `/predict` endpoint that returns a JSON salary prediction.
- Training script to rebuild the RandomForestRegressor from `data/Position_Salaries.csv`.
- Pickled model (`models/rf_regressor.pkl`) loaded at runtime for fast inference.
- Requirements managed via `backend/requirements.txt`.

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

# (Optional) Retrain the model if you modify the dataset
python backend/train_model.py

# Run the Flask API
export FLASK_APP=backend/app.py
flask run   # defaults to http://127.0.0.1:5000

# Open the UI in a browser
open frontend/index.html   # or manually open the file in your browser
```
```

## Architecture

The project follows a monolithic, API‑first architecture: a Flask API (`backend/app.py`) handles prediction requests, while a static frontend (`frontend/index.html` + assets) consumes the API. Model training lives in `backend/train_model.py` and produces a pickle file stored under `models/`. All components run together in a single process during development.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

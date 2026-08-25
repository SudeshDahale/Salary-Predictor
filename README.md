# Salary Predictor

Predict employee salaries using a trained Random Forest model via a Flask API and web UI.

## Overview

The Salary Predictor project combines a data pipeline, model training, and a Flask‑based prediction service with a simple static web interface. Raw salary data from `data/Position_Salaries.csv` is ingested, used to train a Random Forest regression model (`backend/train_model.py`), and the trained model is serialized to `models/rf_regressor.pkl`. The Flask API (`backend/app.py`) loads this pickle, exposes a `/predict` endpoint, and the front‑end (`frontend/index.html`) collects user input and displays the predicted salary.

## Features

- Data ingestion from CSV with optional re‑training capability
- Random Forest regression model training and serialization to a pickle file
- Flask API that loads the serialized model and returns salary predictions in JSON
- Static HTML/CSS/JS front‑end for interactive salary prediction
- All dependencies declared in `backend/requirements.txt` for reproducible environment

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up Python virtual environment
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# Install backend dependencies
pip install -r backend/requirements.txt

# (Optional) Retrain the model – will overwrite models/rf_regressor.pkl
python backend/train_model.py

# Start the Flask prediction service
python backend/app.py
# The API will be available at http://127.0.0.1:5000

# Open the UI in a browser
open frontend/index.html   # or manually open the file in any browser
```
```

## Architecture

The application follows a monolithic, API‑first design. Core components—data ingestion, model training, and the Flask prediction service—reside in the `backend` package and share the same runtime. The front‑end is a static web page that communicates with the Flask API via HTTP, keeping the UI decoupled while preserving a single deployable unit.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

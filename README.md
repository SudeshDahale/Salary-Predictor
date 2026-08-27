# Salary Predictor

A Flask‑based web app that predicts employee salaries from job titles using a trained Random Forest model.

## Overview

Salary Predictor combines a lightweight Flask API with a simple HTML/JS front‑end to deliver real‑time salary estimates. The repository includes a data preparation script, a model‑training utility that generates a serialized Random Forest regressor, and a monolithic API‑first architecture where the front‑end talks to `/predict` (and optionally `/retrain`) endpoints exposed by `backend/app.py`.

## Features

- Interactive web UI (`frontend/index.html`) that collects job position details and displays predicted salary.
- Flask API (`backend/app.py`) exposing `/predict` for inference and `/retrain` for optional model retraining.
- Model training script (`backend/train_model.py`) that reads `data/Position_Salaries.csv`, fits a Random Forest regressor, and stores the artifact in `models/rf_regressor.pkl` with accompanying `metadata.json`.
- Persisted model and metadata in the `models/` directory for fast loading during inference.
- All Python dependencies listed in `backend/requirements.txt` (Flask, scikit‑learn, pandas, joblib, etc.).

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Train the model (creates models/rf_regressor.pkl and metadata.json)
python backend/train_model.py

# Launch the Flask API
python backend/app.py
```

# In a separate terminal, open the UI
open frontend/index.html   # macOS
# or use any browser to open the file directly on Windows/Linux.
```

## Architecture

Monolithic API‑First design – a single Flask service (`backend/app.py`) hosts all REST endpoints, while the static front‑end (`frontend/`) consumes these endpoints. The model artifact lives in `models/`, enabling the API to load it at startup for inference.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

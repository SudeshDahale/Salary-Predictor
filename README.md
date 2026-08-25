# Salary Predictor

Predict employee salaries using a trained Random Forest model via a Flask API and simple web UI.

## Overview

Salary Predictor is a monolithic, API‑first application that ingests raw salary data, trains a Random Forest Regressor, and exposes the model through a Flask REST endpoint. A lightweight static HTML front‑end collects user inputs and displays the predicted salary in real time. The project is organized into clear backend and frontend modules, making it easy to extend or replace any component.

## Features

- Data ingestion and minimal preprocessing of `data/Position_Salaries.csv` using pandas.
- Training of a Random Forest Regressor (`train_model.py`) with scikit‑learn and serialization to `models/rf_regressor.pkl`.
- Flask‑based prediction API (`backend/app.py`) that loads the serialized model and returns JSON salary predictions.
- Static HTML/CSS front‑end (`frontend/index.html`) that gathers user input, calls the API, and displays the predicted salary.
- Model metadata (`models/metadata.json`) documenting training parameters and feature schema.

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

# Train the model (creates models/rf_regressor.pkl and models/metadata.json)
python backend/train_model.py

# Start the Flask prediction service
python backend/app.py
# The API will be available at http://127.0.0.1:5000/predict

# In a separate terminal, open the front‑end (no server needed for static files)
# e.g., using the default file explorer or a simple HTTP server
python -m http.server 8000 --directory frontend
# Then navigate to http://localhost:8000 in a browser.
```
```

## Architecture

The repository follows a **Monolith, API‑First** architecture. All server‑side code lives under `backend/` – `app.py` boots a Flask API that loads `models/rf_regressor.pkl`, while `train_model.py` handles data ingestion from `data/Position_Salaries.csv`, preprocessing with pandas, and model training with scikit‑learn. The trained model and its metadata are stored in `models/`. The client side consists of static files in `frontend/` (e.g., `index.html`, CSS, images) that call the `/predict` endpoint and render results. No separate micro‑services or containers are required; the entire stack runs as a single process.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

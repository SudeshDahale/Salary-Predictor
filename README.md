# Salary Predictor

Estimate software job salaries with a trained Random Forest model via a Flask API and simple web UI.

## Overview

Salary Predictor is a monolithic, API‑first application that trains a Random Forest regression model on a CSV of job positions and salaries, persists the model, and serves predictions through a Flask endpoint. A lightweight HTML/JavaScript frontend posts user‑provided job attributes to the API and displays the estimated salary.

The repository contains a training script, the Flask API, the trained model artifact, and a static web page that together form a self‑contained salary estimation service.

## Features

- 📊 **Model Training** – `train_model.py` reads `data/Position_Salaries.csv`, preprocesses features with pandas, trains a scikit‑learn Random Forest regressor, and saves the model (`models/rf_regressor.pkl`) alongside metadata (`models/metadata.json`).
- 🚀 **Prediction API** – `backend/app.py` exposes a `/predict` POST endpoint that validates incoming JSON, loads the persisted model, and returns a salary estimate.
- 🖥️ **Static Frontend** – `frontend/index.html` provides a user‑friendly form, uses vanilla JavaScript to call the API, and displays the predicted salary without any build step.
- 🔁 **API‑First Design** – All business logic lives in the Flask service; the frontend is a thin client that only consumes the API, making the backend reusable for other clients.
- ⚙️ **Reproducible Environment** – `backend/requirements.txt` pins exact versions of Flask, scikit‑learn, pandas, and other dependencies.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a Python virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate   # on Windows use `venv\Scripts\activate`

# Install backend dependencies
cd backend
pip install -r requirements.txt

# (Optional) Retrain the model – will overwrite the existing pickle
python train_model.py

# Start the Flask API (runs on http://127.0.0.1:5000 by default)
python app.py

# In a new terminal, open the static UI
open ../frontend/index.html   # macOS; use `xdg-open` on Linux or double‑click on Windows

# Fill in the form and press "Predict" – the UI will POST to the API and display the estimated salary.
```

## Architecture

The project follows a monolithic, API‑first architecture. All server‑side code lives in the `backend/` package, where Flask hosts both the prediction REST endpoint and serves the static HTML/JS files. The trained scikit‑learn model is stored as a pickle (`models/rf_regressor.pkl`) and loaded on demand. The frontend (`frontend/index.html`) is a thin client that communicates exclusively via HTTP, keeping the UI decoupled from the model logic while still being packaged in the same repository.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

# Salary Predictor

Predict employee salaries using a trained Random Forest regression model via a simple web UI.

## Overview

The Salary Predictor project provides an end‑to‑end solution for estimating employee salaries based on position, experience, and other features. A Flask‑based backend exposes REST endpoints for model training and salary prediction, while a static HTML frontend collects user input and displays results. Training data lives in the `data/` folder, and the trained model along with its metadata are stored under `models/` for reuse.

## Features

- REST API for training (`/train`) and predicting (`/predict`) salaries built with Flask.
- Persisted Random Forest regression model (`models/rf_regressor.pkl`) and associated metadata (`models/metadata.json`).
- Static HTML frontend (`frontend/index.html`) that calls the backend API and renders predictions.
- Jupyter notebook (`random_forest_regression.ipynb`) demonstrating exploratory data analysis and model evaluation.
- All Python dependencies are captured in `backend/requirements.txt`.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate

# Install backend dependencies
pip install -r backend/requirements.txt

# Run the Flask API (default runs on http://127.0.0.1:5000)
python backend/app.py &

# Open the frontend in a browser
xdg-open frontend/index.html   # Linux/macOS
# or simply open frontend/index.html manually in any browser
```

## Architecture

The repository follows a monolithic, API‑first architecture: a single Flask application (`backend/app.py`) implements HTTP endpoints, while the frontend is a separate static site that communicates with those endpoints. Model artefacts and raw data are versioned alongside the code, making the whole pipeline reproducible.

- **frontend** – static HTML/JS UI for user interaction.
- **backend** – Flask service exposing `/train` and `/predict` routes; uses `train_model.py` to fit a Random Forest and stores results in `models/`.
- **model_store** – `models/` directory holds the serialized model and a JSON metadata file.
- **dataset** – `data/Position_Salaries.csv` contains the raw salary dataset used for training.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

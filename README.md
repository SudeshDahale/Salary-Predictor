# Salary Predictor

A Flask‑based web app that predicts employee salaries using a pre‑trained Random Forest model.

## Overview

The Salary Predictor project provides a simple monolithic, API‑first application that lets users input job details through a static HTML/JS front‑end and receive salary predictions from a Flask back‑end powered by scikit‑learn. The repository includes the pre‑trained Random Forest model, training scripts, the raw salary dataset, and all necessary UI assets.

## Features

- Web UI (frontend) built with HTML, CSS, and JavaScript for intuitive salary input and result display.
- Flask API (backend) exposing a `/predict` endpoint that returns JSON predictions.
- Pre‑trained Random Forest regressor stored in `models/rf_regressor.pkl` with accompanying `models/metadata.json`.
- Training pipeline (`backend/train_model.py`) that reads `data/Position_Salaries.csv` and produces the model artifact.
- Docker‑ready requirements file (`backend/requirements.txt`) listing Flask, scikit‑learn, pandas, and other dependencies.
- Jupyter notebook (`random_forest_regression.ipynb`) documenting exploratory data analysis and model evaluation.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`

# Install back‑end dependencies
pip install -r backend/requirements.txt

# Run the Flask server
python backend/app.py
```

Open `http://127.0.0.1:5000` in a browser to access the UI.
```

## Architecture

The app follows a monolithic, API‑first design: the Flask server (`backend/app.py`) serves the `/predict` REST endpoint and also hosts the static files from `frontend/`. The front‑end makes AJAX calls to the back‑end, which loads the serialized Random Forest model from the `models/` directory and returns the predicted salary. Training utilities reside in the same repository, allowing the model to be re‑trained on the CSV data when needed.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

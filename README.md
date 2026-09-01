# Salary Predictor

Predict employee salaries with a trained Random Forest model via a Flask web app.

## Overview

Salary Predictor is a monolithic Python application that lets users estimate salaries based on job attributes. A static HTML frontend (frontend/index.html) gathers input, which is sent to a Flask backend (backend/app.py). The backend loads a pre‑trained Random Forest regressor (models/rf_regressor.pkl) and its metadata (models/metadata.json) to generate predictions on‑the‑fly. The model is produced by a training script (backend/train_model.py) that consumes the CSV dataset (data/Position_Salaries.csv) and stores the artifact for inference. The entire stack—HTML, Flask, scikit‑learn, and Pickle—runs together without external services.

## Features

- Static HTML UI for easy salary input and result display.
- Flask API that loads a serialized Random Forest model and returns predictions as JSON.
- Training pipeline (train_model.py) that reads the Position_Salaries.csv dataset, fits a Random Forest regressor, and saves both the model pickle and metadata.
- Model versioning via metadata.json for reproducibility.
- All dependencies listed in backend/requirements.txt for reproducible environments.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Run the Flask app (will serve the static frontend as well)
python app.py
```

Visit `http://127.0.0.1:5000` in a browser to use the predictor.

*To retrain the model:*
```bash
python train_model.py   # Generates models/rf_regressor.pkl and models/metadata.json
```
```

## Architecture

Monolithic architecture: a single Flask process serves both the HTML frontend and the prediction endpoint, while the trained model resides in the models directory. The data layer (CSV) is used only during training; inference uses the pickled model and metadata.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

# Salary Predictor Technical Architecture Guide

## System Overview
The Salary Predictor is a monolithic, API‑first application built with Python and Flask. It combines a data ingestion pipeline, a machine‑learning training component, a prediction REST endpoint, and a static web UI. All components reside in a single codebase (backend/, frontend/, models/, data/), enabling rapid prototyping while keeping the API contract clear for future decoupling.

## System Layers
### Data Ingestion Layer
**Technologies:** pandas, CSV

Loads the raw salary dataset (data/Position_Salaries.csv) using pandas, performs minimal preprocessing, and supplies a DataFrame to the training script.

### Model Training Layer
**Technologies:** scikit‑learn, pickle, Python

Implements a Random Forest regression model (sklearn) in backend/train_model.py, trains on the ingested DataFrame, evaluates basic metrics, and serializes the trained model to models/rf_regressor.pkl along with metadata (models/metadata.json).

### Prediction Service Layer
**Technologies:** Flask, Python, pickle

A Flask application (backend/app.py) that loads the serialized model at startup, exposes a /predict POST endpoint, validates incoming JSON payload, runs inference, and returns the predicted salary as JSON.

### User Interface Layer
**Technologies:** HTML, CSS, JavaScript

Static HTML/CSS/JavaScript (frontend/index.html) that collects user inputs, calls the /predict API via fetch/AJAX, and displays the returned salary. Assets are stored under assets/.



## Data Flow & Pipelines
1. The CSV file in data/Position_Salaries.csv is read by backend/train_model.py → 2. A RandomForestRegressor is trained and serialized to models/rf_regressor.pkl (with metadata.json) → 3. backend/app.py starts, loads the pickle model into memory → 4. A user opens frontend/index.html, enters job features, and clicks "Predict" → 5. JavaScript sends a POST request with the feature JSON to Flask's /predict endpoint → 6. Flask deserializes the request, invokes model.predict, and returns a JSON response containing the salary → 7. The UI displays the result to the user.

## Key Design Decisions
- Chosen an API‑first approach to keep the prediction logic reusable beyond the static UI.
- Used a single monolithic repository to simplify deployment and environment management for a proof‑of‑concept.
- Serialized the trained model with pickle for fast load time; trade‑off is limited cross‑language portability.
- Random Forest was selected for its robustness on tabular salary data and minimal hyper‑parameter tuning.
- Static assets are served directly by Flask in development; production can offload to a CDN.
- Input validation performed both client‑side (JS) and server‑side (Flask) to guard against malformed payloads.

## Scalability & Reliability
While the current monolith suffices for low traffic, scaling can be addressed by: • Containerizing the Flask API (Docker) and deploying multiple replicas behind a load balancer. • Moving the model file to a model‑registry (e.g., MLflow) and loading it lazily to support versioning. • Replacing the in‑process Flask server with a WSGI server (Gunicorn) or an ASGI framework for asynchronous handling. • Decoupling the UI into a separate static site hosted on a CDN, reducing load on the API. • Introducing a feature store or database for larger datasets, enabling incremental model retraining without re‑reading the entire CSV.

# Salary Predictor Technical Architecture Guide

## System Overview
The Salary Predictor application is a monolithic web service built with Python and Flask that serves a static HTML frontend and a machine‑learning inference backend. Users interact via a simple form on `frontend/index.html`, which posts the feature values to a Flask endpoint defined in `backend/app.py`. The backend loads a pre‑trained Random Forest regressor (`models/rf_regressor.pkl`) along with its metadata (`models/metadata.json`) and returns a salary prediction. Model training lives in the same repository (`backend/train_model.py` and `random_forest_regression.ipynb`) and produces the model artifact stored under `models/`. All dependencies are listed in `backend/requirements.txt`.

## System Layers
### Presentation Layer
**Technologies:** HTML5, CSS3, Vanilla JavaScript

Static assets that collect input and render predictions. Implemented as plain HTML, CSS, and JavaScript in `frontend/index.html` and supporting images under `assets/`.

### Application Layer
**Technologies:** Python 3.x, Flask, Werkzeug, Gunicorn (optional)

Flask web server that exposes the `/predict` endpoint, performs request validation, loads the ML model, and returns JSON responses. Core code resides in `backend/app.py`. Dependency management is defined in `backend/requirements.txt`.

### Model & Data Layer
**Technologies:** scikit-learn, pickle, pandas

Contains the trained Random Forest regressor (`models/rf_regressor.pkl`), model metadata (`models/metadata.json`), and the original training data (`data/Position_Salaries.csv`). Training scripts (`backend/train_model.py` and `random_forest_regression.ipynb`) use scikit‑learn to produce the model artifact.



## Data Flow & Pipelines
1. **User Interaction** – The browser loads `frontend/index.html` and the user fills the salary‑related fields (e.g., position, years of experience). 2. **Form Submission** – The form issues an HTTP POST request to `/predict` (Flask route in `backend/app.py`). 3. **Request Handling** – Flask parses the JSON payload, validates required fields, and forwards the feature vector to the inference service. 4. **Model Loading** – On first request, `backend/app.py` lazily loads the serialized Random Forest model (`models/rf_regressor.pkl`) using Python's `pickle` module; subsequent requests reuse the in‑memory model. 5. **Prediction** – The feature vector is passed to `model.predict()`, producing a salary estimate. 6. **Response** – Flask returns a JSON response containing the predicted salary. 7. **Display** – The frontend JavaScript updates the UI with the prediction result.

## Key Design Decisions
- Use of **Flask** for a lightweight, single‑process API that aligns with the monolithic deployment model.
- Model serialization with **pickle** (`rf_regressor.pkl`) for fast loading; acceptable because the model is internal and the repository is not exposed to untrusted inputs.
- Separate **frontend** (static HTML) from **backend** (Flask) while keeping both in the same codebase to simplify deployment and versioning.
- Training pipeline is part of the repository, enabling reproducibility: `backend/train_model.py` reads the CSV, trains a Random Forest, and writes the model and metadata.
- Configuration kept minimal – all runtime dependencies are pinned in `backend/requirements.txt`.

## Scalability & Reliability
The current monolith is suitable for low‑to‑moderate traffic. To scale horizontally:
- **Containerize** the Flask app (Docker) and run multiple replicas behind a load balancer.
- Use a **WSGI server** such as Gunicorn with multiple worker processes to leverage multi‑core CPUs.
- Persist the model artifact in a shared location (e.g., S3 or a network file system) so that new replicas can load it without bundling it in the image.
- Cache the loaded model in each worker to avoid repeated disk I/O.
- If request volume grows dramatically, consider extracting the inference step into a separate microservice or deploying the model via a model‑serving framework (e.g., TensorFlow Serving, TorchServe) while keeping the existing Flask front‑end as a thin gateway.

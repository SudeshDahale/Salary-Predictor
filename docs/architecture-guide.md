# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first salary prediction service built with Python, Flask, and scikit‑learn. A static HTML front‑end collects user input (e.g., job position, years of experience) and calls a Flask endpoint that loads a pre‑trained RandomForestRegressor model to return a salary estimate. The codebase is organized into clear functional modules—frontend, backend, model, and data—each residing in its own directory. This guide documents the system layers, component interactions, data pipeline, key design decisions, and scalability considerations.

## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static HTML/JS UI located in `frontend/`. Collects user input and displays predictions. Served directly by Flask's static file handling.

### API Layer
**Technologies:** Python, Flask, Werkzeug

Flask application (`backend/app.py`) exposing HTTP endpoints (e.g., `/predict`). Handles request validation, routing, and response formatting.

### Inference Layer
**Technologies:** scikit-learn, pickle

Loads the persisted scikit‑learn model (`models/rf_regressor.pkl`) and metadata (`models/metadata.json`). Performs feature preprocessing (if any) and returns a salary prediction.

### Training/Data Layer
**Technologies:** pandas, scikit-learn, Jupyter Notebook

Contains raw historical salary data (`data/Position_Salaries.csv`) and training scripts (`backend/train_model.py`, `random_forest_regression.ipynb`). Generates the model artifact and metadata.

### Infrastructure Layer
**Technologies:** pip, virtualenv

Dependency management (`backend/requirements.txt`) and optional VS Code configuration (`.vscode/settings.json`). Provides the runtime environment for the monolith.



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html`, fills out the salary request form, and clicks *Predict*.
2. **HTTP Request** – The form submits a JSON payload (position, experience, etc.) via an HTTP POST to the Flask endpoint defined in `backend/app.py` (e.g., `/predict`).
3. **Backend Processing** – `app.py` validates the request, deserializes the payload, and forwards the feature vector to the model inference layer.
4. **Model Inference** – The inference code loads `models/rf_regressor.pkl` (a pickled `RandomForestRegressor`) and optional metadata from `models/metadata.json`. It computes the predicted salary and returns the value.
5. **Response** – The Flask endpoint returns a JSON response containing the predicted salary.
6. **UI Update** – JavaScript in `index.html` parses the JSON response and displays the salary prediction to the user.
7. **Model Retraining (offline)** – Data scientists run `backend/train_model.py` (or the Jupyter notebook `random_forest_regression.ipynb`) which reads `data/Position_Salaries.csv`, trains a new RandomForestRegressor, and overwrites `models/rf_regressor.pkl` and `models/metadata.json`.
8. **Deployment** – The entire monolith (frontend static assets + Flask service) can be containerized or deployed on a VM, exposing port 5000 (default Flask) to serve both static UI and API.

## Key Design Decisions
- Monolithic, API‑first design simplifies deployment: a single Flask process serves both static UI and prediction API.
- Choosing scikit‑learn's RandomForestRegressor balances interpretability, training speed, and prediction latency for tabular salary data.
- Persisting the model with pickle keeps the runtime lightweight; model loading occurs once at startup to avoid per‑request I/O.
- Separating training code from inference (`train_model.py` vs. `app.py`) enables offline model updates without affecting the serving process.
- Using static HTML for the front‑end eliminates the need for a separate SPA framework, reducing bundle size and complexity.

## Scalability & Reliability
The current monolith is suitable for low‑to‑moderate traffic (hundreds of requests per minute). To scale:
- **Horizontal scaling**: Containerize the Flask app (Docker) and run multiple replicas behind a load balancer (e.g., Nginx, AWS ELB). The static UI can be offloaded to a CDN.
- **Model serving optimization**: Load the model once per worker process; for large models, consider using a dedicated model server (e.g., TensorFlow Serving, TorchServe) or a lightweight inference microservice.
- **Caching**: Cache frequent predictions (e.g., based on identical input tuples) using an in‑memory store like Redis to reduce CPU load.
- **Asynchronous processing**: For heavy preprocessing, move to a task queue (Celery) and return a job ID, though the current model inference is fast enough to remain synchronous.
- **Data pipeline**: Automate periodic retraining by scheduling `train_model.py` (cron, Airflow) and swapping the model artifact atomically.
Overall, the architecture can evolve from a single-process monolith to a micro‑service ecosystem without major refactoring, thanks to the clear API contract.

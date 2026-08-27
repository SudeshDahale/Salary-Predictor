# Technical Architecture Guide – Salary-Predictor

## System Overview
Salary-Predictor is a monolithic, API‑first application that predicts employee salaries based on job title and other input features. The system is built with Python and Flask for the backend, scikit‑learn for the machine‑learning model, and plain HTML/CSS/JavaScript for the frontend UI. All components reside in a single repository, with a clear separation of concerns into frontend, backend, model training, and data/model storage modules.

## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static assets that provide the user interface. Includes `frontend/index.html`, CSS, and JavaScript files that collect input and display predictions.

### API Layer
**Technologies:** Python, Flask

Flask application exposing HTTP endpoints for prediction (and optional training). Core code lives in `backend/app.py` and routes are defined here.

### Model Inference Layer
**Technologies:** scikit-learn, Python

Loads the serialized Random Forest model (`models/rf_regressor.pkl`) and associated `models/metadata.json`. Performs prediction using scikit‑learn.

### Training Layer
**Technologies:** Python, scikit-learn, pandas

Standalone script `backend/train_model.py` that reads the CSV dataset (`data/Position_Salaries.csv`), trains a `RandomForestRegressor`, evaluates it, and writes the model artifact and metadata to the `models/` directory.

### Data & Model Store
**Technologies:** CSV, Pickle

Versioned raw data and model artifacts stored in the repository. The CSV provides the training ground truth; the `.pkl` file holds the trained model.



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html` in a browser and fills out the salary query form. 2. **API Request** – The form triggers a JavaScript `fetch` call to the Flask endpoint defined in `backend/app.py` (e.g., `/predict`). 3. **Inference** – The Flask handler loads the serialized Random Forest model from `models/rf_regressor.pkl` (metadata in `models/metadata.json`) and runs `model.predict` on the supplied features. 4. **Response** – The predicted salary is returned as JSON and rendered back in the UI. 5. **Model Retraining (optional)** – An administrative endpoint (if exposed) calls `backend/train_model.py`, which reads `data/Position_Salaries.csv`, fits a new `RandomForestRegressor`, and overwrites the model artifact and metadata. 6. **Persistence** – Trained model artifacts are stored under `models/` and the raw dataset remains under `data/` for reproducibility.

## Key Design Decisions
- Monolithic repository – all code (frontend, backend, training scripts, data, models) lives in one repo, simplifying deployment for a small‑scale service.
- API‑first approach – the Flask app defines clear JSON endpoints (`/predict`, optional `/train`) that decouple the UI from the inference logic.
- Model artifact versioning – persisting the Random Forest model as `rf_regressor.pkl` alongside a JSON metadata file enables reproducible inference without retraining on every request.
- Separation of training logic – `train_model.py` is isolated from the request handling code, allowing model updates without affecting the API runtime.
- Minimal dependency footprint – `backend/requirements.txt` lists only Flask and scikit‑learn (plus pandas), keeping the container image lightweight.

## Scalability & Reliability
Because the application is monolithic, scaling is currently achieved by replicating the entire service behind a load balancer. The stateless Flask API can run in multiple containers (Docker or virtualenv) without shared memory, as the model is loaded read‑only from the filesystem. For higher throughput, the following can be considered:
- **Model caching** – Load the model once at app start and reuse the object across requests (already implied by `app.py`).
- **Horizontal scaling** – Deploy multiple instances behind an Nginx/HAProxy reverse proxy.
- **Asynchronous inference** – Offload prediction to a background worker (e.g., Celery) if request latency becomes a bottleneck.
- **Model versioning** – Store model artifacts in an external object store (S3, GCS) and load them on startup to avoid large repository clones.
- **Containerization** – Package the backend with Docker, pinning Python and library versions from `backend/requirements.txt` for reproducible deployments.

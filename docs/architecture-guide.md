# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first application that predicts employee salaries based on job characteristics. The system is built with Python and Flask for the backend API, scikit‑learn for the machine‑learning model, and plain HTML/CSS for the front‑end UI. A pre‑trained RandomForestRegressor model is serialized with Pickle and stored under `models/`. The training pipeline (`backend/train_model.py` and `random_forest_regression.ipynb`) reads raw salary data from `data/Position_Salaries.csv`, trains the model, and writes both the model file (`models/rf_regressor.pkl`) and associated metadata (`models/metadata.json`). The front‑end (`frontend/index.html`) collects user input, sends it to the Flask API (`backend/app.py`), receives a JSON salary prediction, and renders the result. All source files are organized under clear directories (`backend/`, `frontend/`, `models/`, `data/`).

## System Layers
### Presentation Layer (UI)
**Technologies:** HTML, CSS, JavaScript (fetch API)

Static HTML page (`frontend/index.html`) with CSS assets that collects job parameters from the user and displays predictions. No server‑side rendering; all UI logic runs in the browser.

### API Layer
**Technologies:** Python, Flask

Flask application (`backend/app.py`) exposing RESTful endpoints (`/predict`). Handles request parsing, input validation, and response formatting. Acts as the single entry point for the monolithic service.

### Prediction Service
**Technologies:** scikit‑learn, Pickle

Business logic that receives a feature vector, invokes the serialized model, and returns a salary forecast. Model loading is performed on first request and cached for subsequent calls.

### Model Management
**Technologies:** Pickle, JSON

Responsible for persisting the trained model (`models/rf_regressor.pkl`) and associated metadata (`models/metadata.json`). Provides helper functions for serialization/deserialization and version tracking.

### Training Pipeline
**Technologies:** Python, pandas, scikit‑learn, Jupyter

Standalone script (`backend/train_model.py`) and Jupyter notebook (`random_forest_regression.ipynb`) that ingest raw data (`data/Position_Salaries.csv`), perform feature engineering, train a `RandomForestRegressor`, evaluate performance, and output the model and metadata files.

### Data Layer
**Technologies:** CSV

Source CSV dataset (`data/Position_Salaries.csv`) used for model training. No runtime database is required; the model is the only persistent artifact for inference.



## Data Flow & Pipelines
1. User fills HTML form → 2. Browser sends POST /predict → 3. Flask parses JSON → 4. Feature vector passed to Prediction Service → 5. Model (Pickle) loaded if needed → 6. RandomForestRegressor predicts → 7. JSON response sent back → 8. UI updates with salary.

**File‑level trace**:
`frontend/index.html` → `fetch('/predict', {...})` → `backend/app.py` (route `/predict`) → `backend/prediction_service.py` (load `models/rf_regressor.pkl`) → Return to `app.py` → JSON → Browser.

## Key Design Decisions
- API‑first approach: All UI interactions are mediated through a REST endpoint, making the back‑end reusable for other clients (e.g., mobile apps).
- Monolithic deployment: Both UI static files and Flask API reside in the same repository, simplifying local development and CI pipelines.
- Pickle for model serialization: Chosen for its simplicity and native compatibility with scikit‑learn objects; accompanied by a JSON metadata file to avoid feature‑order mismatches.
- Separate training pipeline: Training code lives outside the serving codebase, allowing model updates without redeploying the API if the model file is swapped.
- Minimal dependencies: `backend/requirements.txt` pins only Flask and scikit‑learn, keeping the runtime lightweight.

## Scalability & Reliability
While the current implementation runs as a single‑process Flask app, several scalability paths are viable:
- **Horizontal scaling**: Deploy multiple instances behind a load balancer (e.g., Nginx or cloud LB). Because the model is read‑only after load, each instance can cache the Pickle file in memory without contention.
- **Process workers**: Use a production WSGI server such as Gunicorn with multiple worker processes/threads to utilize multi‑core CPUs.
- **Containerization**: Dockerize the `backend/` folder; containers can be orchestrated with Kubernetes for auto‑scaling based on request latency or CPU usage.
- **Model versioning**: Store model artifacts in an object store (S3, GCS) and load them on container start, enabling zero‑downtime model swaps.
- **Caching predictions**: For repeated identical requests, an in‑memory cache (e.g., `functools.lru_cache` or Redis) can reduce inference latency.
- **Asynchronous inference**: If future feature engineering becomes heavy, offload prediction to a background worker (Celery) and return a job ID to the client.
These strategies preserve the API‑first contract while allowing the service to handle higher traffic volumes without redesigning the core monolith.

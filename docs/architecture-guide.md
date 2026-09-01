# Technical Architecture Guide – Salary Predictor

## System Overview
The Salary‑Predictor repository implements a monolithic, API‑first web application that predicts employee salaries based on job attributes. The system consists of a lightweight Flask backend (backend/app.py) exposing a JSON prediction endpoint, a static HTML/CSS/JavaScript frontend (frontend/index.html) that collects user input, a pre‑trained scikit‑learn Random Forest model (models/rf_regressor.pkl) with accompanying metadata (models/metadata.json), and a training pipeline (backend/train_model.py, random_forest_regression.ipynb) that ingests the raw salary CSV (data/Position_Salaries.csv). All components live in a single repository, making deployment simple while keeping a clear logical separation between UI, API, model, and data layers.

## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static web UI that captures user input and displays predictions. Implemented with HTML, CSS, and vanilla JavaScript. Served directly by Flask’s static file handling.

### API Layer
**Technologies:** Python, Flask

Flask application (`backend/app.py`) that defines the `/predict` endpoint, handles request validation, loads the model, and returns JSON responses. Dependency list is pinned in `backend/requirements.txt`.

### Model Layer
**Technologies:** scikit‑learn, joblib, JSON

Pre‑trained Random Forest regression model stored as a pickle (`models/rf_regressor.pkl`). Associated metadata (`models/metadata.json`) contains feature schema, model version, and evaluation scores.

### Data Layer
**Technologies:** pandas, CSV

Source dataset (`data/Position_Salaries.csv`) containing historical salary records. Used for both training and offline validation.

### Training Layer
**Technologies:** Python, pandas, scikit‑learn, Jupyter

Python script (`backend/train_model.py`) and Jupyter notebook (`random_forest_regression.ipynb`) that orchestrate data loading, feature engineering, model training, and persistence. This layer is executed manually or via a CI job to refresh the model.



## Data Flow & Pipelines
1. User fills the salary form in the static UI (frontend/index.html) and submits → JavaScript sends a POST request with JSON payload to the Flask prediction API (backend/app.py). 2. The Flask endpoint lazily loads the serialized Random Forest model (models/rf_regressor.pkl) and its metadata (models/metadata.json) using scikit‑learn and pandas. 3. The payload is transformed into a feature vector, passed to the model’s `predict` method, and the result is returned as JSON to the frontend. 4. The UI updates the page with the predicted salary.

Training pipeline (offline):
1. The raw CSV dataset (data/Position_Salaries.csv) is read with pandas in backend/train_model.py (or the exploratory notebook random_forest_regression.ipynb). 2. Data cleaning, feature engineering, and train‑test split are performed. 3. A scikit‑learn `RandomForestRegressor` is fitted, evaluated, and the final model is persisted to models/rf_regressor.pkl via `joblib.dump`. 4. Model hyper‑parameters and performance metrics are written to models/metadata.json for runtime introspection.

## Key Design Decisions
- API‑first approach: The Flask service exposes a clean JSON contract (`/predict`) that decouples the UI from the inference logic, enabling future client diversification (mobile, CLI, etc.).
- Monolithic repository layout: All code, data, and model artifacts reside together, simplifying local development and CI pipelines while still preserving logical module boundaries (frontend, backend, model_store, training_job).
- Model serialization with joblib: Storing the Random Forest as a binary pickle (`rf_regressor.pkl`) enables fast load times (≈ tens of milliseconds) and avoids re‑training on every request.
- Metadata file (`metadata.json`): Provides versioning and schema information at runtime, allowing the API to validate incoming payloads against the exact feature set used during training.
- Explicit dependency lock (`backend/requirements.txt`): Guarantees reproducible environments across development, testing, and production.
- Separation of training and inference code: `train_model.py` contains heavy data processing and model fitting logic, while `app.py` only performs lightweight inference, keeping request latency low.

## Scalability & Reliability
Because the application is monolithic, horizontal scaling can be achieved by running multiple Flask worker processes (e.g., via gunicorn) behind a load balancer. The model object is loaded once per worker, minimizing per‑request overhead. For higher throughput, the model layer could be extracted into a dedicated model‑serving microservice (TensorFlow Serving or a FastAPI wrapper) while keeping the existing UI unchanged. Caching predictions for identical requests (e.g., using Redis) would further reduce compute load. The data layer remains read‑only in production, so the CSV file can be stored on a shared volume or object store without impacting scalability. Continuous integration can automate retraining (`train_model.py`) and artifact promotion to `models/` to keep the service up‑to‑date without downtime.

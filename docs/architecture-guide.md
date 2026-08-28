# Technical Architecture Guide – Salary Predictor

## System Overview
The Salary Predictor repository implements an end‑to‑end machine‑learning powered salary estimation service. It follows a monolithic, API‑first design where a Flask backend provides a REST‑style prediction endpoint and a lightweight static frontend collects user input. The system is built with Python, Flask, scikit‑learn, and standard web technologies (HTML, CSS, JavaScript). Model artifacts are persisted on disk and loaded at runtime for low‑latency inference. All source data originates from a CSV dataset (data/Position_Salaries.csv) that is ingested, transformed, and used to train a Random Forest regressor (backend/train_model.py). The trained model is serialized to models/rf_regressor.pkl alongside metadata (models/metadata.json).

## System Layers
### Data Ingestion
**Technologies:** Python, pandas (implicitly via scikit‑learn)

Loads raw CSV data (`data/Position_Salaries.csv`) and performs any required preprocessing before model training.

### Model Training
**Technologies:** Python, scikit‑learn, pickle

Implements training logic for a Random Forest regressor, evaluates performance, and serialises the trained model and metadata.

### Model Persistence
**Technologies:** File system storage (pkl, json)

Stores the serialized model (`models/rf_regressor.pkl`) and accompanying metadata (`models/metadata.json`) for runtime loading.

### Prediction Service (API Layer)
**Technologies:** Python, Flask, pickle, scikit‑learn

A Flask application (`backend/app.py`) that deserialises the model at start‑up, validates incoming requests, performs inference, and returns JSON responses.

### Frontend UI
**Technologies:** HTML, CSS, JavaScript

Static HTML page (`frontend/index.html`) with CSS and JavaScript that captures user input, calls the prediction API, and renders the salary estimate.



## Data Flow & Pipelines
1. **Data Ingestion** – The CSV file `data/Position_Salaries.csv` is read by `backend/train_model.py`. 2. **Model Training** – Using scikit‑learn (`RandomForestRegressor`), the training script processes the dataset, fits the model, and serialises it with `pickle` to `models/rf_regressor.pkl`; training metadata (e.g., feature list, training date) is written to `models/metadata.json`. 3. **Model Persistence** – The model artifact and metadata reside in the `models/` directory, making them available to the runtime service. 4. **Prediction Service** – The Flask app (`backend/app.py`) loads the model and metadata at start‑up, exposes an HTTP endpoint (e.g., `/predict`) that receives JSON payloads from the frontend. 5. **Frontend UI** – `frontend/index.html` (with accompanying CSS/JS) presents a form; upon submission it issues an AJAX request to the Flask endpoint, receives the predicted salary, and displays it to the user. 6. **Response** – The prediction result is returned as JSON and rendered in the UI.

## Key Design Decisions
- Monolithic repository layout – all backend, model artifacts, and frontend assets reside in a single codebase for simplicity and rapid iteration.
- API‑first approach – the Flask app exposes a clear HTTP contract, enabling the frontend (or any future client) to consume predictions without tight coupling.
- Model serialization with `pickle` – chosen for its native Python compatibility and ease of use with scikit‑learn models.
- Separate `models/` directory – isolates artefacts from source code, facilitating versioning and potential model registry integration.
- Minimal external dependencies – only Flask and scikit‑learn are required, keeping the deployment footprint small.

## Scalability & Reliability
The current monolithic design is sufficient for low‑to‑moderate traffic (e.g., demo or internal usage). To scale horizontally, the Flask service can be containerised (Docker) and deployed behind a load balancer; model loading can be moved to a shared model server (e.g., TensorFlow Serving or a custom gRPC service) to reduce per‑instance memory overhead. For high‑throughput scenarios, consider:
- Caching recent predictions or model metadata in Redis.
- Asynchronous request handling using a production‑grade WSGI server (Gunicorn) with multiple worker processes.
- Storing the CSV dataset and model artefacts in cloud storage (S3, GCS) and loading them on container start‑up.
- Adding CI/CD pipelines that retrain the model automatically on new data and version the artefacts.

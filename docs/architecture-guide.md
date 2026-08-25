# Salary Predictor Technical Architecture Guide

## System Overview
The Salary Predictor repository implements a monolithic, API‑first application that predicts employee salaries based on position data. The solution is built with Python, Flask, scikit‑learn, pandas, and plain HTML/CSS. All backend logic resides under the **backend/** directory while the static user interface lives in **frontend/**. Model artefacts are persisted under **models/** and the raw dataset under **data/**. The architecture follows a straightforward linear pipeline: data ingestion → model training → model serving via a Flask API → consumption by a static web page.

Key source files:
- **backend/app.py** – Flask entry point exposing the `/predict` endpoint.
- **backend/train_model.py** – Script that loads `data/Position_Salaries.csv`, preprocesses it with pandas, trains a RandomForestRegressor, and writes `models/rf_regressor.pkl`.
- **models/rf_regressor.pkl** – Serialized model used at inference time.
- **frontend/index.html** – Static UI that gathers user inputs and calls the Flask API.
- **backend/requirements.txt** – Exact Python dependencies (Flask, scikit‑learn, pandas, etc.).

## System Layers
### Data Ingestion & Pre‑processing
**Technologies:** pandas

Loads the raw CSV (`data/Position_Salaries.csv`) and applies minimal cleaning required for model consumption. Implemented in `backend/train_model.py` using pandas.

### Model Training
**Technologies:** scikit-learn, pickle

Trains a RandomForestRegressor on the cleaned dataset and serialises the model to `models/rf_regressor.pkl`. The training script also writes `models/metadata.json` for versioning.

### Prediction Service (API)
**Technologies:** Flask, pickle, scikit-learn

Flask application (`backend/app.py`) that loads the serialized model at startup, exposes a `/predict` HTTP endpoint, and handles inference requests from the UI.

### User Interface
**Technologies:** HTML, CSS, JavaScript (fetch)

Static HTML/CSS page (`frontend/index.html`) that gathers user inputs, invokes the Flask API via fetch/AJAX, and renders the predicted salary.



## Data Flow & Pipelines
1. **Raw Data Load** – `backend/train_model.py` reads `data/Position_Salaries.csv` using pandas.
2. **Pre‑processing** – Minimal cleaning (e.g., handling missing values, encoding categorical columns) is performed in the same script.
3. **Model Training** – A `RandomForestRegressor` from scikit‑learn is trained on the pre‑processed dataframe.
4. **Model Serialization** – The trained model is persisted to `models/rf_regressor.pkl` via `pickle`.
5. **API Startup** – `backend/app.py` loads the serialized model at startup and exposes a `/predict` POST endpoint.
6. **User Interaction** – `frontend/index.html` collects input fields (e.g., position, experience) and sends a JSON payload to the Flask API.
7. **Prediction** – The API deserialises the payload, applies the same preprocessing steps, invokes `model.predict()`, and returns the salary estimate as JSON.
8. **Result Display** – The frontend receives the JSON response and updates the UI with the predicted salary.

All components run within a single process space, making the flow synchronous and deterministic.

## Key Design Decisions
- API‑First approach: Even though the UI is static, all business logic (prediction) is accessed through a Flask REST endpoint, enabling future client diversification.
- Model serialization with pickle: Chosen for simplicity and direct compatibility with scikit‑learn objects; stored under `models/` alongside metadata for reproducibility.
- Monolithic layout: All backend code resides under a single `backend/` package, reducing deployment complexity for a small‑scale prototype.
- Separation of concerns via directories: `data/` for raw inputs, `models/` for artefacts, `frontend/` for presentation, `backend/` for logic, which aids maintainability.

## Scalability & Reliability
The current monolith is sufficient for low‑traffic demo usage. To handle increased load or to support multiple clients:
- **Containerisation**: Wrap the Flask service in a Docker container; orchestrate multiple replicas behind a load balancer (e.g., Nginx or Kubernetes Service).
- **Model Server**: Offload inference to a dedicated model‑serving framework (e.g., TensorFlow Serving or TorchServe) and replace the pickle‑based loading with gRPC/REST calls.
- **Asynchronous Processing**: Introduce a task queue (Celery + Redis) for heavy preprocessing or batch predictions, keeping the API response fast.
- **Data Versioning**: Store the training CSV and model artefacts in a version‑controlled data lake (e.g., DVC) to ensure reproducible builds across scaled instances.
- **Horizontal Scaling of UI**: Host static assets on a CDN to reduce latency and serve high volumes of concurrent users.

These steps preserve the existing codebase while allowing incremental scaling without a complete architectural rewrite.

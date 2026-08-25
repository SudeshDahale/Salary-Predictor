# Salary Predictor Technical Architecture Guide

## System Overview
The Salary Predictor repository implements a monolithic, API‑first application for estimating employee salaries based on job characteristics. It combines a Flask‑based backend that serves a trained scikit‑learn RandomForest regression model via a REST endpoint with a lightweight static HTML/JavaScript frontend that gathers user input and calls the prediction API. Data ingestion, model training, model serving, and presentation are organized into distinct modules, each represented by concrete source files in the repository (e.g., `backend/train_model.py`, `backend/app.py`, `frontend/index.html`). The architecture is deliberately simple to enable rapid experimentation while still providing a clear separation of concerns.

## System Layers
### Data Layer
**Technologies:** pandas, CSV

Responsible for raw data storage and preprocessing. The CSV file `data/Position_Salaries.csv` is the single source of truth. pandas is used for loading, cleaning, and preparing feature matrices.

### Model Training Layer
**Technologies:** scikit-learn, pickle, JSON

Encapsulated in `backend/train_model.py`. Implements feature engineering, train‑test split, and RandomForest regression training using scikit‑learn. Persists the model (`models/rf_regressor.pkl`) and accompanying metadata (`models/metadata.json`).

### Model Serving Layer
**Technologies:** Flask, Python

Implemented by `backend/app.py`. A Flask monolith that loads the serialized model at startup and exposes a RESTful `POST /predict` endpoint. Handles request validation, inference, and response formatting.

### Presentation Layer
**Technologies:** HTML, JavaScript, CSS

Static web assets located in `frontend/`. `index.html` provides the UI; JavaScript fetches predictions from the backend API. No server‑side rendering is performed.



## Data Flow & Pipelines
1. **Data Ingestion** – `backend/train_model.py` reads the raw CSV `data/Position_Salaries.csv` using pandas. The DataFrame is cleaned, feature‑engineered, and split into train/test sets. 2. **Model Training** – The same script builds a `RandomForestRegressor` (scikit‑learn), fits it on the training data, evaluates performance, and serializes the trained model to `models/rf_regressor.pkl` (pickle). Model metadata (feature list, training date, performance metrics) is stored in `models/metadata.json`. 3. **Model Serving** – `backend/app.py` starts a Flask application. At startup it deserializes `models/rf_regressor.pkl` and loads `metadata.json`. The API defines a `POST /predict` endpoint that accepts a JSON payload of feature values, converts it to a pandas DataFrame, runs `model.predict()`, and returns the predicted salary. 4. **Frontend Interaction** – `frontend/index.html` (with embedded JavaScript) renders a form for user input (e.g., position, experience, location). Upon submission, the script issues a `fetch` POST request to the Flask `/predict` endpoint, receives the JSON response, and displays the predicted salary to the user.

## Key Design Decisions
- API‑First approach: even though the UI is static, all business logic is accessed through a well‑defined Flask endpoint, enabling future clients (mobile, CLI) without UI changes.
- Monolithic repository layout keeps all code (data, model, API, UI) in a single git project, simplifying versioning for a prototype.
- Pickle serialization for the model: fast to load and write, suitable for a single‑process Flask server; accompanied by a human‑readable metadata JSON for transparency.
- RandomForestRegressor chosen for its robustness to non‑linear relationships and minimal feature scaling requirements, matching the tabular nature of the salary dataset.
- Dependency isolation via `backend/requirements.txt` ensures reproducible environment for both training and serving.

## Scalability & Reliability
While the current monolith works for low‑traffic demo usage, scaling can be addressed in several dimensions:
- **Horizontal API scaling**: Deploy `backend/app.py` behind a WSGI server (Gunicorn) with multiple workers and place a load balancer (NGINX) in front. The model is read‑only after load, so workers can safely share the same pickle file.
- **Model versioning**: Store models in a dedicated artifact repository (e.g., S3 or a model registry) and include a version identifier in the API path (`/v1/predict`). This decouples training from serving and enables zero‑downtime rollout.
- **Containerization**: Wrap the backend in a Docker image (Dockerfile can be derived from `backend/requirements.txt`). Containers make scaling predictable on Kubernetes or ECS.
- **Caching**: Frequently requested prediction inputs can be cached (e.g., using Redis) to reduce inference latency.
- **Separation of concerns**: For larger workloads, split the monolith into two services – a dedicated model‑inference microservice and a static‑site host for the UI. Communication remains via the same JSON API, preserving the API‑first contract.
- **Data pipeline automation**: Replace the manual `train_model.py` run with an orchestrated ETL job (Airflow, Prefect) that retrains nightly and updates the model artifact.
These steps preserve the existing codebase while providing a clear migration path toward a more distributed, production‑grade architecture.

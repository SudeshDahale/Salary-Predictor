# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first web application that predicts employee salaries based on input features. It consists of a static frontend UI, a Flask‑based backend exposing a prediction API, a model training pipeline using scikit‑learn, and persisted artifacts (model and metadata) alongside the raw training dataset. The entire stack is written in Python for the server side and vanilla HTML/CSS/JavaScript for the client side, making the solution lightweight and easy to deploy.

Key directories:
- **backend/** – Flask app (`app.py`), model training script (`train_model.py`), and Python dependencies (`requirements.txt`).
- **frontend/** – Static HTML entry point (`index.html`) and associated assets.
- **models/** – Serialized Random Forest regressor (`rf_regressor.pkl`) and model metadata (`metadata.json`).
- **data/** – Source CSV (`Position_Salaries.csv`).
- **random_forest_regression.ipynb** – Exploratory notebook used during development.

The architecture follows a clear separation of concerns while remaining a single deployable unit, aligning with the API‑first philosophy: the frontend interacts with the backend solely through HTTP endpoints.

## System Layers
### Presentation Layer (Frontend UI)
**Technologies:** HTML5, CSS3, JavaScript (vanilla), Assets in assets/ directory

Static assets (HTML, CSS, JavaScript) that render a form for salary‑prediction inputs and display results returned from the backend API.

### Application Layer (Backend API)
**Technologies:** Python 3.x, Flask, Werkzeug, scikit‑learn (runtime inference), Gunicorn (optional production WSGI server)

A Flask web application (`backend/app.py`) exposing HTTP endpoints (e.g., `/predict`). It handles request validation, loads the serialized model, performs inference, and returns JSON responses.

### Model Training Layer
**Technologies:** Python 3.x, pandas, scikit‑learn, joblib / pickle, Jupyter Notebook

Python scripts (`backend/train_model.py`) and an accompanying Jupyter notebook (`random_forest_regression.ipynb`) that read the raw CSV, preprocess features, train a `RandomForestRegressor`, evaluate performance, and serialize the artifact.

The training pipeline writes the model to `models/rf_regressor.pkl` and stores auxiliary information (feature list, training date, metrics) in `models/metadata.json`.

### Persistence Layer
**Technologies:** CSV (pandas I/O), Pickle (model serialization), JSON (metadata)

File‑system based storage for both the raw dataset (`data/Position_Salaries.csv`) and model artifacts (`models/`). No database is used; the application reads these files at startup or on‑demand.



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html`, fills in the salary‑related fields, and clicks *Submit*.
2. **HTTP Request** – JavaScript captures the form data and issues a `POST` request to the Flask endpoint `/predict` (defined in `backend/app.py`).
3. **Request Handling** – Flask validates the payload, converts it into the feature vector expected by the model, and loads the serialized Random Forest model from `models/rf_regressor.pkl` (lazy‑loaded on first request).
4. **Inference** – The model predicts a salary value; the backend packages the result (e.g., `{ "predicted_salary": 75200 }`) into a JSON response.
5. **Response Rendering** – The frontend receives the JSON, extracts the predicted salary, and updates the DOM to present the value to the user.

**Training Flow** – When `backend/train_model.py` is executed: 
- Reads `data/Position_Salaries.csv`.
- Performs preprocessing (encoding categorical columns, scaling if needed).
- Splits data, trains `RandomForestRegressor`, evaluates on a hold‑out set.
- Persists the trained model (`rf_regressor.pkl`) and writes `metadata.json` with schema, metrics, and timestamp.
- Optionally, the notebook visualizes feature importance and error distribution.

All interactions remain internal to the monolith; the only external surface is the HTTP API consumed by the UI.

## Key Design Decisions
- API‑First approach: the frontend never calls Python functions directly; it communicates exclusively via HTTP, enabling future decoupling (e.g., moving to a micro‑frontend or mobile client).
- Use of Flask for its minimal footprint and ease of exposing JSON endpoints, matching the project's educational scope.
- Model serialization with pickle (via joblib) provides quick load times and straightforward versioning; the accompanying JSON metadata ensures reproducibility.
- Static file serving for the UI keeps the deployment simple – the same Flask process can serve HTML/CSS/JS or a separate static server can be used.
- Random Forest regressor selected for its robustness to feature scaling and ability to handle mixed numeric/categorical data without extensive preprocessing.

## Scalability & Reliability
The current monolith is suitable for low‑to‑moderate traffic (e.g., demo or prototype). To scale horizontally:

1. **Containerization** – Package the application into a Docker image; each replica runs the same Flask process, reading the shared model artifact from a mounted volume or a read‑only object store (e.g., S3).
2. **Load Balancing** – Place a reverse proxy (NGINX, HAProxy, or cloud LB) in front of multiple Flask instances to distribute incoming `/predict` requests.
3. **Model Serving Separation** – Offload inference to a dedicated model‑serving layer (TensorFlow Serving, TorchServe, or a simple FastAPI service). The Flask API would become a thin orchestrator, reducing latency and allowing independent scaling of compute‑intensive inference.
4. **Caching** – For repeated predictions with identical inputs, introduce an in‑memory cache (Redis or Flask‑caching) to avoid redundant model evaluation.
5. **Asynchronous Processing** – If future extensions add heavier preprocessing or batch predictions, move to a task queue (Celery + RabbitMQ/Redis) to free the request thread.
6. **Statelessness** – Ensure the Flask app does not rely on mutable in‑process state (e.g., re‑load the model on each request or use a thread‑safe singleton). This guarantees that any replica can serve any request.

Even without these enhancements, the architecture is cleanly layered, making incremental scaling steps straightforward.

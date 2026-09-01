# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first application that predicts salary ranges for job positions using a trained Random Forest regression model. The system is composed of a lightweight Flask backend that serves prediction and model‑training endpoints, a static HTML frontend that collects user inputs and displays results, and supporting data and model artifacts stored in CSV and Pickle formats. All components are packaged together in a single repository, enabling straightforward deployment and local experimentation.

## System Layers
### Presentation Layer
**Technologies:** HTML5, CSS, Vanilla JavaScript (fetch API)

Static HTML page (`frontend/index.html`) that gathers input from users and displays prediction results. No JavaScript frameworks are used; the page performs simple form submission to the backend API.

### API Layer
**Technologies:** Python 3.x, Flask, Werkzeug, pickle

Flask application (`backend/app.py`) exposing RESTful endpoints `/predict` for inference and `/train` for model retraining. Handles request validation, model loading, and JSON serialization.

### Model & Data Layer
**Technologies:** pandas, scikit‑learn (RandomForestRegressor), pickle, JSON

Contains the persisted machine‑learning artifact (`models/rf_regressor.pkl`) and its accompanying `metadata.json`. Training data lives in `data/Position_Salaries.csv`. The training script (`backend/train_model.py`) reads the CSV, preprocesses it, fits a scikit‑learn Random Forest, and writes the artifacts.

### Infrastructure Layer
**Technologies:** Python virtual environment, pip, VSCode settings

All components are packaged as a single monolithic repository. Dependencies are listed in `backend/requirements.txt`. The project can be run locally with `python -m flask run` or containerised using a Dockerfile (not present but straightforward to add).



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html` in a browser and enters job‑related fields (e.g., position title, years of experience). The page submits a POST request to the Flask endpoint `/predict` defined in `backend/app.py`.
2. **Request Handling** – Flask parses the incoming JSON payload, loads the serialized Random Forest model from `models/rf_regressor.pkl` (using `pickle`), and applies the model to the received features.
3. **Prediction Response** – The backend returns a JSON response containing the predicted salary, which the frontend renders on the page.
4. **Model Retraining (optional)** – An authorized request to `/train` triggers `backend/train_model.py`. This script reads the historical dataset `data/Position_Salaries.csv`, performs preprocessing, fits a `RandomForestRegressor` (from scikit‑learn), and serializes the new model to `models/rf_regressor.pkl`. Metadata such as training date, feature importance, and model parameters are written to `models/metadata.json`.
5. **Static Assets** – Images under `assets/` are served directly by the web server or bundled with the HTML for branding and documentation.

All data movement stays within the monolith: the frontend talks only to the Flask API, and the backend accesses the CSV and Pickle files on the same filesystem.

## Key Design Decisions
- API‑First approach: even though the UI is a simple static page, all business logic is accessed through HTTP endpoints, making future UI replacements (React, mobile) trivial.
- Monolithic layout: keeping frontend, backend, data, and model files in one repo reduces operational overhead for a small‑scale demo and simplifies version control.
- Pickle for model persistence: chosen for its simplicity and direct compatibility with scikit‑learn objects; acceptable because the service runs in a trusted environment.
- CSV as source data: human‑readable format enables easy updates to the training set without code changes.
- Separate training script (`train_model.py`): isolates heavy computation from request handling, allowing training to be scheduled or triggered manually without affecting the prediction service.

## Scalability & Reliability
While the current monolith suffices for low‑traffic usage and local experimentation, scaling can be achieved by:
- **Containerisation**: Dockerising the Flask app and serving static assets via a lightweight web server (nginx) to separate concerns.
- **Horizontal scaling**: Deploy multiple Flask instances behind a load balancer; the model file can be stored in a shared volume or object store (e.g., S3) to avoid duplication.
- **Model versioning**: Replace the single Pickle file with a model registry (MLflow, DVC) to support A/B testing and rollback.
- **Asynchronous training**: Move the training step to a background job queue (Celery + Redis) so that `/train` does not block the API.
- **Data store migration**: For larger datasets, shift from CSV to a relational database (PostgreSQL) or data lake, enabling incremental updates and faster feature engineering.
These steps preserve the existing API contract while allowing the system to handle higher request volumes and larger model assets.

# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first system for predicting job salaries based on input features such as job position and experience. The system consists of a Flask backend that serves a REST prediction endpoint and a static frontend UI for user interaction. Model training is performed offline via a Python script, producing a pickled scikit‑learn RandomForestRegressor stored under the models directory. Historical salary data resides in a CSV file and is used both for training and optional reference during inference.

Key components include:
- **frontend/index.html** (HTML/CSS/JS) – static UI.
- **backend/app.py** – Flask application exposing `/predict` endpoint.
- **backend/train_model.py** – script that reads `data/Position_Salaries.csv`, trains a RandomForestRegressor, and serialises it to `models/rf_regressor.pkl`.
- **models/rf_regressor.pkl** – serialized model used at runtime.
- **models/metadata.json** – model metadata (e.g., training date, feature list).
- **data/Position_Salaries.csv** – source dataset.

The architecture is deliberately simple to enable rapid prototyping while maintaining a clear separation between UI, API, and model artifacts.



## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static web UI built with HTML, CSS, and JavaScript that collects user inputs and displays predictions. Files: `frontend/index.html` and associated assets.

### API Layer
**Technologies:** Python, Flask

Flask application exposing a RESTful `/predict` endpoint. Handles request parsing, validation, model loading, and response formatting. Core file: `backend/app.py`.

### Model Layer
**Technologies:** scikit-learn, Pickle

Encapsulates the trained scikit‑learn RandomForestRegressor. The model artifact (`models/rf_regressor.pkl`) is loaded lazily by the API. Model metadata lives in `models/metadata.json`.

### Data Layer
**Technologies:** CSV

Source CSV dataset (`data/Position_Salaries.csv`) used for offline training and optional reference during inference. No runtime database is required; the dataset is read only during training.

### Training Layer
**Technologies:** Python, scikit-learn, pandas

Standalone script (`backend/train_model.py`) that implements the data preprocessing, model training, evaluation, and serialization steps. Executed manually or via CI/CD to update the model.



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html` in a browser, enters job details (e.g., position, years of experience) and clicks *Predict*.
2. **Client Request** – JavaScript code captures the form data and sends a JSON POST request to the Flask endpoint defined in `backend/app.py` (`/predict`).
3. **API Layer** – `app.py` parses the request, validates inputs, and loads the serialized model (`models/rf_regressor.pkl`) if not already in memory.
4. **Inference** – The model receives the feature vector, performs prediction using scikit‑learn's `RandomForestRegressor.predict`, and returns a salary estimate.
5. **Response** – `app.py` wraps the prediction in a JSON response and sends it back to the browser.
6. **Presentation** – The frontend JavaScript receives the JSON payload, extracts the salary value, and updates the UI to display the predicted salary.

**Training Pipeline** (offline):
- `backend/train_model.py` reads `data/Position_Salaries.csv`, performs preprocessing (encoding categorical columns, scaling if needed), splits data, trains a `RandomForestRegressor`, evaluates performance, writes the model to `models/rf_regressor.pkl`, and records metadata to `models/metadata.json`.


## Key Design Decisions
- Monolithic layout keeps deployment simple – a single Flask process serves both static assets (if configured) and the prediction API.
- API‑first approach ensures the prediction logic is decoupled from the UI, allowing future clients (mobile, CLI) to reuse the endpoint without UI changes.
- Pickle is used for model serialization for speed and ease of integration with scikit‑learn; the repository stores the artifact under `models/` and loads it at runtime.
- RandomForestRegressor was chosen for its robustness to non‑linear relationships and minimal feature scaling requirements, reducing preprocessing complexity.
- No external database is introduced; the CSV dataset suffices for training, keeping the stack lightweight.

## Scalability & Reliability
Because the current design runs as a single Flask process, scalability is limited to vertical scaling (more CPU/RAM) or simple process replication behind a reverse proxy (e.g., gunicorn + Nginx). To handle higher request volumes:
- Deploy the Flask app with a production WSGI server (gunicorn) and configure multiple worker processes.
- Cache the loaded model in memory to avoid repeated disk I/O.
- Separate static assets onto a CDN or serve them directly from a web server, reducing load on the Flask process.
- If future feature expansion requires model versioning or A/B testing, consider extracting the Model Layer into a dedicated microservice exposing gRPC/REST, allowing independent scaling.


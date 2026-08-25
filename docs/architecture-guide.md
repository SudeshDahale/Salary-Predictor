# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first application for predicting employee salaries based on role, location, and experience. The system consists of a static HTML front‑end that gathers user input, a Flask back‑end that provides HTTP endpoints for model training and inference, a model store for persisting trained artefacts, and a dataset folder containing the raw CSV used for training. All components are packaged in a single repository and communicate via HTTP calls, enabling rapid prototyping while keeping deployment simple.

## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, Vanilla JavaScript

Static assets served to the browser – HTML, CSS, and JavaScript. The UI collects input parameters (e.g., job title, location, experience) and displays the predicted salary returned from the back‑end.

### API Layer
**Technologies:** Python 3, Flask, Flask‑RESTful (if used), Werkzeug

Python Flask application exposing HTTP endpoints for model inference (`/predict`) and training (`/train`). All business logic is accessed through these REST‑style APIs, making the system API‑first.

### Business Logic & ML Layer
**Technologies:** scikit‑learn, pandas, numpy, pickle

Code that loads the persisted model, runs predictions, and orchestrates model training. The training script **backend/train_model.py** reads raw data, performs preprocessing, fits a RandomForestRegressor, and writes artefacts to the model store.

### Data & Model Store Layer
**Technologies:** CSV files, Pickle, JSON

Filesystem‑based storage for raw datasets and trained artefacts. The CSV file **data/Position_Salaries.csv** is the source of truth for training. Model artefacts (**models/rf_regressor.pkl**, **models/metadata.json**) are version‑controlled alongside code.



## Data Flow & Pipelines
1. The user opens **frontend/index.html**, fills the salary query form and submits it. 2. The form triggers a POST request to the Flask service defined in **backend/app.py** (e.g., `/predict`). 3. The back‑end loads the serialized model **models/rf_regressor.pkl** and its **models/metadata.json**, runs the prediction, and returns a JSON response to the front‑end, which updates the UI. 4. For model retraining, an authorized client can call the `/train` endpoint (implemented in **backend/train_model.py**). The training script reads **data/Position_Salaries.csv**, fits a RandomForestRegressor, serialises the new model to **models/rf_regressor.pkl**, and updates **models/metadata.json**. 5. The persisted artefacts are versioned in the repository, allowing the prediction endpoint to always use the latest trained model.

## Key Design Decisions
- Monolithic repository – all code, data, and model artefacts reside in a single repo, simplifying local development and CI pipelines.
- API‑first approach – even the simple HTML UI talks to Flask over HTTP, enabling future replacement of the front‑end (e.g., React) without touching business logic.
- Pickle for model serialization – fast read/write for scikit‑learn models, but requires careful version control and trusted execution environment.
- Static file serving – the Flask app can optionally serve the HTML UI, eliminating the need for a separate web server in development.

## Scalability & Reliability
Because the current architecture is monolithic, scaling out involves replicating the Flask service behind a load balancer and sharing the model store via a network file system or object storage (e.g., S3). For higher throughput, the prediction endpoint can be decoupled into a lightweight inference service (e.g., FastAPI) and the training workflow can be off‑loaded to a batch job or orchestrator (Airflow, Prefect). Model versioning can be enhanced by storing artefacts in a dedicated model registry (MLflow) rather than the repository filesystem.

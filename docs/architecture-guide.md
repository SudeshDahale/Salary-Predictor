# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first application that predicts employee salaries based on job details. The system consists of a static front‑end UI (HTML/CSS/JavaScript) that captures user input, a Flask‑based back‑end that exposes a prediction REST endpoint, a trained scikit‑learn Random Forest model stored as a pickle, and CSV data used for model training. All components reside in a single codebase and are version‑controlled together, making deployment straightforward while still preserving a clear separation of concerns between presentation, API, and model layers.

## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static web assets that collect job parameters and render predictions. Built with plain HTML, CSS, and vanilla JavaScript; no build step required.

### API Layer
**Technologies:** Python, Flask

Flask application exposing REST endpoints (e.g., `/predict`). Handles request validation, model invocation, and response formatting. Runs in a single Python process but can be served with a production WSGI server (gunicorn/uwsgi).

### Model Layer
**Technologies:** scikit-learn, pickle, JSON

Encapsulates the trained Random Forest regressor. Model artifact is a pickle file loaded with scikit‑learn. Metadata (feature order, model version) lives in JSON alongside the pickle.

### Data Layer
**Technologies:** CSV, pandas

Source CSV containing historical salary data used for training. Stored under *data/Position_Salaries.csv* and read by the training script.



## Data Flow & Pipelines
1. **User Interaction** – The user opens *frontend/index.html* and fills the job‑detail form. 2. **Request** – JavaScript sends an HTTP POST (e.g., `/predict`) to the Flask service defined in *backend/app.py*. 3. **API Layer** – The Flask route parses the JSON payload, validates required fields, and forwards the feature vector to the Model Service. 4. **Model Service** – The back‑end lazily loads the serialized Random Forest model from *models/rf_regressor.pkl* (or reuses an in‑memory instance). Using scikit‑learn, it computes the salary prediction. 5. **Response** – The predicted salary (and optional metadata from *models/metadata.json*) is returned as JSON. 6. **Presentation** – The front‑end JavaScript receives the response, formats it, and updates the UI to display the predicted salary to the user.

The training pipeline (offline) is separate: *backend/train_model.py* reads *data/Position_Salaries.csv*, trains a `RandomForestRegressor`, persists the model and metadata, and can be re‑executed to refresh the model.

**Key Files**:
- *frontend/index.html* – static UI.
- *backend/app.py* – Flask API server.
- *backend/train_model.py* – Model training script.
- *models/rf_regressor.pkl* – Serialized model.
- *models/metadata.json* – Model version / feature schema.
- *data/Position_Salaries.csv* – Training data.
- *backend/requirements.txt* – Python dependencies (Flask, scikit‑learn, pandas, etc.).

## Key Design Decisions
- API‑First monolith: the front‑end never directly accesses the model; all predictions flow through a defined Flask API, enabling future decoupling into micro‑services if needed.
- Model serialization via pickle: quick to load and compatible with scikit‑learn, but ties the model to the Python runtime version; metadata JSON mitigates version drift.
- Static front‑end: eliminates the need for a separate Node.js build pipeline, keeping the stack lightweight.
- Separate training script (*backend/train_model.py*) from the serving code to keep production dependencies minimal and avoid accidental retraining at runtime.

## Scalability & Reliability
Although the current deployment is a single‑process Flask app, the architecture supports horizontal scaling:
- **Stateless API**: Each request is independent; multiple Flask instances can run behind a load balancer (NGINX, AWS ELB) without shared state.
- **Model Caching**: Load the Random Forest once at process start and reuse it across requests; when scaling, each worker process will have its own in‑memory copy (acceptable for the modest model size).
- **Production WSGI Server**: Use gunicorn with multiple workers (`--workers N`) to leverage multi‑core CPUs.
- **Containerization**: Dockerizing the app (Dockerfile not present but easy to add) isolates dependencies and simplifies scaling on orchestration platforms (Kubernetes, ECS).
- **Future Decoupling**: If request volume grows, the Model Layer can be extracted into a dedicated prediction micro‑service (e.g., FastAPI or TensorFlow Serving) while the API Layer becomes a thin gateway.
- **Data Store Migration**: For larger training datasets, move *data/Position_Salaries.csv* to a managed data lake (S3, GCS) and update the training script accordingly.
- **Model Versioning**: Store multiple model artifacts (e.g., `rf_regressor_v1.pkl`, `rf_regressor_v2.pkl`) and reference the desired version via metadata; a CI/CD pipeline can automate promotion of new models without downtime.

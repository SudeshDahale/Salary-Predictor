# Salary-Predictor Technical Architecture Guide

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first machine‑learning service that predicts software‑engineer salaries based on input features. The system consists of four logical layers—Data Ingestion, Model Training, Model Serving, and Presentation—implemented with Python, Flask, scikit‑learn, pandas, HTML and JavaScript. A Random Forest regressor is trained on the CSV dataset located under `data/`, persisted as a pickle, and served via a REST endpoint consumed by a static web UI.

## System Layers
### Data Ingestion Layer
**Technologies:** pandas

Responsible for loading raw salary data from `data/Position_Salaries.csv` into pandas DataFrames. Handles basic validation (missing values, type coercion) before handing the data to the training pipeline.

### Model Training Layer
**Technologies:** scikit-learn, pandas, pickle, json

Encapsulated in `backend/train_model.py`. Transforms the ingested DataFrame, splits it into train/test sets, fits a scikit‑learn `RandomForestRegressor`, evaluates performance, and persists the trained model (`models/rf_regressor.pkl`) together with a JSON metadata file (`models/metadata.json`).

### Model Serving Layer
**Technologies:** Python, Flask, pickle, JSON

Implemented by the Flask application in `backend/app.py`. At startup it deserialises the model pickle and metadata, registers the `/predict` REST endpoint, and processes incoming JSON payloads to return salary predictions.

### Presentation Layer
**Technologies:** HTML, JavaScript, CSS

Static web UI located under `frontend/`. `index.html` contains a form and vanilla JavaScript that calls the `/predict` API via the Fetch API, then renders the prediction on the page.



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html`, enters job attributes (e.g., title, location, years of experience) and clicks *Predict*.
2. **Request Dispatch** – JavaScript in the page serialises the input as JSON and sends an HTTP POST to the Flask endpoint `/predict` defined in `backend/app.py`.
3. **Model Inference** – On application start, `app.py` loads `models/rf_regressor.pkl` (the trained RandomForestRegressor) and `models/metadata.json`. The request payload is transformed into a pandas `DataFrame`, passed to `model.predict()`, and the resulting salary value is packaged into a JSON response.
4. **Response Rendering** – The frontend receives the JSON, extracts the predicted salary, and updates the DOM to display the result to the user.
5. **Training Loop (offline)** – `backend/train_model.py` reads `data/Position_Salaries.csv` with pandas, performs feature engineering, fits a `RandomForestRegressor`, writes the model pickle to `models/rf_regressor.pkl` and stores training metadata (e.g., feature list, model version) in `models/metadata.json`. This script is executed manually or via CI/CD to refresh the model.

All data movement stays within the repository; no external storage or message brokers are used.

## Key Design Decisions
- API‑First Design – Even though the UI is static, the Flask service exposes a clean JSON‑based `/predict` endpoint, allowing future clients (mobile apps, other services) to reuse the model without UI changes.
- Monolithic Repository – All source, data, model artifacts, and UI assets reside in a single git repository, simplifying versioning and deployment for a small‑scale project.
- Model Persistence with Pickle – Chosen for its simplicity and direct compatibility with scikit‑learn objects. The model is versioned via the accompanying `metadata.json` file.
- Separation of Concerns via Directory Structure – `backend/` holds all Python code, `frontend/` contains static assets, `data/` stores raw CSV, and `models/` stores artefacts. This layout eases navigation and potential containerisation.
- Minimal Dependency Set – `backend/requirements.txt` pins only Flask, pandas, scikit‑learn, and their transitive dependencies, keeping the container image small.

## Scalability & Reliability
The current monolith runs a single Flask process that loads the model into memory. To scale horizontally:
- **Containerisation**: Package the `backend/` folder into a Docker image. Deploy multiple replicas behind a load balancer (e.g., Nginx, AWS ELB).
- **WSGI Workers**: Use gunicorn with multiple worker processes to utilise multi‑core CPUs, each sharing the same model file on disk.
- **Model Caching**: Since the model is read‑only after start‑up, it can be memory‑mapped or loaded once per worker, avoiding repeated I/O.
- **Async I/O**: For very high request rates, migrate to an async framework (e.g., FastAPI + uvicorn) while keeping the same scikit‑learn model.
- **Model Server**: For future extensions (e.g., TensorFlow, ONNX), replace the Flask inference layer with a specialised model‑serving solution (TensorFlow Serving, TorchServe) without touching the UI.
- **Data Pipeline Scaling**: If the CSV grows, consider moving ingestion to a data lake (S3) and using Spark or Dask for preprocessing, but the core API contract would remain unchanged.
Overall, the architecture supports incremental scaling by containerising the Flask service and adding more workers, while the clear API boundary ensures downstream clients are unaffected.

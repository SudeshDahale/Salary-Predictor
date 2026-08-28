# Technical Architecture Guide for Salary-Predictor

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first system that predicts salaries based on job position features. It combines a Flask‑based backend service that loads a pre‑trained scikit‑learn RandomForestRegressor model with a static HTML/JavaScript frontend that gathers user input and invokes the prediction endpoint. All artefacts (training data, model pickle, and metadata) reside in the repository, enabling end‑to‑end reproducibility.

Key repository artifacts:
- **backend/app.py** – Flask application exposing the `/predict` API.
- **backend/train_model.py** – Script that trains the RandomForestRegressor using **data/Position_Salaries.csv** and persists the model to **models/rf_regressor.pkl** with accompanying **models/metadata.json**.
- **frontend/index.html** – Static UI (HTML/CSS/JS) that posts user‑provided features to the Flask API.
- **models/rf_regressor.pkl** – Serialized model artefact used at inference time.
- **data/Position_Salaries.csv** – Source dataset for model training.
- **random_forest_regression.ipynb** – Exploratory notebook (reference only).

The architecture is deliberately simple: a single Flask process serves both API requests and static assets, making it easy to run locally with the `requirements.txt` in **backend/**.


## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static web assets that render the UI and handle user interactions. Implemented with HTML, CSS, and vanilla JavaScript. The main entry point is **frontend/index.html** which collects feature values (e.g., years of experience, location, role) and issues an AJAX POST to the backend prediction endpoint.

### API Layer
**Technologies:** Python, Flask

A Flask application defined in **backend/app.py** that exposes a RESTful `/predict` endpoint. The API receives a JSON payload, validates required fields, loads the pre‑trained model, runs inference, and returns the predicted salary as JSON.

### Model Layer
**Technologies:** scikit-learn, pickle

Encapsulates the machine‑learning artefacts. The RandomForestRegressor model is serialized with `pickle` into **models/rf_regressor.pkl**. Model metadata (feature ordering, preprocessing steps, version) lives in **models/metadata.json**. The API loads this artefact once at startup (or lazily on first request) to avoid repeated I/O.

### Data Layer
**Technologies:** pandas, CSV

Holds the raw training dataset **data/Position_Salaries.csv** and the notebook **random_forest_regression.ipynb** used for exploratory analysis. The training script **backend/train_model.py** reads the CSV, performs any preprocessing, fits the RandomForestRegressor, and persists the model and metadata.



## Data Flow & Pipelines
1. **User Interaction** – The browser loads **frontend/index.html** and the user fills the salary‑prediction form.
2. **Request Submission** – JavaScript serialises the form data into JSON and sends an HTTP POST to `http://<host>:<port>/predict`.
3. **API Handling** – Flask route in **backend/app.py** parses the JSON, validates required fields, and forwards the feature vector to the Model Layer.
4. **Model Inference** – The loaded `RandomForestRegressor` (from **models/rf_regressor.pkl**) predicts the salary using the supplied features.
5. **Response** – Flask returns a JSON payload `{ "predicted_salary": <value> }`.
6. **UI Update** – The frontend JavaScript receives the response and displays the predicted salary to the user.

Training flow (offline, not part of the runtime service):
- **backend/train_model.py** reads **data/Position_Salaries.csv**, fits the model, writes **models/rf_regressor.pkl** and **models/metadata.json**.
- The notebook **random_forest_regression.ipynb** documents exploratory steps and hyper‑parameter tuning.


## Key Design Decisions
- API‑First Monolith: The Flask server both serves static UI files (via `send_from_directory`) and provides the `/predict` endpoint, reducing deployment complexity.
- Model Serialization with Pickle: Chosen for simplicity and direct compatibility with scikit‑learn objects. Model artefacts are version‑controlled in the **models/** directory.
- Separate Training Script: `backend/train_model.py` isolates the heavy training workload from the inference service, allowing retraining without touching the production API.
- Metadata JSON: Stores feature order and preprocessing flags, ensuring the API can validate incoming payloads against the model's expectations.
- Minimal Dependency Footprint: `backend/requirements.txt` lists only Flask, scikit‑learn, pandas, and related libraries, facilitating lightweight Docker images.

## Scalability & Reliability
While the current monolith is sufficient for development and low‑traffic demo usage, the following patterns enable scaling:

* **Horizontal Scaling** – Deploy multiple Flask instances behind a load balancer (e.g., Nginx or cloud LB). Use a production WSGI server such as Gunicorn (`gunicorn -w 4 backend.app:app`) to increase concurrency.
* **Model Loading Strategy** – Load the model once at process start to avoid per‑request I/O. For massive models, consider memory‑mapped loading or a separate model‑serving microservice (e.g., TensorFlow Serving or a FastAPI wrapper) to isolate inference latency.
* **Static Asset CDN** – Offload **frontend/** assets to a CDN to reduce bandwidth on the Flask host.
* **Containerization** – Build a Docker image (`Dockerfile` can be derived from **backend/requirements.txt**) to enable rapid scaling via Kubernetes or serverless platforms.
* **Asynchronous Request Handling** – If prediction latency grows, migrate the Flask endpoint to an async framework (FastAPI or Quart) or queue predictions via a task broker (Celery + Redis) for background processing.

These steps preserve the existing API contract while allowing the system to handle higher request volumes and larger model artefacts without major refactoring.

# Technical Architecture Guide for Salary-Predictor

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first web application that predicts employee salaries based on job attributes. A lightweight Flask server hosts a REST endpoint for inference, while a static HTML/JS frontend provides a user‑friendly form. Model training is performed offline via a Python script that consumes a CSV dataset, trains a scikit‑learn RandomForestRegressor, and persists the model and its metadata under the `models/` directory. The entire stack (Python, Flask, scikit‑learn, HTML/CSS/JS) runs as a single process, making the solution simple to deploy and extend.

Key directories:
- `backend/`: Flask app (`app.py`), dependency list (`requirements.txt`), and model training script (`train_model.py`).
- `frontend/`: UI (`index.html`) and associated static assets.
- `models/`: Serialized model (`rf_regressor.pkl`) and JSON metadata (`metadata.json`).
- `data/`: Raw training data (`Position_Salaries.csv`).
- `random_forest_regression.ipynb`: Exploratory notebook used during model development.

The guide describes the logical layers, component interactions, data pipelines, design decisions, and scalability considerations for this codebase.

## System Layers
### Presentation Layer
**Technologies:** HTML, CSS, JavaScript

Static web UI built with HTML, CSS, and JavaScript. The file `frontend/index.html` renders a form where users input job title, location, experience, etc. The UI posts a JSON payload to the Flask prediction endpoint using the Fetch API and displays the returned salary prediction.

### API Layer
**Technologies:** Python, Flask

Python Flask application (`backend/app.py`). Exposes a RESTful `/predict` endpoint that accepts a POST request with the user input, loads the trained model from `models/rf_regressor.pkl`, performs inference, and returns a JSON response. Flask also serves the static UI files when the app is run in production mode.

### Model & Inference Layer
**Technologies:** scikit-learn, pickle

Encapsulates the trained RandomForestRegressor model (`models/rf_regressor.pkl`) and its accompanying `models/metadata.json`. The model is loaded lazily on the first request and cached in memory for subsequent predictions to reduce I/O overhead.

### Training & Data Layer
**Technologies:** Python, pandas, scikit-learn, pickle

Offline training script (`backend/train_model.py`) reads the CSV dataset `data/Position_Salaries.csv`, performs any necessary preprocessing, trains a RandomForestRegressor, evaluates basic metrics, and persists the model and metadata. The Jupyter notebook `random_forest_regression.ipynb` documents exploratory data analysis and hyper‑parameter tuning performed during development.



## Data Flow & Pipelines
1. **User Interaction** – A user opens `frontend/index.html` in a browser and fills out the salary prediction form.
2. **Request Submission** – JavaScript captures the form data and issues a `POST /predict` request (JSON body) to the Flask server (`backend/app.py`).
3. **API Handling** – Flask validates the payload, deserializes the stored RandomForest model (`models/rf_regressor.pkl`), and calls `model.predict()` with the processed feature vector.
4. **Inference** – The model returns a numeric salary estimate.
5. **Response** – Flask wraps the estimate in a JSON response (`{ "predicted_salary": <value> }`) and sends it back to the client.
6. **Result Presentation** – The frontend JavaScript receives the response and updates the DOM to display the predicted salary to the user.

**Training Pipeline** (offline, not part of the request flow):
- `backend/train_model.py` reads `data/Position_Salaries.csv` → preprocess → split → train RandomForest → compute simple metrics → serialize model to `models/rf_regressor.pkl` and write `models/metadata.json`.
- The notebook `random_forest_regression.ipynb` provides exploratory analysis that informed feature engineering and hyper‑parameter choices.

## Key Design Decisions
- API‑First Monolith: The Flask server is the single entry point for both UI assets and the prediction API, simplifying deployment and eliminating the need for inter‑service networking.
- Model Serialization with Pickle: Using `pickle` to store the scikit‑learn model provides a quick, language‑native way to persist and load the model without external model servers.
- Separate Training Script: Keeping training logic in `backend/train_model.py` isolates long‑running compute from the request‑handling process, allowing model updates without impacting API uptime.
- Static UI Served by Flask: By configuring Flask's static folder to point at `frontend/`, the same process delivers HTML/CSS/JS, reducing infrastructure complexity.
- Minimal Dependency Set: `backend/requirements.txt` pins only Flask and scikit‑learn (plus pandas), keeping the container image small and the build pipeline fast.

## Scalability & Reliability
Although designed as a simple monolith, the architecture can be scaled horizontally or vertically:
- **Horizontal Scaling** – Deploy multiple Flask instances behind a load balancer (e.g., Nginx or HAProxy). Because the model is loaded into memory on each instance, ensure the model file is available on all nodes (shared volume or container image).
- **Model Caching** – Load the model once at application start and keep it in a global variable to avoid repeated disk I/O.
- **Asynchronous Inference** – For higher request rates, replace the synchronous endpoint with a background task queue (Celery + Redis) that processes predictions asynchronously.
- **Containerization** – Package the app in a Docker image; the image includes the model, allowing rapid scaling via Kubernetes deployments.
- **Resource Isolation** – RandomForest inference is CPU‑bound; allocate appropriate CPU limits per container or consider moving inference to a dedicated inference service (e.g., TensorFlow Serving) if latency becomes a concern.
- **Data Versioning** – Store training datasets and model artifacts in a version‑controlled artifact repository (e.g., DVC) to support reproducible builds across scaled environments.

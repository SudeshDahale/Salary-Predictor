# Technical Architecture Guide – Salary-Predictor

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first web application that predicts salary ranges for software positions. The backend is a Flask service that exposes a single prediction endpoint. It loads a pre‑trained Random Forest model (persisted as `models/rf_regressor.pkl`) and uses pandas for request parsing and response formatting. Model training is performed offline by `backend/train_model.py` using scikit‑learn and the CSV data in `data/Position_Salaries.csv`. A static HTML/JavaScript frontend (`frontend/index.html`) collects job attributes, calls the prediction API, and displays the result. All components live in a single repository and are packaged together for simple deployment.

## System Layers
### Presentation Layer
**Technologies:** HTML, JavaScript, CSS

Static web assets (HTML, CSS, JavaScript) served directly from the Flask static route or a simple web server. Handles user input and displays predictions.

### API Layer
**Technologies:** Python, Flask

Flask application (`backend/app.py`) exposing HTTP endpoints. Routes request payloads to the service layer and returns JSON responses.

### Service & Model Layer
**Technologies:** Python, scikit-learn, pandas

Loads the persisted Random Forest regressor (`models/rf_regressor.pkl`) at startup. Performs data validation, feature engineering (if any), and invokes the model for inference.

### Training & Data Layer
**Technologies:** Python, pandas, scikit-learn, Jupyter Notebook (`random_forest_regression.ipynb`)

Offline script (`backend/train_model.py`) reads raw salary data (`data/Position_Salaries.csv`), trains a Random Forest regressor, serializes the model to `models/rf_regressor.pkl`, and writes metadata (`models/metadata.json`).



## Data Flow & Pipelines
1. **User Interaction** – The user opens `frontend/index.html` in a browser and fills the job‑attribute form. 2. **API Call** – JavaScript sends an HTTP POST request to `/predict` (implemented in `backend/app.py`). 3. **Request Handling** – Flask parses the JSON payload, converts it into a pandas DataFrame, and forwards the data to the loaded Random Forest model. 4. **Prediction** – The model (`rf_regressor.pkl`) computes a salary estimate, which Flask returns as JSON. 5. **Result Rendering** – The frontend receives the JSON response and updates the UI with the predicted salary.

## Key Design Decisions
- Monolithic repository – all code (backend, frontend, model artifacts) lives in a single Git repo, simplifying versioning and deployment.
- API‑First approach – the Flask app exposes a single `/predict` endpoint, allowing the same API to be consumed by the HTML frontend or any future client.
- Model persistence with `pickle` – the trained Random Forest model is serialized to `models/rf_regressor.pkl` for fast loading at runtime.
- Separation of training and inference – `train_model.py` is an explicit script, keeping the inference service lightweight.
- Minimal external dependencies – only Flask, pandas, scikit-learn, and their transitive packages are listed in `backend/requirements.txt`.

## Scalability & Reliability
The current monolith is sufficient for low‑to‑moderate traffic (e.g., prototype or internal use). To scale:
- **Horizontal scaling**: Containerize the Flask app (Docker) and run multiple instances behind a load balancer. Because the model is loaded in memory, each replica can serve predictions independently.
- **Model serving separation**: Extract the inference logic into a dedicated model‑serving microservice (e.g., TensorFlow Serving, TorchServe, or a FastAPI wrapper) to reduce latency and enable zero‑downtime model updates.
- **Caching**: Introduce an in‑memory cache (Redis) for repeated identical requests.
- **Asynchronous processing**: For batch predictions, add a task queue (Celery) and worker processes.
- **Data pipeline**: Automate periodic retraining by scheduling `train_model.py` via cron or CI/CD, then replace `rf_regressor.pkl` without downtime.

# Salary Predictor – Technical Architecture Guide

## System Overview
The Salary Predictor repository implements a monolithic, API‑first machine‑learning service that predicts employee salaries based on position data. A Random Forest regressor is trained offline, serialized with pickle, and served via a Flask REST endpoint. A lightweight HTML frontend posts user features to the API and renders the predicted salary.

## System Layers
### Data Layer
**Technologies:** CSV, Pickle

Raw CSV dataset stored under data/Position_Salaries.csv and the serialized model artifacts under models/. The CSV is read during training; the .pkl and metadata.json are loaded at runtime for inference.

### Model Training Layer
**Technologies:** Python, scikit-learn, pandas

Standalone Python script backend/train_model.py that reads the CSV, encodes categorical features, splits data, trains a scikit‑learn RandomForestRegressor, evaluates basic metrics, and writes the trained model to models/rf_regressor.pkl along with models/metadata.json.

### Prediction Service Layer
**Technologies:** Flask, Python

Flask application backend/app.py that loads the pickled model at startup, defines a /predict POST endpoint expecting JSON payload with the same feature schema used during training, runs model.predict, and returns the salary as JSON.

### Presentation Layer
**Technologies:** HTML, JavaScript, CSS

Static HTML page frontend/index.html that collects user input via a form, sends an asynchronous fetch request to the /predict endpoint, and displays the returned salary value to the user.



## Data Flow & Pipelines
User opens frontend/index.html → fills form → browser sends JSON payload to Flask /predict endpoint → app loads rf_regressor.pkl (if not already in memory) → model computes salary → Flask returns JSON response → browser updates UI with predicted salary. Offline, backend/train_model.py reads data/Position_Salaries.csv → preprocesses → trains RandomForestRegressor → serializes model to models/rf_regressor.pkl and writes models/metadata.json.

## Key Design Decisions
- Keep the ML pipeline separate from the serving API to simplify retraining and versioning.
- Use pickle for model persistence to avoid heavy serialization frameworks.
- Expose a single POST /predict endpoint (API‑first) to decouple frontend from backend implementation.
- Store static assets in a dedicated frontend folder, enabling easy replacement with a SPA framework if needed.

## Scalability & Reliability
The monolithic design is sufficient for low‑traffic demo use. For higher load, the Flask service can be containerised and scaled horizontally behind a load balancer; the model can be loaded once per worker to reduce memory overhead. Switching to a model server such as TorchServe or using a lightweight serialization format (joblib) would improve cold‑start time. Adding a message queue (e.g., RabbitMQ) would enable asynchronous batch predictions.

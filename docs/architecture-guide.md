# Technical Architecture Guide for Salary-Predictor

## System Overview
The Salary-Predictor repository implements a monolithic, API‑first application that predicts job salaries using a machine‑learning model. The system consists of a data ingestion pipeline that reads the CSV dataset, a model training component that builds a Random Forest regressor and serializes it, a Flask‑based prediction API that serves model inference, and a static HTML frontend that collects user input and displays predictions. All components reside in a single codebase with clear module separation, leveraging Python for backend logic, HTML for the UI, and CSV/Pickle for data storage.

## System Layers
### Data Layer
**Technologies:** CSV, Python (pandas)

Handles raw data storage and preprocessing. The source file Position_Salaries.csv in the data directory is loaded, cleaned, and transformed into training features and labels. The processed dataset is used directly by the training script.

### Model Layer
**Technologies:** Python, scikit-learn, Pickle

Encapsulates model training and persistence. The train_model.py script reads the prepared dataset, trains a scikit‑learn Random Forest regressor, evaluates basic metrics, and serializes the trained model to rf_regressor.pkl using pickle. Model metadata is stored in models/metadata.json.

### API Layer
**Technologies:** Python, Flask, Pickle

Exposes a RESTful endpoint for salary prediction. backend/app.py defines a Flask application with an endpoint (e.g., /predict) that accepts JSON payloads of feature values, loads the serialized model, runs inference, and returns the predicted salary as JSON.

### Presentation Layer
**Technologies:** HTML, JavaScript, CSS

Provides a static user interface. frontend/index.html contains a form that gathers input features, posts them to the prediction API via JavaScript fetch, and renders the returned salary. Assets such as cover images reside in the assets folder.

### Infrastructure Layer
**Technologies:** VS Code, Python packaging (pip)

Defines development environment configuration. .vscode/settings.json supplies IDE settings; backend/requirements.txt enumerates Python dependencies required for data processing, model training, and the API.



## Data Flow & Pipelines
1. Data Ingestion: backend/train_model.py reads data/Position_Salaries.csv, performs preprocessing, and splits into features/target. 2. Model Training: The same script trains a RandomForestRegressor, then serializes the model to models/rf_regressor.pkl and writes model metadata to models/metadata.json. 3. Deployment: backend/app.py starts a Flask server, loads models/rf_regressor.pkl at startup (or lazily per request), and exposes a /predict endpoint. 4. Prediction Request: frontend/index.html collects user input, sends a POST request with JSON to /predict. 5. Inference: The API deserializes the model, computes the salary prediction, and returns a JSON response. 6. UI Rendering: The frontend receives the response and updates the DOM to show the predicted salary.

## Key Design Decisions
- API‑First monolith: Even though the UI is static, the Flask API is the sole source of business logic, enabling future decoupling into microservices without rewriting core functionality.
- Pickle for model serialization: Chosen for simplicity and direct compatibility with scikit‑learn; model files are version‑controlled in the repository under models/.
- Random Forest regressor: Provides good baseline performance for tabular salary data without extensive hyper‑parameter tuning.
- Static HTML UI: Keeps the frontend lightweight and easy to host on any static file server, reducing operational overhead.

## Scalability & Reliability
The current monolithic design is suitable for prototype and low‑traffic scenarios. To scale:
- **Horizontal API scaling**: Containerize backend/app.py (e.g., Docker) and run multiple instances behind a load balancer. Because the model is loaded from a pickle file, each instance can cache the deserialized model in memory.
- **Model versioning**: Store model artifacts in an object store (e.g., S3) and load them at runtime, allowing seamless upgrades without redeploying the entire codebase.
- **Asynchronous inference**: For high request volumes, offload predictions to a task queue (Celery/RabbitMQ) to decouple request handling from compute.
- **Data pipeline expansion**: Replace the CSV ingestion with a streaming data source (e.g., Kafka) and retraining jobs scheduled via Airflow if continuous learning is required.
- **Frontend scaling**: Host the static assets on a CDN to reduce latency and handle large numbers of concurrent users.

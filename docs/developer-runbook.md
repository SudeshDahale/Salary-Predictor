# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.8+ installed on the system
- Git for source control
- Node.js (optional, for frontend live-reload if desired)
- Virtual environment tool (venv or virtualenv)
- Access to the project's Git repository

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point. |
| `FLASK_ENV` | Required | Set to `development` to enable debugger and auto‑reload. |
| `MODEL_PATH` | Required | Filesystem path to the serialized RandomForest model (`models/rf_regressor.pkl`). |
| `DATA_PATH` | Optional | Path to the raw CSV dataset used for training. Required only when invoking `train_model.py`. |


## Local Setup & Development
1. 1. Clone the repository:
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. Create and activate a Python virtual environment:
3.    ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
4. 3. Install backend dependencies:
5.    ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```
6. 4. Verify that the training data exists at `data/Position_Salaries.csv`. The repository already contains this file.
7. 5. (Optional) Train or re‑train the model:
8.    ```bash
   python backend/train_model.py
   ```
9.    This script reads the CSV, preprocesses the data, fits a RandomForestRegressor, and writes the serialized model to `models/rf_regressor.pkl` along with metadata in `models/metadata.json`.
10. 6. Set required environment variables (see *Environment Variables* section).
11. 7. Run the Flask API:
12.    ```bash
   export FLASK_APP=backend/app.py
   export FLASK_ENV=development
   export MODEL_PATH=models/rf_regressor.pkl
   export DATA_PATH=data/Position_Salaries.csv   # only needed for retraining
   flask run --port 5000
   ```
13.    The API will be reachable at `http://127.0.0.1:5000`.
14. 8. Open the frontend UI in a browser:
15.    - Either open `frontend/index.html` directly, or serve the `frontend` folder with a simple HTTP server for live reload:
16.    ```bash
   cd frontend
   python -m http.server 8080
   # Then navigate to http://127.0.0.1:8080
   ```
17. 9. Use the form on the page to submit salary prediction requests. The form posts JSON to the Flask endpoint `/predict` and displays the returned salary.

## Running Tests
```bash
pytest || echo "No test suite defined – manual verification recommended"
```

## Troubleshooting
### ImportError: No module named 'flask' when running `flask run`
**Resolution:** Make sure the virtual environment is activated and that you installed the backend requirements (`pip install -r backend/requirements.txt`).

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the model artifact, or verify that the file exists in the repository.

### CORS errors when the frontend tries to POST to the API
**Resolution:** The Flask app includes CORS support via the `flask_cors` package. Ensure it is installed (`pip install flask-cors`) and that the `CORS(app)` call is present in `backend/app.py`.

### The prediction endpoint returns a 500 error with a stack trace about a missing feature column
**Resolution:** The input JSON must contain all features expected by the model (see `backend/app.py` for the required keys). Ensure the frontend form fields match the model's feature names.

### Changes to `frontend/index.html` are not reflected when reloading the page
**Resolution:** If you opened the HTML file directly, the browser may cache it. Clear the cache or serve the folder via a local HTTP server (`python -m http.server`).



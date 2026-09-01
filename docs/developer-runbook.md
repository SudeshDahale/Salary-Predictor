# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed on the system
- Git client for cloning the repository
- Access to a terminal/command prompt
- Internet connection to install Python dependencies

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `MODEL_PATH` | Optional | Absolute or relative path to the serialized Random Forest model (`models/rf_regressor.pkl`). Defaults to `models/rf_regressor.pkl` if not set. |
| `METADATA_PATH` | Optional | Path to the JSON file containing model metadata (`models/metadata.json`). Used for feature validation at inference time. |


## Local Setup & Development
1. 1. Clone the repository:
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. 3. Install backend Python dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. 4. Verify that the data file exists:
   - `data/Position_Salaries.csv` should be present (it ships with the repo).
5. 5. (Optional) Re‑train the model to generate a fresh artifact:
   ```bash
   python backend/train_model.py
   ```
   This script reads the CSV, fits a RandomForestRegressor and writes two files under `models/`:
   - `rf_regressor.pkl` (the Pickle‑serialized model)
   - `metadata.json` (model metadata such as feature order and training date).
6. 6. Set required environment variables (see below).
7. 7. Start the Flask API server:
   ```bash
   export FLASK_APP=backend/app.py   # macOS/Linux
   # set FLASK_APP=backend\app.py   # Windows PowerShell
   export FLASK_ENV=development      # enables auto‑reload
   flask run --port 5000
   ```
   The API will be reachable at `http://127.0.0.1:5000`.
8. 8. Open the frontend UI:
   - Either open `frontend/index.html` directly in a browser (static mode) **or**
   - Serve it through Flask by navigating to `http://127.0.0.1:5000` if the Flask app is configured to serve static files (the current `app.py` does so).
9. 9. Use the UI to input a job title, years of experience, etc., and click **Predict** – the page will POST to the `/predict` endpoint and display the estimated salary.

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"Position": "Data Scientist", "YearsExperience": 5, "Education": "Masters"}'
```

## Troubleshooting
### ImportError: No module named 'flask'
**Resolution:** Make sure the virtual environment is activated and that `pip install -r backend/requirements.txt` completed without errors.

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the model file, or verify that the `models/` directory contains `rf_regressor.pkl`.

### 500 Internal Server Error when calling /predict
**Resolution:** Check the Flask server logs for a stack trace. Common causes are mismatched input field names or missing keys in the JSON payload. Ensure the request body matches the fields expected by `backend/app.py` (see the `expected_features` list in the file).

### CORS errors when the frontend is served from a different origin
**Resolution:** The Flask app includes `flask_cors.CORS(app)`. If you changed the host/port, restart the server so the CORS headers are regenerated, or add the new origin to the allowed list in `app.py`.



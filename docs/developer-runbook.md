# Developer Runbook – Salary-Predictor

## Prerequisites
- Python 3.9+ installed on the system
- Git for cloning the repository
- Internet access to fetch Python packages

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point. |
| `FLASK_ENV` | Optional | Set to `development` for debug mode; `production` for a hardened run. |


## Local Setup & Development
1. 1. Clone the repository:
   ```
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. 3. Install backend dependencies:
   ```
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. 4. Verify that the raw dataset exists at `data/Position_Salaries.csv`. If the file is missing, obtain it from the original source or copy it from a backup.
5. 5. Train (or retrain) the model:
   ```
   python backend/train_model.py
   ```
   This script reads the CSV, fits a Random Forest regressor, and writes two artefacts to the `models/` folder:
   - `rf_regressor.pkl` (the serialized model)
   - `metadata.json` (model hyper‑parameters and training timestamp)
6. 6. Start the Flask prediction service:
   ```
   export FLASK_APP=backend/app.py
   export FLASK_ENV=development   # enables hot‑reload & detailed errors
   flask run --port 5000
   ```
   The API will be reachable at `http://127.0.0.1:5000`.
7. 7. Open the UI in a browser:
   - Simply open `frontend/index.html` (no server required) or serve the `frontend/` folder via a static server (e.g., `python -m http.server 8080` and navigate to `http://localhost:8080`).
8. 8. Use the UI to submit a job position, location, and other features; the frontend sends a POST request to `/predict` and displays the predicted salary.

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"Position": "Data Scientist", "Location": "San Francisco", "Experience": 5, "Education": "Masters"}'
```

## Troubleshooting
### ImportError: No module named 'sklearn'
**Resolution:** Activate the virtual environment and ensure `backend/requirements.txt` has been installed (`pip install -r backend/requirements.txt`).

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Run `python backend/train_model.py` to generate the model artefacts, or copy the missing files into the `models/` directory.

### Flask reports "Address already in use" when starting the server
**Resolution:** Either stop the process occupying port 5000 or start Flask on a different port, e.g., `flask run --port 5001`.

### Frontend returns "Failed to fetch" when submitting the form
**Resolution:** Make sure the Flask API is running and reachable at the URL configured in `frontend/index.html` (default: http://127.0.0.1:5000/predict). Also verify that CORS is not being blocked; the Flask app currently allows all origins.

### Model predictions seem wildly inaccurate
**Resolution:** Re‑train the model after verifying the CSV data integrity. Check `models/metadata.json` for the hyper‑parameters used; you may adjust `n_estimators`, `max_depth`, etc., inside `backend/train_model.py` and rerun the training step.



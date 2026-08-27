# Salary-Predictor Repository – Developer Runbook

## Prerequisites
- Python 3.8 or newer installed and accessible via `python`/`python3`.
- Git installed to clone the repository.
- Virtual environment tool (`venv` or `virtualenv`).
- Internet connection for installing Python dependencies from PyPI.

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point (backend/app.py). Required when using the `flask` CLI. |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reloading and detailed error pages. Optional. |
| `MODEL_PATH` | Optional | If you wish to override the default model location (`models/rf_regressor.pkl`), set this variable. The Flask app reads it on startup. |


## Local Setup & Development
1. 1. **Clone the repository**
   ```bash
2. git clone https://github.com/SudeshDahale/Salary-Predictor.git
3. cd Salary-Predictor
4. ```
5. 
6. 2. **Create and activate a virtual environment**
   ```bash
7. python -m venv .venv
8. # On Windows
9. .venv\Scripts\activate
10. # On macOS/Linux
11. source .venv/bin/activate
12. ```
13. 
14. 3. **Install backend dependencies**
   ```bash
15. pip install -r backend/requirements.txt
16. ```
17. 
18. 4. **Verify the data file is present**
   The CSV used for training lives at `data/Position_Salaries.csv`. No action required unless you replace it.
19. 
20. 5. **(Optional) Retrain the model**
   If you want to generate a fresh model, run:
   ```bash
21. python backend/train_model.py
22. ```
23.    This script reads `data/Position_Salaries.csv`, fits a `RandomForestRegressor`, and writes the serialized model to `models/rf_regressor.pkl` along with `models/metadata.json`.
24. 
25. 6. **Start the Flask prediction service**
   ```bash
26. export FLASK_APP=backend/app.py   # macOS/Linux
27. set FLASK_APP=backend\app.py      # Windows CMD
28. export FLASK_ENV=development       # optional – enables auto‑reload
29. flask run --port 5000
30. ```
31.    The service will be reachable at `http://127.0.0.1:5000/predict`.
32. 
33. 7. **Open the static frontend**
   Open `frontend/index.html` in a browser. The page posts JSON to the `/predict` endpoint and displays the returned salary.

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"years_experience": 5, "education_level": "Bachelor", "city": "San Francisco"}'

# Expected JSON response example
# {"predicted_salary": 85000.0}
```

## Troubleshooting
### ImportError: No module named 'flask' (or other missing packages).
**Resolution:** Ensure the virtual environment is activated and all dependencies are installed with `pip install -r backend/requirements.txt`.

### FileNotFoundError: models/rf_regressor.pkl not found when starting the Flask app.
**Resolution:** Run `python backend/train_model.py` to generate the model artifact, or verify that `models/rf_regressor.pkl` exists and is readable.

### Port 5000 already in use; Flask fails to start.
**Resolution:** Either stop the process using the port (`lsof -i :5000` then `kill <pid>`) or start Flask on a different port, e.g., `flask run --port 5001` and adjust the frontend AJAX URL accordingly.

### CORS error when the frontend HTML tries to POST to `/predict`.
**Resolution:** The Flask app includes the `flask_cors` extension. If you modified `app.py`, ensure `CORS(app)` is called. For local testing, you can open the HTML file via a simple static server (`python -m http.server 8000 --directory frontend`).

### Prediction returns a 500 error with traceback about missing columns.
**Resolution:** The request payload must contain the exact feature names expected by the model (see `train_model.py` for the column list). Align the JSON keys with the training dataset columns.



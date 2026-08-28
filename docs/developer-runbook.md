# Salary-Predictor Repository – Developer Runbook

## Prerequisites
- Python 3.9+ installed on the development machine
- Git client for cloning the repository
- Virtual environment tool (venv or virtualenv) – optional but recommended

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point (backend/app.py). |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reloading and debug logging. |
| `PORT` | Optional | Port on which the Flask API runs. Defaults to 5000 if not set. |


## Local Setup & Development
1. 1. **Clone the repository**
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
3. 3. **Install backend dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. 4. **Verify the trained model files are present**
   Ensure `models/rf_regressor.pkl` and `models/metadata.json` exist (they are tracked in the repo).
5. 5. **Run the Flask API**
   ```bash
   # The Flask entry point lives in backend/app.py
   export FLASK_APP=backend/app.py   # Windows: set FLASK_APP=backend\app.py
   export FLASK_ENV=development      # Enables auto‑reload & debug mode
   flask run --port 5000
   ```
6.    The API will start on `http://127.0.0.1:5000/`.  The only public endpoint (see `backend/app.py`) is:
   - `POST /predict` – expects a JSON payload with the employee features and returns a salary prediction.
   
7. 6. **Open the static UI**
   In a separate terminal, simply open the HTML file:
   ```bash
   start frontend/index.html   # Windows
   open frontend/index.html    # macOS
   xdg-open frontend/index.html # Linux
   ```
   The page posts user input to `http://127.0.0.1:5000/predict` and displays the result.
8. 7. **Optional – Retrain the model**
   If you need to regenerate the model, run the training script:
   ```bash
   python backend/train_model.py --data data/Position_Salaries.csv --output-dir models/
   ```
   This script uses `scikit‑learn`'s `RandomForestRegressor` and writes `rf_regressor.pkl` and `metadata.json`.
   

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"position": "Data Scientist", "experience": 3, "education": "Masters", "location": "San Francisco"}'
# Expected response (example): {"predicted_salary": 125000}
```

## Troubleshooting
### ImportError: cannot import name 'Flask' from 'flask'
**Resolution:** Ensure the virtual environment is active and that `backend/requirements.txt` has been installed. Re‑run `pip install -r backend/requirements.txt`.

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Confirm the `models/` directory contains `rf_regressor.pkl` and `metadata.json`. If missing, regenerate the model by executing `python backend/train_model.py`.

### Port 5000 already in use when running `flask run`
**Resolution:** Either stop the process occupying the port or run Flask on a different port, e.g., `flask run --port 5001`. Update the UI's fetch URL accordingly.

### CORS errors when the HTML page calls the API
**Resolution:** The Flask app (see `backend/app.py`) already enables CORS via `flask_cors`. If you modified the code, ensure `CORS(app)` is called before registering routes.

### Prediction endpoint returns 500 Internal Server Error
**Resolution:** Check the Flask console output for traceback. Common causes are:
- Mismatched JSON keys (the UI sends keys that the model expects). Verify the payload matches the schema used in `app.py`.
- Scikit‑learn version mismatch causing the pickled model to be unreadable. Align the version with the one used during training (`requirements.txt` pins scikit‑learn).



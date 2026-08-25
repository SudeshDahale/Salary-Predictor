# Salary Predictor – Developer Runbook

## Prerequisites
- Git
- Python 3.9+
- pip
- virtualenv (or venv)
- Node.js is NOT required – frontend is static HTML/CSS/JS
- Internet access to install Python packages

## Local Setup & Development
1. 1. Clone the repository
2. ```bash
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor
```
3. 2. Create and activate a virtual environment
4. ```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# .\venv\Scripts\activate   # Windows PowerShell
```
5. 3. Install backend dependencies
6. ```bash
pip install -r backend/requirements.txt
```
7. 4. Verify that the data file exists (it is shipped with the repo)
8. ```bash
ls data/Position_Salaries.csv
```
9. 5. (Optional) Retrain the model – only needed if you modify the training script or want a fresh model
10. ```bash
python backend/train_model.py
```
11.    - The script reads `data/Position_Salaries.csv`, trains a Random Forest Regressor, and writes:
12.      - `models/rf_regressor.pkl`  – serialized model
13.      - `models/metadata.json`    – model metadata (feature list, version, training date)
14. 
15. 6. Start the Flask API server
16. ```bash
export FLASK_APP=backend/app.py   # Linux/macOS
set FLASK_APP=backend\app.py        # Windows CMD
flask run --port 5000
```
17.    - The API will be reachable at `http://127.0.0.1:5000`.
18.    - Primary endpoint: `POST /predict` with JSON payload `{ "experience": ..., "education": ..., "city": ... }` (see `backend/app.py` for exact schema).
19. 
20. 7. Open the static frontend
21.    - The UI is a plain HTML page; you can open it directly:
22. ```bash
open frontend/index.html   # macOS
start frontend\index.html   # Windows
xdg-open frontend/index.html # Linux
```
23.    - Or serve it via a simple HTTP server (useful for CORS when the UI calls the API):
24. ```bash
python -m http.server 8080 --directory frontend
# then navigate to http://localhost:8080
```

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"experience":5,"education":"Masters","city":"San Francisco"}'
```

## Troubleshooting
### ImportError or ModuleNotFoundError when running `backend/app.py` or `train_model.py`
**Resolution:** Make sure the virtual environment is activated and that all packages from `backend/requirements.txt` are installed. Re‑run `pip install -r backend/requirements.txt`.

### FileNotFoundError for `data/Position_Salaries.csv` or `models/rf_regressor.pkl`
**Resolution:** Confirm you are running the commands from the repository root. The relative paths in the code assume the `data/` and `models/` directories are siblings of `backend/`. If the model file is missing, execute `python backend/train_model.py` to generate it.

### Flask server returns 500 Internal Server Error on `/predict`
**Resolution:** Check the server logs; common causes are mismatched feature names or missing metadata. Ensure `models/metadata.json` exists and that the JSON schema matches the input fields expected by `backend/app.py`.

### Frontend cannot reach the API (CORS error or network failure)
**Resolution:** If you opened `index.html` directly via `file://`, the browser blocks XHR requests. Serve the UI with a local HTTP server (step 7) or enable CORS in `backend/app.py` (the repo already includes `flask_cors`). Ensure the API URL in `frontend/index.html` points to `http://127.0.0.1:5000`.

### Model training is extremely slow or crashes
**Resolution:** The dataset is modest (~few thousand rows). If you experience memory pressure, ensure you are not running other heavy workloads, or reduce the number of trees in `train_model.py` (parameter `n_estimators`).



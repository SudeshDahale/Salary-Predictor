# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed on the development machine.
- Git installed to clone the repository.
- Internet access to install Python packages from PyPI.

## Local Setup & Development
1. 1. Clone the repository:
2.    ```
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 2. Create and activate a virtual environment (recommended):
7.    ```
8.    python -m venv venv
9.    # On Windows
10.    venv\Scripts\activate
11.    # On macOS/Linux
12.    source venv/bin/activate
13.    ```
14. 3. Install backend dependencies defined in `backend/requirements.txt`:
15.    ```
16.    pip install -r backend/requirements.txt
17.    ```
18. 4. Verify the trained model artifact exists (`models/rf_regressor.pkl`). If you need to retrain:
19.    ```
20.    python backend/train_model.py
21.    ```
22.    This script reads `data/Position_Salaries.csv`, fits a `RandomForestRegressor`, and writes the model to `models/rf_regressor.pkl` and metadata to `models/metadata.json`.
23. 5. Launch the Flask prediction service:
24.    ```
25.    python backend/app.py
26.    ```
27.    By default the API runs on `http://127.0.0.1:5000` (see `backend/app.py` for the exact host/port).
28. 6. Open the UI in a browser:
29.    - Open `frontend/index.html` directly (file://) or serve the static files with any simple HTTP server, e.g.:
30.    ```
31.    cd frontend
32.    python -m http.server 8000
33.    ```
34.    Then navigate to `http://localhost:8000` and use the form to submit salary queries.

## Running Tests
```bash
### API sanity check
curl -X POST -H "Content-Type: application/json" -d '{"position": "Data Scientist", "experience": 3}' http://127.0.0.1:5000/predict

### End‑to‑end UI test (manual)
1. Run the Flask API (`backend/app.py`).
2. Serve the frontend (`python -m http.server` inside `frontend`).
3. Fill the form in the browser and verify a numeric salary is displayed.

```

## Troubleshooting
### ImportError or ModuleNotFoundError when running `backend/app.py` or `train_model.py`.
**Resolution:** Ensure the virtual environment is activated and all packages from `backend/requirements.txt` are installed. Re‑run `pip install -r backend/requirements.txt`.

### FileNotFoundError: `models/rf_regressor.pkl` not found.
**Resolution:** Run the training script `python backend/train_model.py` to generate the model artifact, or verify that the `models/` directory contains `rf_regressor.pkl` and `metadata.json`.

### Port 5000 already in use when starting the Flask server.
**Resolution:** Either stop the process occupying the port or change the port in `backend/app.py` (e.g., `app.run(port=5001)`).

### CORS errors when the frontend attempts to call the API.
**Resolution:** The Flask app includes CORS handling via `flask_cors`. If missing, install the package (`pip install flask-cors`) and ensure `CORS(app)` is called in `backend/app.py`.

### Prediction response is empty or returns HTTP 500.
**Resolution:** Check the console logs of `backend/app.py` for stack traces. Common causes are mismatched input keys (the API expects fields defined in the request JSON) or a corrupted model file. Re‑train the model if needed.



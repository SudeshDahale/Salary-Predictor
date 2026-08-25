# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.8+ installed on the development machine
- Git for source control
- Node.js (optional) if you wish to serve the static frontend via a simple HTTP server

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Entry point for the Flask development server. |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reload and debug mode. |


## Local Setup & Development
1. 1. Clone the repository:
2.    ```bash
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 2. Create and activate a Python virtual environment:
7.    ```bash
8.    python -m venv venv
9.    # Windows
10.    venv\Scripts\activate
11.    # macOS/Linux
12.    source venv/bin/activate
13.    ```
14. 3. Install backend dependencies:
15.    ```bash
16.    cd backend
17.    pip install -r requirements.txt
18.    cd ..
19.    ```
20. 4. (Optional) Install a lightweight HTTP server for the frontend if you prefer not to use Flask to serve static files:
21.    ```bash
22.    npm install -g serve   # or use Python's built‑in server later
23.    ```
24. 5. Verify the data file is present:
25.    Ensure `data/Position_Salaries.csv` exists – it is the source used for training and inference.
26. 6. Train the model (first‑time setup):
27.    ```bash
28.    python backend/train_model.py
29.    ```
30.    This script reads `data/Position_Salaries.csv`, fits a `RandomForestRegressor`, and writes the serialized model to `models/rf_regressor.pkl` together with metadata in `models/metadata.json`.
31. 7. Run the Flask API:
32.    ```bash
33.    export FLASK_APP=backend/app.py   # Windows: set FLASK_APP=backend\app.py
34.    export FLASK_ENV=development      # optional – enables auto‑reload
35.    flask run --port 5000
36.    ```
37.    The API will be reachable at `http://127.0.0.1:5000/predict` (POST JSON).
38. 8. Open the UI:
39.    - Either open `frontend/index.html` directly in a browser (the page makes a CORS‑enabled fetch to `http://127.0.0.1:5000/predict`).
40.    - Or serve the static folder:
41.      ```bash
42.      cd frontend
43.      serve . -l 3000   # or: python -m http.server 3000
44.      ```
45.      Then navigate to `http://localhost:3000`.

## Running Tests
```bash
pytest -q  # (No test suite currently – use manual curl checks below)
# Manual API sanity check
curl -X POST http://127.0.0.1:5000/predict \
     -H 'Content-Type: application/json' \
     -d '{"experience":5,"education":"Bachelors","city":"New York"}'
```

## Troubleshooting
### ImportError: No module named 'sklearn'
**Resolution:** Activate the virtual environment and reinstall requirements: `pip install -r backend/requirements.txt`.

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the model pickle. Verify `models/rf_regressor.pkl` exists.

### CORS error when the UI calls the API
**Resolution:** The Flask app includes CORS headers via `flask_cors`. Ensure the Flask server is running on the same host/port specified in the UI fetch request, or adjust the `origin` in `backend/app.py`.

### Port 5000 already in use
**Resolution:** Start Flask on an alternative port: `flask run --port 5001` and update the fetch URL in `frontend/index.html` accordingly.

### Model prediction returns NaN or unrealistic values
**Resolution:** Confirm the preprocessing steps in `backend/app.py` match those used during training (e.g., categorical encoding). Re‑run `train_model.py` after any data schema change.



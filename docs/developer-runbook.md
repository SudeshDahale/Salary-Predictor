# Salary-Predictor – Developer Runbook

## Prerequisites
- Python 3.9+ installed on the development machine.
- Git for source control.
- Internet access to download Python dependencies.

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point. |
| `FLASK_ENV` | Optional | Set to `development` to enable hot‑reloading and detailed error pages. |


## Local Setup & Development
1. 1. Clone the repository:
2.    ```
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 
7. 2. Create and activate a virtual environment (recommended):
8.    ```
9.    python -m venv venv
10.    # Windows
11.    venv\Scripts\activate
12.    # macOS / Linux
13.    source venv/bin/activate
14.    ```
15. 
16. 3. Install backend Python dependencies:
17.    ```
18.    pip install --upgrade pip
19.    pip install -r backend/requirements.txt
20.    ```
21. 
22. 4. Verify that the CSV dataset is present at `data/Position_Salaries.csv`. If the file is missing, obtain it from the original source or ask a teammate.
23. 
24. 5. Train the model (creates `models/rf_regressor.pkl` and `models/metadata.json`):
25.    ```
26.    python backend/train_model.py
27.    ```
28.    *The script reads `data/Position_Salaries.csv`, fits a RandomForestRegressor, and persists the artefacts in the `models/` directory.*
29. 
30. 6. Run the Flask API locally:
31.    ```
32.    export FLASK_APP=backend/app.py   # macOS / Linux
33.    set FLASK_APP=backend\app.py      # Windows CMD
34.    export FLASK_ENV=development       # optional – enables auto‑reload
35.    flask run --port 5000
36.    ```
37.    The service will be reachable at `http://127.0.0.1:5000`.
38. 
39. 7. Open the static UI:
40.    * Open `frontend/index.html` in a web browser.
41.    * The page posts JSON to `http://127.0.0.1:5000/predict` and displays the returned salary estimate.

## Running Tests
```bash
There are no dedicated test suites in the current codebase.  To verify end‑to‑end functionality you can:
```bash
# 1) Ensure the API is running (step 6 above)
# 2) Issue a sample prediction request
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"experience":5,"education":"Bachelors","location":"NY"}'
```
You should receive a JSON response with a `salary` field.

Additionally, you can manually run the notebook `random_forest_regression.ipynb` to explore data and model performance.
```

## Troubleshooting
### `ModuleNotFoundError: No module named 'flask'`
**Resolution:** Activate the virtual environment and reinstall dependencies: `source venv/bin/activate && pip install -r backend/requirements.txt`.

### `FileNotFoundError: [Errno 2] No such file or directory: 'data/Position_Salaries.csv'`
**Resolution:** Confirm the CSV exists at the expected path. If missing, retrieve the dataset from the project source or ask a teammate.

### `OSError: [Errno 2] No such file or directory: 'models/rf_regressor.pkl'` when calling `/predict`
**Resolution:** Run `python backend/train_model.py` to generate the model artefacts before starting the API.

### CORS‑related errors in the browser UI
**Resolution:** The current Flask app does not enable CORS. For local development, either open `index.html` via `file://` (which bypasses CORS) or install `flask-cors` and add `CORS(app)` in `backend/app.py`.

### Changes to `backend/app.py` are not reflected without restarting the server
**Resolution:** Ensure `FLASK_ENV=development` is set before running `flask run`. This enables the built‑in reloader.



# Salary-Predictor Developer Runbook

## Prerequisites
- Git
- Python >=3.8
- pip
- virtualenv (or venv module)
- A web browser for UI testing

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Entry point for Flask; points to the main application module. |
| `FLASK_ENV` | Optional | Set to `development` to enable debugger and auto‑reloader. |


## Local Setup & Development
1. 1. Clone the repository:
2.    ```
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 2. Create and activate a virtual environment:
7.    ```
8.    python -m venv venv
9.    # Windows
10.    venv\Scripts\activate
11.    # macOS/Linux
12.    source venv/bin/activate
13.    ```
14. 3. Install backend dependencies:
15.    ```
16.    pip install -r backend/requirements.txt
17.    ```
18. 4. Verify that the training data exists:
19.    - The CSV file `data/Position_Salaries.csv` should be present. If you receive a "File not found" error, ensure the `data` folder is in the project root.
20. 5. (Optional) Train / refresh the model:
21.    ```
22.    python backend/train_model.py
23.    ```
24.    This script reads `data/Position_Salaries.csv`, fits a `RandomForestRegressor`, and writes:
25.    - `models/rf_regressor.pkl` – the serialized model
26.    - `models/metadata.json` – JSON with feature‑order, model version, and training timestamp.
27.    *If the model files already exist and you do not need to retrain, you can skip this step.*
28. 6. Set required Flask environment variables (if any). The project uses the default Flask configuration, but for explicitness you may set:
29.    ```
30.    export FLASK_APP=backend/app.py
31.    export FLASK_ENV=development   # enables auto‑reloader
32.    ```
33. 7. Run the backend API:
34.    ```
35.    flask run --host=127.0.0.1 --port=5000
36.    ```
37.    The service will be reachable at `http://127.0.0.1:5000`.
38. 8. Open the UI:
39.    - Open `frontend/index.html` in a browser (e.g., double‑click the file or serve it via a simple HTTP server).
40.    - The UI posts JSON to the backend endpoint `/predict` and displays the returned salary.
41. 9. Development loop:
42.    - Edit `frontend/index.html` / CSS / JS and refresh the browser.
43.    - Edit backend code in `backend/app.py` or `backend/train_model.py` and restart Flask (auto‑reload works when `FLASK_ENV=development`).

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"position": "Data Scientist", "experience": 5}'
# Expected response: {"salary": <predicted_value>}
```

## Troubleshooting
### ImportError: No module named 'sklearn'
**Resolution:** Ensure you installed the requirements inside the activated virtual environment (`pip install -r backend/requirements.txt`).

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Run `python backend/train_model.py` to generate the model artifact, or copy the provided `models/rf_regressor.pkl` into the `models` directory.

### Address already in use: port 5000
**Resolution:** Either stop the process using the port or start Flask on a different port, e.g., `flask run --port=5001`.

### Frontend shows "Failed to fetch" or CORS errors
**Resolution:** The UI is a static file; when opened directly (`file://`), browsers block XHR to `http://127.0.0.1:5000`. Serve the UI via a simple server, e.g., `python -m http.server 8080` inside the `frontend` folder and open `http://localhost:8080`.

### Prediction values seem wildly inaccurate
**Resolution:** Retrain the model after verifying the CSV format. Run `python backend/train_model.py` and ensure `models/rf_regressor.pkl` is updated.



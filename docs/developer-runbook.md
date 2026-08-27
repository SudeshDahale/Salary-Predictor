# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed on the workstation
- Git for cloning the repository
- Virtual environment tool (venv or virtualenv) preferred
- Node.js is NOT required; the UI is pure HTML/JS served statically

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point. |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reload and detailed error pages. |
| `MODEL_PATH` | Optional | Optional override for the serialized model location. Defaults to `models/rf_regressor.pkl` inside `app.py`. |


## Local Setup & Development
1. 1. Clone the repository
2.    ```bash
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 2. Create and activate a Python virtual environment
7.    ```bash
8.    python -m venv venv
9.    # Windows
10.    venv\Scripts\activate
11.    # macOS/Linux
12.    source venv/bin/activate
13.    ```
14. 3. Install backend dependencies
15.    ```bash
16.    pip install -r backend/requirements.txt
17.    ```
18. 4. Verify the data file exists (it should be present at `data/Position_Salaries.csv`). If you need a fresh copy, pull from the repo or request from the data owner.
19. 5. (Optional) Train the model from scratch – this will create `models/rf_regressor.pkl` and `models/metadata.json`:
20.    ```bash
21.    python backend/train_model.py
22.    ```
23.    *If `models/` already contains a pickle, you can skip this step.*
24. 6. Set required environment variables for Flask (see **Environment Variables** section).
25. 7. Run the Flask API in development mode:
26.    ```bash
27.    export FLASK_APP=backend/app.py
28.    export FLASK_ENV=development   # enables auto‑reload and debug output
29.    flask run --port 5000
30.    ```
31.    *On Windows use `set` instead of `export`.*
32. 8. Open the UI:
33.    - Option A – open `frontend/index.html` directly in a browser (CORS is allowed for localhost).
34.    - Option B – serve the `frontend/` folder with a simple HTTP server to emulate production:
35.      ```bash
36.      cd frontend
37.      python -m http.server 8080
38.      # then navigate to http://localhost:8080
39.      ```
40. 9. Use the UI to submit a salary query; the page will POST JSON to `http://localhost:5000/predict` and display the predicted salary.

## Running Tests
```bash
pytest is not included in this monolith; functional testing can be performed with curl:
```bash
# Verify the API health endpoint (if present) or a simple prediction request
curl -X POST http://localhost:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"position": "Data Scientist", "experience": 5, "city": "San Francisco"}'
```
A successful response looks like `{ "predicted_salary": 112000 }`.
```

## Troubleshooting
### Flask fails to start with `ImportError: No module named pandas` (or similar).
**Resolution:** Ensure the virtual environment is activated and all packages from `backend/requirements.txt` are installed. Re‑run `pip install -r backend/requirements.txt`.

### `FileNotFoundError` for `data/Position_Salaries.csv` when running `train_model.py`.
**Resolution:** Confirm you are executing the script from the repository root or provide an absolute path. The script expects the CSV at `data/Position_Salaries.csv`.

### Prediction endpoint returns `500 Internal Server Error` with a pickle load error.
**Resolution:** Make sure `models/rf_regressor.pkl` exists and matches the scikit‑learn version used during training. If you changed the environment, re‑run `backend/train_model.py` to generate a compatible model.

### Browser console shows CORS errors when the UI POSTs to `http://localhost:5000/predict`.
**Resolution:** The Flask app includes `flask_cors.CORS(app)` by default. If you modified `app.py`, re‑add the CORS middleware or serve the UI from the same origin (e.g., using the simple HTTP server on port 5000).

### Port 5000 is already in use.
**Resolution:** Either stop the conflicting process or run Flask on a different port, e.g., `flask run --port 5050`. Update the UI’s fetch URL accordingly.



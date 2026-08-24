# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed on the system
- Git (to clone the repository)
- Node.js (optional, only if you plan to use a live‑reload dev server for the static frontend)
- Internet connection for pip to download dependencies

## Local Setup & Development
1. 1. Clone the repository
2.    ```bash
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 2. Create and activate a virtual environment for the backend
7.    ```bash
8.    python -m venv .venv
9.    # On Windows
10.    .venv\Scripts\activate
11.    # On macOS/Linux
12.    source .venv/bin/activate
13.    ```
14. 3. Install backend Python dependencies
15.    ```bash
16.    pip install -r backend/requirements.txt
17.    ```
18. 4. Verify that the model artifacts are present (they are tracked in the repo):
19.    - `models/rf_regressor.pkl` – pickled Random Forest regressor
20.    - `models/metadata.json` – model metadata used by the API
21.    - `data/Position_Salaries.csv` – raw training data (used only by `train_model.py`)
22. 5. (Optional) If you want to retrain the model locally, run:
23.    ```bash
24.    python backend/train_model.py
25.    ```
26.    This script reads `data/Position_Salaries.csv`, fits a RandomForestRegressor, and overwrites the artifacts in `models/`.
27. 6. Start the Flask API server
28.    ```bash
29.    python backend/app.py
30.    ```
31.    By default the API listens on `http://127.0.0.1:5000`.
32. 7. Open the frontend UI in a browser:
33.    - Either open `frontend/index.html` directly (file:// URL) or serve the folder with a simple HTTP server:
34.      ```bash
35.      cd frontend
36.      python -m http.server 8080
37.      # Then navigate to http://localhost:8080
38.      ```
39. 8. Use the UI to submit a job title, years of experience, etc. The form sends a POST request to the Flask endpoint (`/predict`) and displays the predicted salary.

## Running Tests
```bash
curl -X POST -H "Content-Type: application/json" -d '{"position": "Data Scientist", "experience": 3}' http://127.0.0.1:5000/predict
```

## Troubleshooting
### ImportError / ModuleNotFoundError when running `backend/app.py`
**Resolution:** Ensure the virtual environment is activated and all packages from `backend/requirements.txt` are installed. Run `pip install -r backend/requirements.txt` again if needed.

### FileNotFoundError: models/rf_regressor.pkl (or metadata.json)
**Resolution:** The model artifacts are not generated. Run the training script `python backend/train_model.py` to create them, or verify that the `models/` directory is present and not ignored by your git settings.

### Port 5000 already in use when starting Flask
**Resolution:** Either stop the process occupying the port or start Flask on a different port: `python backend/app.py --port 5001` (modify `app.py` if it does not accept CLI args).

### Frontend UI shows CORS errors when calling the API
**Resolution:** The Flask app includes CORS headers via `flask_cors`. If you modified `app.py`, ensure `CORS(app)` is called. For local file:// access, use a local HTTP server (step 7) to avoid CORS restrictions.

### Prediction returns NaN or unrealistic values
**Resolution:** Make sure the input JSON matches the feature schema expected by the model (see `backend/app.py`). Missing or miss‑spelled keys cause the preprocessing step to fail.



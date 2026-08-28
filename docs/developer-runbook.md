# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed on the development machine
- Git installed for source control
- Access to a terminal / command prompt
- Basic knowledge of Flask and scikit-learn

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point. |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reloading and debug mode (optional). |
| `MODEL_PATH` | Optional | Absolute or relative path to the serialized model (`models/rf_regressor.pkl`). If omitted, the app defaults to `models/rf_regressor.pkl`. |


## Local Setup & Development
1. 1. **Clone the repository**
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Unix/macOS
   source venv/bin/activate
   ```
3. 3. **Install backend dependencies** (the requirements are listed in `backend/requirements.txt`)
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. 4. **Verify the data file exists** – `data/Position_Salaries.csv` must be present (it is part of the repository). No extra steps are required unless you intend to replace it with a custom dataset.
5. 5. **(Optional) Train / re‑train the model** – the training script is `backend/train_model.py`. Running it will produce `models/rf_regressor.pkl` and `models/metadata.json`.
   ```bash
   python backend/train_model.py
   ```
6. 6. **Set required environment variables** (see the "Environment Variables" section). For a typical local run you can set them in the shell or create a `.env` file in the project root.
7. 7. **Start the Flask API** – the entry point is `backend/app.py`.
   ```bash
   export FLASK_APP=backend/app.py   # Windows: set FLASK_APP=backend\app.py
   export FLASK_ENV=development      # optional, enables hot‑reload
   flask run
   ```
8. 8. **Open the UI** – point a browser to `http://127.0.0.1:5000/`. The static UI lives in `frontend/index.html` and is served by the Flask app.

## Running Tests
```bash
```bash
# Verify the API health check (if one exists) or the prediction endpoint directly.
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"experience":5,"education":"Bachelor","city":"New York"}'

# Expected result: a JSON payload containing the predicted salary, e.g. {"salary": 85000}
```
```

## Troubleshooting
### ImportError: No module named 'flask' (or scikit-learn).
**Resolution:** Make sure the virtual environment is active and dependencies from `backend/requirements.txt` are installed. Re‑run `pip install -r backend/requirements.txt`.

### FileNotFoundError: `models/rf_regressor.pkl` not found.
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the model files, or verify that `models/rf_regressor.pkl` is present in the repository.

### HTTP 500 error when calling `/predict`.
**Resolution:** Check the Flask console output for stack traces. Common causes are mismatched feature columns between the request JSON and the training data. Ensure the JSON keys match the features expected by `backend/app.py` (e.g., `experience`, `education`, `city`).

### Port 5000 already in use.
**Resolution:** Either stop the process that is occupying the port or start Flask on a different port: `flask run --port 5001`.

### HTML UI does not load or shows a blank page.
**Resolution:** Confirm that Flask is serving static files from the `frontend/` directory. The `backend/app.py` should have a route like `@app.route('/')` that returns `frontend/index.html`. If you modified the file structure, update the route accordingly.



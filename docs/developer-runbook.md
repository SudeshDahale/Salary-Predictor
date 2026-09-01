# Salary Predictor - Developer Runbook

## Prerequisites
- Git
- Python 3.8 or higher
- pip
- Virtualenv (optional but recommended)
- Node.js (only if you wish to serve the frontend via a dev server, not required for basic usage)

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Path to the Flask application entry point. |
| `FLASK_ENV` | Optional | Set to `development` to enable debug mode and auto‑reload. |
| `MODEL_PATH` | Optional | Absolute or relative path to the serialized Random Forest model. Defaults to `models/rf_regressor.pkl` if not set. |


## Local Setup & Development
1. 1. **Clone the repository**
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. **Create and activate a virtual environment** (recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. 3. **Install backend dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```
4. 4. **Verify the dataset is present**
   The file `data/Position_Salaries.csv` should exist. If it is missing, obtain it from the original source or ask the project maintainer.
5. 5. **(Optional) Retrain the model**
   If you want to rebuild the model from scratch, run:
   ```bash
   python backend/train_model.py
   ```
   This will generate `models/rf_regressor.pkl` and update `models/metadata.json`.
   *Note*: The repository already ships a pre‑trained model, so this step can be skipped for normal development.
6. 6. **Start the Flask API**
   ```bash
   export FLASK_APP=backend/app.py   # Windows: set FLASK_APP=backend\app.py
   export FLASK_ENV=development       # Enables auto‑reload; optional
   flask run --host=0.0.0.0 --port=5000
   ```
   The API will be reachable at `http://localhost:5000`.
7. 7. **Serve the frontend**
   The UI is a static HTML page. You can open it directly in a browser (`frontend/index.html`) or serve it via a simple HTTP server to avoid CORS issues:
   ```bash
   # Using Python's built‑in server
   cd frontend
   python -m http.server 8080
   ```
   Then navigate to `http://localhost:8080`.
   The page will POST JSON to the Flask endpoint `/predict`.
   8. **Iterate**
   - Modify `backend/app.py` to adjust API logic.
   - Adjust the training script `backend/train_model.py` for new features or hyper‑parameters.
   - Refresh the frontend to see updated predictions.
   - When changes are made to the API, the Flask development server will auto‑reload.


## Running Tests
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"Position": "Data Scientist", "Location": "San Francisco", "Company Size": "100-500", "Education": "Master"}'
```

## Troubleshooting
### Flask fails to start with `ModuleNotFoundError` for a package.
**Resolution:** Ensure you are inside the virtual environment and that `pip install -r backend/requirements.txt` completed without errors. Re‑run the install command if needed.

### `FileNotFoundError: [Errno 2] No such file or directory: 'data/Position_Salaries.csv'` during training.
**Resolution:** Confirm the CSV file exists at `data/Position_Salaries.csv`. If missing, copy it from the original dataset source or ask the maintainer.

### `pickle.UnpicklingError` when the API loads `models/rf_regressor.pkl`.
**Resolution:** The model file may be corrupted. Re‑run `python backend/train_model.py` to regenerate the pickle, or replace the file with a fresh copy from the repository.

### CORS error in the browser when the frontend calls the API.
**Resolution:** Run the frontend via a local HTTP server (`python -m http.server`) instead of opening the HTML file directly, or add appropriate CORS headers in `backend/app.py` (e.g., using `flask-cors`).

### Port 5000 already in use.
**Resolution:** Stop the process occupying the port or start Flask on a different port, e.g., `flask run --port 5001`. Update the frontend JavaScript to point to the new port.



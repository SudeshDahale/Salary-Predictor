# Salary-Predictor Developer Runbook

## Prerequisites
- Git
- Python 3.8+
- pip
- virtualenv (or venv)
- Internet connection (for initial pip install)
- Optional: VS Code or any IDE for debugging

## Local Setup & Development
1. 1. **Clone the repository**
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```
3. 3. **Install backend dependencies**
   ```bash
   pip install -r backend/requirements.txt
   ```
4. 4. **Verify the data and model assets are present**
   - `data/Position_Salaries.csv` – raw CSV used for training.
   - `models/rf_regressor.pkl` – pre‑trained Random Forest model.
   - `models/metadata.json` – model metadata (feature list, version, etc.).
   These files are already committed; ensure they are not omitted by any Git LFS or ignore rules.
5. 5. **(Optional) Install frontend tooling** – the UI is pure HTML/CSS/JS, so no npm install is required. Simply open `frontend/index.html` in a browser after the backend is running.
6. 6. **Run the Flask API**
   ```bash
   python backend/app.py
   ```
   The service will start on `http://127.0.0.1:5000` (default Flask port).
7. 7. **Open the UI**
   - Open `frontend/index.html` in your preferred browser.
   - The page expects the API at `http://127.0.0.1:5000/predict`. Adjust the JavaScript fetch URL in `frontend/index.html` only if you change the host/port.

## Running Tests
```bash
No automated test suite is included in the repository. Manual sanity checks:

1. **Smoke‑test the API**
   ```bash
   curl -X POST http://127.0.0.1:5000/predict \
        -H "Content-Type: application/json" \
        -d '{"experience":5,"education":"Bachelors","city":"San Francisco"}'
   ```
   You should receive a JSON response with a `salary` field.

2. **Re‑train the model** (useful to verify the training pipeline)
   ```bash
   python backend/train_model.py
   ```
   This script reads `data/Position_Salaries.csv`, fits a `RandomForestRegressor`, and overwrites `models/rf_regressor.pkl` and `models/metadata.json`.

3. **Validate the UI**
   - Fill the form on `frontend/index.html` and submit.
   - Confirm the displayed salary matches the API response.
```

## Troubleshooting
### ImportError: No module named 'flask' (or other packages)
**Resolution:** Ensure the virtual environment is activated and all dependencies are installed via `pip install -r backend/requirements.txt`. Re‑run the install command if you added new packages.

### FileNotFoundError for `data/Position_Salaries.csv` or `models/rf_regressor.pkl`
**Resolution:** Confirm you are running the commands from the repository root. Paths in the code are relative to the project root (`data/` and `models/`). If you moved files, restore them from the repo.

### Flask server starts but `/predict` returns 500 Internal Server Error
**Resolution:** Check the server logs for the traceback. Common causes:
- Mismatch between model metadata and input fields (e.g., missing required feature). Ensure the JSON payload matches the feature names expected in `models/metadata.json`.
- Corrupted model file. Delete `models/rf_regressor.pkl` and re‑run `backend/train_model.py` to generate a fresh model.

### Frontend shows a CORS error or cannot reach the API
**Resolution:** The UI uses a plain fetch request to `http://127.0.0.1:5000/predict`. Make sure the Flask app is running on the same host/port. If you change the host, update the fetch URL in `frontend/index.html` accordingly.

### Training script runs extremely slowly or crashes with memory errors
**Resolution:** The dataset (`Position_Salaries.csv`) is modest (~few thousand rows). If you see memory pressure, verify you are not inadvertently loading a much larger file. You can limit the training size in `backend/train_model.py` by sub‑sampling the DataFrame.



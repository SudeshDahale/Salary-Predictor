# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed on the machine.
- Git installed to clone the repository.
- Access to the internet to install Python dependencies.

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Optional | Specifies the Flask application entry point. Set to `backend/app.py` when using `flask run`. |
| `FLASK_ENV` | Optional | Enables development mode (`development`) which provides debugger and auto‑reload. |


## Local Setup & Development
1. 1. Clone the repository:
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. 3. Install backend dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. 4. Verify that the CSV dataset exists at `data/Position_Salaries.csv`. If it is missing, download it from the original source or ask a teammate.
5. 5. Train the model (or re‑train if you modified the training script):
   ```bash
   python backend/train_model.py
   ```
   This script reads `data/Position_Salaries.csv`, fits a `RandomForestRegressor`, and writes two artifacts to the `models/` directory:
   - `rf_regressor.pkl` – the serialized model
   - `metadata.json` – model metadata (features, version, etc.)
6. 6. Start the Flask API server:
   ```bash
   python backend/app.py
   ```
   The server listens on `http://127.0.0.1:5000` by default and exposes the `/predict` endpoint.
7. 7. Open the UI in a browser:
   - Either serve the static files with a simple HTTP server (e.g., `python -m http.server 8080 --directory frontend`) and navigate to `http://localhost:8080`, or
   - Open `frontend/index.html` directly (the page makes AJAX calls to `http://127.0.0.1:5000/predict`).
8. 8. (Optional) Run the Jupyter notebook `random_forest_regression.ipynb` to explore the data and model performance interactively.

## Running Tests
```bash
Validate the API with a quick curl request:
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"YearsExperience": 5, "EducationLevel": "Bachelor", "City": "San Francisco"}'
```
You should receive a JSON response similar to:
```json
{ "predicted_salary": 85000.23 }
```
```

## Troubleshooting
### ImportError / ModuleNotFoundError when running `backend/app.py` or `train_model.py`.
**Resolution:** Ensure the virtual environment is activated and that you installed the requirements (`pip install -r backend/requirements.txt`). Re‑run the install step if needed.

### `FileNotFoundError: [Errno 2] No such file or directory: 'models/rf_regressor.pkl'` when calling `/predict`.
**Resolution:** Run the training script (`python backend/train_model.py`) to generate `models/rf_regressor.pkl` and `models/metadata.json`. Verify that the `models/` directory contains both files.

### Port 5000 already in use, Flask fails to start.
**Resolution:** Either stop the process occupying the port or start Flask on a different port:
```bash
python backend/app.py --port 5001
```
Update the AJAX URL in `frontend/index.html` accordingly.

### CORS errors in the browser console when the UI calls the `/predict` endpoint.
**Resolution:** The Flask app includes a simple CORS header (`Access-Control-Allow-Origin: *`). If you modified `app.py`, re‑add the header or install `flask-cors` and wrap the app:
```python
from flask_cors import CORS
CORS(app)
```

### Model predictions seem wildly off (e.g., negative salaries).
**Resolution:** Check that the input JSON keys and data types match the training schema (see `models/metadata.json`). Missing or mis‑typed fields cause the model to receive NaNs, leading to erroneous outputs. Also ensure you are using the latest trained model.



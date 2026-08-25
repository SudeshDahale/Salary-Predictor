# Salary-Predictor Developer Runbook

## Prerequisites
- Git
- Python 3.9+ installed and added to PATH
- pip (Python package manager)
- Virtual environment tool (venv or virtualenv)
- A web browser for UI testing

## Local Setup & Development
1. 1. **Clone the repository**
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. **Create and activate a Python virtual environment**
   ```bash
   # Unix/macOS
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. 3. **Install backend dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r backend/requirements.txt
   ```
4. 4. **Verify the dataset is present**
   The CSV file `data/Position_Salaries.csv` ships with the repo; no action required unless you replace it with your own data.
5. 5. **(Optional) Retrain the model**
   If you modify the dataset or want to experiment with different hyper‑parameters, run the training script:
   ```bash
   python backend/train_model.py
   ```
   This will (re)create `models/rf_regressor.pkl` and update `models/metadata.json`.
6. 6. **Start the Flask API**
   ```bash
   python backend/app.py
   ```
   By default the service runs on `http://127.0.0.1:5000`.
   The API exposes:
   - `GET /` – health check (returns *"Salary Predictor API is running"*).
   - `POST /predict` – expects a JSON payload with the keys `position`, `experience`, `education`, etc., and returns a JSON object containing the predicted salary.
7. 7. **Open the frontend UI**
   Open `frontend/index.html` in a browser (no server required). The UI posts to `http://127.0.0.1:5000/predict` and displays the prediction.
   If you prefer to serve the static files via Flask, add the `frontend` folder to the Flask static path or run a simple HTTP server:
   ```bash
   cd frontend
   python -m http.server 8080
   ```
   Then navigate to `http://localhost:8080`.

## Running Tests
```bash
### Quick sanity‑check of the API
```bash
# Ensure the Flask server is running (step 6 above)
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"position": "Data Scientist", "experience": 5, "education": "Masters"}'
```
You should receive a JSON response similar to:
```json
{"predicted_salary": 115000}
```
### Unit‑test placeholder (if tests are added later)
```bash
pytest
```
```

## Troubleshooting
### ImportError: No module named 'flask' (or other missing package)
**Resolution:** Make sure you activated the virtual environment and installed the requirements (`pip install -r backend/requirements.txt`).

### FileNotFoundError: 'models/rf_regressor.pkl' not found when calling `/predict`
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the model file, or ensure the `models` directory contains `rf_regressor.pkl`.

### Port 5000 already in use
**Resolution:** Either stop the process occupying the port or start the Flask app on an alternate port:
```bash
python backend/app.py --port 5001
```

### Frontend shows a CORS error when calling the API
**Resolution:** The Flask app includes CORS support via the `flask-cors` package. If you removed it, reinstall and add:
```python
from flask_cors import CORS
CORS(app)
```

### Prediction values look wildly off (e.g., negative salaries)
**Resolution:** Confirm you are using the correct, most recent model file. Retrain the model with the provided dataset (`backend/train_model.py`). Also verify that the input JSON keys match what the model expects.



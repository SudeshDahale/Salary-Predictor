# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed and added to PATH
- Git installed for source control
- Internet access to install Python dependencies

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Optional | Entry point for the Flask development server (set to `backend/app.py`). |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reload and debugging. |


## Local Setup & Development
1. 1. Clone the repository:
   ```bash
   git clone https://github.com/SudeshDahale/Salary-Predictor.git
   cd Salary-Predictor
   ```
2. 2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
3. 3. Install backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. 4. Verify the dataset is present (the repository includes it):
   ```bash
   ls data/Position_Salaries.csv
   ```
5. 5. Train the model (creates `models/rf_regressor.pkl` and `models/metadata.json`):
   ```bash
   python backend/train_model.py
   ```
6. 6. Launch the Prediction API (listens on http://127.0.0.1:5000 by default):
   ```bash
   python backend/app.py
   ```
7. 7. Open the UI in a browser (no server needed for static HTML):
   - Double‑click `frontend/index.html` **or** serve it via a simple HTTP server:
     ```bash
     cd frontend
     python -m http.server 8000
     ```
   - Then navigate to `http://localhost:8000`.
   - The UI will call the local API at `http://127.0.0.1:5000/predict` to obtain salary predictions.

## Running Tests
```bash
curl -X POST -H "Content-Type: application/json" -d '{"Position": "Data Scientist", "Location": "San Francisco", "YearsExperience": 3}' http://127.0.0.1:5000/predict
```

## Troubleshooting
### ImportError / ModuleNotFoundError when running scripts.
**Resolution:** Ensure the virtual environment is activated and all packages from `backend/requirements.txt` are installed.

### FileNotFoundError: `data/Position_Salaries.csv` not found.
**Resolution:** Confirm you are running commands from the repository root. The file lives at `data/Position_Salaries.csv`.

### pickle.UnpicklingError when loading `models/rf_regressor.pkl`.
**Resolution:** Re‑run the training script (`python backend/train_model.py`) to regenerate a compatible model file.

### API returns 404 or connection refused.
**Resolution:** Make sure the Flask server is running (`python backend/app.py`). Verify it is listening on port 5000 and no other process is occupying that port.

### Frontend UI shows CORS or network errors when calling `/predict`.
**Resolution:** The UI expects the API at `http://127.0.0.1:5000`. If you changed the host/port, update the fetch URL in `frontend/index.html` accordingly.



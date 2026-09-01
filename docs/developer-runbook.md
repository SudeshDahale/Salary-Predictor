# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed
- Git for source control
- Virtual environment tool (venv or conda)
- Node.js is NOT required (frontend is static HTML)
- Access to a terminal/command prompt

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Optional | Points Flask to the application entry point. Set to `app.py` when using `flask run`. |
| `FLASK_ENV` | Optional | Set to `development` to enable debug mode and auto‑reloading. |


## Local Setup & Development
1. 1. Clone the repository:
2.    ```
3.    git clone https://github.com/SudeshDahale/Salary-Predictor.git
4.    cd Salary-Predictor
5.    ```
6. 2. Create and activate a Python virtual environment:
7.    ```
8.    python -m venv venv
9.    # Windows
10.    venv\Scripts\activate
11.    # macOS/Linux
12.    source venv/bin/activate
13.    ```
14. 3. Install backend dependencies:
15.    ```
16.    cd backend
17.    pip install -r requirements.txt
18.    cd ..
19.    ```
20. 4. Verify the data file is present:
21.    - `data/Position_Salaries.csv` contains the historical salary records used for model training.
22. 5. (Optional) Inspect the Jupyter notebook `random_forest_regression.ipynb` to understand model training logic.
23. 6. Launch the Flask API locally:
24.    ```
25.    cd backend
26.    python app.py
27.    ```
28.    The service starts on `http://127.0.0.1:5000` (default Flask port).
29. 7. Open the static UI:
30.    - Open `frontend/index.html` in a web browser.
31.    - The page sends HTTP requests to the locally‑running API (endpoint details are defined in `backend/app.py`).
32. 8. (If you need to re‑train the model) run the training script:
33.    ```
34.    cd backend
35.    python train_model.py
36.    ```
37.    This script reads `data/Position_Salaries.csv`, fits a Random Forest regressor, and writes:
38.    - `models/rf_regressor.pkl` (pickled model)
39.    - `models/metadata.json` (feature/target schema, training date, etc.)

## Running Tests
```bash
There are no dedicated test suites in this monolith. Quick sanity checks:
```bash
# 1. Verify the API returns a prediction for a sample payload
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"position": "Data Scientist", "experience": 3, "location": "Remote"}'
# Expected: JSON response with a `salary` field.

# 2. Run the training script in dry‑run mode (it prints model R²)
python backend/train_model.py --dry-run
```
If you add unit tests later, place them under a `tests/` folder and execute `pytest`.
```

## Troubleshooting
### ImportError or missing package when running `app.py`
**Resolution:** Ensure you installed the exact versions from `backend/requirements.txt` inside the activated virtual environment.

### Flask server crashes with `FileNotFoundError: [Errno 2] No such file or directory: 'models/rf_regressor.pkl'`
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the model pickle and metadata files before starting the API.

### Frontend shows a blank page or CORS error
**Resolution:** The HTML page expects the API at `http://127.0.0.1:5000`. Verify the Flask server is running and reachable. If you change the host/port, update the fetch URL in `frontend/index.html` accordingly.

### `curl` request returns 404 or 405
**Resolution:** Confirm the endpoint path matches the route defined in `backend/app.py` (e.g., `/predict`). Use the correct HTTP method (POST).

### Model accuracy appears far lower after re‑training
**Resolution:** Check that `data/Position_Salaries.csv` has not been corrupted. The notebook `random_forest_regression.ipynb` documents expected preprocessing steps.



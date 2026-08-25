# Salary-Predictor Developer Runbook

## Prerequisites
- Python 3.9+ installed
- Git for source control
- Virtual environment tool (venv or conda)
- Internet access to install Python dependencies

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Entry point for the Flask development server (points to backend/app.py). |
| `FLASK_ENV` | Optional | Set to `development` to enable auto‑reload and detailed error pages. |


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
16.    cd backend
17.    pip install -r requirements.txt
18.    cd ..
19.    ```
20. 4. (Optional) Install Jupyter if you want to explore `random_forest_regression.ipynb`:
21.    ```
22.    pip install notebook
23.    ```
24. 5. Verify the data file exists at `data/Position_Salaries.csv`. The repository ships this CSV; no additional download is required.
25. 6. Train the model (first‑time setup). The training script writes the model artifact to `models/rf_regressor.pkl` and metadata to `models/metadata.json`:
26.    ```
27.    python backend/train_model.py
28.    ```
29.    *If the model files already exist, you can skip this step.*
30. 7. Start the Flask API:
31.    ```
32.    cd backend
33.    export FLASK_APP=app.py   # macOS/Linux
34.    set FLASK_APP=app.py      # Windows
35.    flask run --port 5000
36.    ```
37.    The API will be reachable at `http://127.0.0.1:5000/predict` (POST JSON).
38. 8. Open the frontend:
39.    - Open `frontend/index.html` in a web browser, or
40.    - Serve the static files with a simple HTTP server for live reload:
41.      ```
42.      cd frontend
43.      python -m http.server 8080
44.      ```
45.    Then navigate to `http://localhost:8080`.

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"years_experience":5,"education":"Masters","city":"San Francisco"}'
```

## Troubleshooting
### ImportError: No module named 'flask' (or other missing packages)
**Resolution:** Ensure the virtual environment is activated and dependencies are installed with `pip install -r backend/requirements.txt`.

### FileNotFoundError: data/Position_Salaries.csv not found
**Resolution:** Confirm the repository was cloned with the `data` directory intact. The CSV should be at the path `data/Position_Salaries.csv`.

### Model file not found: models/rf_regressor.pkl
**Resolution:** Run `python backend/train_model.py` to generate the model artifact. Verify that `models/metadata.json` is also created.

### Flask reports "Address already in use" when starting the server
**Resolution:** Another process is listening on port 5000. Either stop that process or start Flask on a different port, e.g., `flask run --port 5001`.

### Frontend shows "Failed to fetch" after clicking Predict
**Resolution:** The backend API must be running and CORS must be allowed. By default `app.py` enables CORS via `flask_cors`. Verify the Flask server is reachable at the URL used in the JavaScript (`http://127.0.0.1:5000/predict`).



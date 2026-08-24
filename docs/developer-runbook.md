# Salary-Predictor Development Runbook

## Prerequisites
- Python 3.8+ installed on the system
- Git for version control
- Internet connection to install Python packages

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
16.    pip install --upgrade pip
17.    pip install -r backend/requirements.txt
18.    ```
19. 4. Verify that the pre‑trained model and metadata are present:
20.    - `models/rf_regressor.pkl` – serialized RandomForest model
21.    - `models/metadata.json` – model version and training statistics
22. 5. (Optional) If you want to retrain the model, ensure the CSV data file exists:
23.    ```
24.    ls data/Position_Salaries.csv
25.    ```
26.    The training script `backend/train_model.py` will read this file and rewrite the model files.
27. 6. Set required environment variables (if any). The project currently does not require custom variables, but for extensibility you may define:
28.    - `FLASK_ENV=development` – enables Flask debug mode
29.    - `MODEL_PATH=models/rf_regressor.pkl` – path to the serialized model (defaults to the same path in code)
30.    Export them before starting the server:
31.    ```
32.    export FLASK_ENV=development
33.    export MODEL_PATH=models/rf_regressor.pkl
34.    ```
35. 7. Launch the Flask API:
36.    ```
37.    cd backend
38.    flask run --port 5000
39.    ```
40.    The API will be reachable at `http://127.0.0.1:5000`.
41. 8. Open the front‑end UI:
42.    - Open `frontend/index.html` in a browser (no server needed for static assets) or serve the folder with a simple HTTP server:
43.    ```
44.    cd frontend
45.    python -m http.server 8000
46.    ```
47.    Then navigate to `http://localhost:8000`.
48. 9. Use the UI to submit job details; the form posts to the Flask endpoint `/predict` and displays the returned salary.

## Running Tests
```bash
## No formal test suite provided. Manual validation steps:
1. Start the backend as described above.
2. In a separate terminal, issue a curl request:
```bash
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"Country":"United States","Education":"Bachelors","Experience":5,"Job Title":"Data Scientist"}'
```
   Expected response: a JSON payload with a `predicted_salary` field.
3. Verify the front‑end UI reflects the same prediction when you fill the form and press *Submit*.

```

## Troubleshooting
### ImportError: No module named 'flask' when running `flask run`
**Resolution:** Make sure the virtual environment is activated and that you installed the requirements (`pip install -r backend/requirements.txt`).

### FileNotFoundError: models/rf_regressor.pkl not found
**Resolution:** Confirm that the `models/` directory contains `rf_regressor.pkl` and `metadata.json`. If missing, retrain the model by running `python backend/train_model.py` which will generate the files.

### CORS error when the front‑end tries to call the API
**Resolution:** The Flask app is configured for same‑origin requests. Either serve the front‑end from the same host/port (e.g., using `python -m http.server` on port 5000) or enable CORS in `backend/app.py` by installing `flask-cors` and adding `CORS(app)`.

### Port 5000 already in use
**Resolution:** Run the Flask server on an alternative port, e.g., `flask run --port 5050`, and update the front‑end AJAX URL accordingly.



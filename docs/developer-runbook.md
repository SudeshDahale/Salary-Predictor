# Salary Predictor – Developer Runbook

## Prerequisites
- Python 3.9+ installed
- Git for source control
- Node.js (optional, only for serving static frontend if using a dev server)
- Internet connection to install Python packages

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Optional | Entry point for Flask when using `flask run`. Set to `backend/app.py`. |
| `FLASK_ENV` | Optional | Set to `development` to enable hot‑reloading and detailed error pages. |


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
16.    pip install -r backend/requirements.txt
17.    ```
18. 4. Verify that the data file exists at `data/Position_Salaries.csv`. This CSV is used for model training.
19. 5. (Optional) Train the model locally to generate a fresh pickle:
20.    ```
21.    python backend/train_model.py
22.    ```
23.    - The script reads `data/Position_Salaries.csv`, trains a `RandomForestRegressor`, and writes `models/rf_regressor.pkl` and `models/metadata.json`.
24. 6. Start the Flask API server:
25.    ```
26.    python backend/app.py
27.    ```
28.    - By default the API runs on `http://127.0.0.1:5000` and exposes the `/predict` POST endpoint.
29. 7. Open the frontend UI:
30.    - The static page lives at `frontend/index.html`. You can open it directly in a browser (`file://`), or serve it with a simple HTTP server for CORS friendliness:
31.    ```
32.    cd frontend
33.    python -m http.server 8080
34.    ```
35.    - Then navigate to `http://localhost:8080`.
36. 8. Use the UI to submit a job title, experience, and location. The form will POST JSON to the Flask `/predict` endpoint and display the predicted salary.
37. 9. (Optional) Run the Jupyter notebook `random_forest_regression.ipynb` for exploratory analysis and model diagnostics.

## Running Tests
```bash
pytest || echo "No test suite defined – manual verification is recommended."
# Manual test: with the API running, execute:
curl -X POST http://127.0.0.1:5000/predict \
     -H "Content-Type: application/json" \
     -d '{"position": "Data Scientist", "experience": 3, "location": "San Francisco"}'
```

## Troubleshooting
### ImportError: No module named 'pandas' (or other package)
**Resolution:** Ensure the virtual environment is activated and dependencies are installed with `pip install -r backend/requirements.txt`.

### Flask server returns 500 Internal Server Error on `/predict`
**Resolution:** Check `backend/app.py` logs – most likely the model file `models/rf_regressor.pkl` is missing or corrupted. Re‑run `python backend/train_model.py` to regenerate it.

### CORS errors when the frontend calls the API
**Resolution:** The Flask app includes a simple CORS header. If you serve the HTML via `file://` you may hit browser restrictions; instead serve the frontend with `python -m http.server` as described in step 7.

### Prediction values seem unrealistic (e.g., negative salary)
**Resolution:** Inspect `backend/train_model.py` – ensure the target column is correctly selected and that the model is trained on cleaned data. Retrain after fixing any data preprocessing issues.

### Port 5000 already in use
**Resolution:** Start the Flask app on a different port: `python backend/app.py --port 5001` (modify `app.run()` accordingly) or free the existing process.



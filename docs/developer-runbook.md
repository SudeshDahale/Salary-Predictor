# Salary Predictor Development Runbook

## Prerequisites
- Git
- Python >=3.9
- pip
- virtualenv (or venv module)
- Node.js (optional, only for frontend tooling)
- Internet connection for pip package download

## Environment Variables
| Variable | Status | Description |
| :--- | :--- | :--- |
| `FLASK_APP` | Required | Entry point for Flask; set to backend/app.py |
| `FLASK_ENV` | Optional | Flask environment, e.g., development or production |
| `MODEL_PATH` | Optional | Path to the serialized model file; defaults to models/rf_regressor.pkl |


## Local Setup & Development
1. git clone https://github.com/SudeshDahale/Salary-Predictor.git
2. cd Salary-Predictor
3. python -m venv venv
4. source venv/bin/activate   # On Windows use 'venv\Scripts\activate'
5. pip install -r backend/requirements.txt
6. Ensure the dataset exists at data/Position_Salaries.csv (provided in repo).
7. Run the training script to generate the model: python backend/train_model.py
8. Verify that models/rf_regressor.pkl and models/metadata.json are created.
9. Export required env vars (example below).
10. Start the Flask API: flask run --host=0.0.0.0 --port=5000
11. Open frontend/index.html in a browser (or serve the static folder with a simple HTTP server).

## Running Tests
```bash
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"experience":5,"education":"Bachelors","city":"New York"}'
```

## Troubleshooting
### ImportError or ModuleNotFoundError (e.g., pandas, sklearn).
**Resolution:** Activate the virtual environment and reinstall dependencies: source venv/bin/activate && pip install -r backend/requirements.txt

### flask command not found.
**Resolution:** Ensure the virtual environment is active; Flask is installed via requirements.txt. If still missing, run: pip install flask

### Port 5000 already in use.
**Resolution:** Stop the process using the port or start Flask on an alternate port: flask run --port=5001

### Model file not found (FileNotFoundError for rf_regressor.pkl).
**Resolution:** Run the training script (backend/train_model.py) to generate the model, or verify that the path set in MODEL_PATH matches the actual location.

### Prediction API returns 500 Internal Server Error.
**Resolution:** Check the Flask console for stack trace. Common causes: malformed JSON payload, missing required fields, or mismatched feature names. Adjust the request payload to match the model's expected input schema.



# Salary Predictor – Development Runbook

## Prerequisites
- Python 3.9 or later installed
- Git installed
- Virtual environment tool (venv or conda)

## Local Setup & Development
1. git clone https://github.com/SudeshDahale/Salary-Predictor.git
2. cd Salary-Predictor
3. python -m venv venv && source venv/bin/activate   # on Windows use `venv\Scripts\activate`
4. pip install -r backend/requirements.txt
5. Verify that data/Position_Salaries.csv is present (it ships with the repo)
6. Run the training script to (re)create the model: python backend/train_model.py   # this generates models/rf_regressor.pkl and models/metadata.json
7. Start the Flask API: cd backend && export FLASK_APP=app.py && export FLASK_ENV=development && flask run   # on Windows use `set` instead of `export`

## Running Tests
```bash
# Manual smoke test – ensure the API returns a prediction
curl -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"YearsExperience":5,"EducationLevel":"Bachelor"}'
```

## Troubleshooting
### ImportError: No module named 'sklearn' when running train_model.py or app.py
**Resolution:** Activate the virtual environment and ensure you installed the requirements: `pip install -r backend/requirements.txt`

### FileNotFoundError for models/rf_regressor.pkl when calling the /predict endpoint
**Resolution:** Run the training script (`python backend/train_model.py`) to generate the serialized model before starting the Flask server

### Flask server fails to start with "Error: Could not locate a Flask application"
**Resolution:** Make sure you are in the `backend` directory and have set FLASK_APP to `app.py` (e.g., `export FLASK_APP=app.py` on Unix or `set FLASK_APP=app.py` on Windows)



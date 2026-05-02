"""
Random Forest Regression - Flask REST API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, json, numpy as np, os

app = Flask(__name__)
CORS(app)

BASE = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE, '..', 'models')

regressor = joblib.load(os.path.join(MODEL_DIR, 'rf_regressor.pkl'))
with open(os.path.join(MODEL_DIR, 'metadata.json')) as f:
    meta = json.load(f)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'model': 'RandomForestRegressor', 'n_estimators': 10})


@app.route('/api/metadata', methods=['GET'])
def metadata():
    return jsonify(meta)


@app.route('/api/predict', methods=['POST'])
def predict():
    body = request.get_json(force=True)
    level = body.get('level')
    if level is None:
        return jsonify({'error': 'Missing "level" field'}), 400
    try:
        level = float(level)
    except (ValueError, TypeError):
        return jsonify({'error': '"level" must be a number'}), 400

    prediction = regressor.predict([[level]])[0]
    return jsonify({
        'level': level,
        'predicted_salary': round(float(prediction), 2)
    })


if __name__ == '__main__':
    print("🚀 Salary Predictor API running on http://localhost:5000")
    app.run(debug=True, port=5000)

"""
Random Forest Regression - Model Training
Exact code from random_forest_regression.ipynb
Dataset: Position_Salaries.csv
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib, json, os

# ── Importing the dataset (exact notebook code)
dataset = pd.read_csv('../data/Position_Salaries.csv')
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values

# ── Training the Random Forest Regression model on the whole dataset (exact notebook code)
regressor = RandomForestRegressor(n_estimators=10, random_state=0)
regressor.fit(X, y)

# ── Predicting a new result (exact notebook code)
test_pred = regressor.predict([[6.5]])
print(f"Prediction for level 6.5: {test_pred}")  # Should print [167000.]

# ── Save model and dataset info
os.makedirs('../models', exist_ok=True)
joblib.dump(regressor, '../models/rf_regressor.pkl')

# Build prediction curve data (for visualisation, exact notebook logic)
X_grid = np.arange(min(X)[0], max(X)[0], 0.01)
X_grid_reshaped = X_grid.reshape((len(X_grid), 1))
y_grid = regressor.predict(X_grid_reshaped).tolist()

meta = {
    "n_estimators": 10,
    "random_state": 0,
    "test_prediction_level_6_5": float(test_pred[0]),
    "dataset": {
        "positions": dataset['Position'].tolist(),
        "levels": dataset['Level'].tolist(),
        "salaries": dataset['Salary'].tolist(),
    },
    "curve": {
        "x": X_grid.tolist(),
        "y": y_grid,
    }
}

with open('../models/metadata.json', 'w') as f:
    json.dump(meta, f)

print("Model saved to ../models/rf_regressor.pkl")
print("Metadata saved to ../models/metadata.json")

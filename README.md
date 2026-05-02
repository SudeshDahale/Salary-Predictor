# Salary Predictor - Predictive Analytics Application 
![Cover Image](./assets/salary-cover.png)


Built using the exact code from `random_forest_regression.ipynb` and the `Position_Salaries.csv` dataset.

---

## Deployed Link - https://salary-prediction-rf.netlify.app/
> Wait for couple of minutes when using for the first time

## 📁 Project Structure

```
salary_predictor/
├── random_forest_regression.ipynb   ← Original notebook (unchanged)
├── data/
│   └── Position_Salaries.csv        ← Original dataset (unchanged)
├── backend/
│   ├── train_model.py               ← Trains model using exact notebook code
│   ├── app.py                       ← Flask REST API
│   └── requirements.txt
├── frontend/
│   └── index.html                   ← UI (works offline too)
├── models/
│   ├── rf_regressor.pkl             ← Trained model (auto-generated)
│   └── metadata.json                ← Model info + dataset + curve data
└── README.md
```

---

## 🚀 How to Run

### Step 1 — Install dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 2 — Train the model
```bash
cd backend
python train_model.py
```
Output:
```
Prediction for level 6.5: [167000.]
Model saved to ../models/rf_regressor.pkl
```

### Step 3 — Start the API
```bash
python backend/app.py
# → Running on http://localhost:5000
```

### Step 4 — Open the UI
Open `frontend/index.html` in any browser.

> ✅ The UI **works offline** too — it uses a built-in model simulation when the API is not running.

---

## 🤖 ML Model (Exact Notebook Code)

```python
# Importing the dataset
dataset = pd.read_csv('Position_Salaries.csv')
X = dataset.iloc[:, 1:-1].values
y = dataset.iloc[:, -1].values

# Training the Random Forest Regression model on the whole dataset
from sklearn.ensemble import RandomForestRegressor
regressor = RandomForestRegressor(n_estimators = 10, random_state = 0)
regressor.fit(X, y)

# Predicting a new result
regressor.predict([[6.5]])   # → array([167000.])
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |
| GET | `/api/metadata` | Model info, dataset, curve data |
| POST | `/api/predict` | Predict salary for a given level |

### Example
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"level": 6.5}'
```
```json
{ "level": 6.5, "predicted_salary": 167000.0 }
```

---

## 📊 Dataset

| Position | Level | Salary |
|---|---|---|
| Business Analyst | 1 | $45,000 |
| Junior Consultant | 2 | $50,000 |
| Senior Consultant | 3 | $60,000 |
| Manager | 4 | $80,000 |
| Country Manager | 5 | $110,000 |
| Region Manager | 6 | $150,000 |
| Partner | 7 | $200,000 |
| Senior Partner | 8 | $300,000 |
| C-level | 9 | $500,000 |
| CEO | 10 | $1,000,000 |

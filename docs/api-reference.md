# Salary Predictor API Reference

**Base URL:** `http://localhost:5000`  
**Authentication:** None – The API is publicly accessible within the deployment environment. Production deployments may add token‑based authentication.

## Overview
The Salary Predictor provides a RESTful API for predicting salaries based on job position, years of experience, and other features. The Flask backend loads a pre‑trained Random Forest regression model (rf_regressor.pkl) and exposes a single prediction endpoint. The API follows an API‑first design and is consumed by the static HTML frontend.

Base URL: http://<host>:5000 (or as configured).

## Endpoints
### `POST` /predict
Generate a salary prediction for a given set of input features. The request payload must be JSON containing the same columns used during model training (e.g., "Position", "YearsExperience", "EducationLevel", etc.). The endpoint validates the input, runs the model, and returns the predicted salary.

**Parameters / Payload:**
JSON body with keys matching the training feature set. Example:
```json
{
  "Position": "Data Scientist",
  "YearsExperience": 3,
  "EducationLevel": "Master",
  "Location": "San Francisco",
  "CompanySize": "Medium"
}
```

**Response:**
```json
JSON object with the predicted salary and optional metadata.
```json
{
  "predicted_salary": 112500,
  "currency": "USD",
  "model_version": "1.0",
  "timestamp": "2026-08-27T12:34:56Z"
}
```
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – The JSON payload is missing, malformed, or lacks required feature fields. |
| `500` | Internal Server Error – Unexpected failure while loading the model, processing the request, or generating the prediction. |


# Salary Predictor API Reference

**Base URL:** `http://localhost:5000`  
**Authentication:** None (open API for demonstration purposes)

## Overview
The Salary Predictor provides a Flask‑based REST API for generating salary estimates using a trained RandomForest regression model. The API accepts structured JSON payloads describing a job posting and returns a numeric salary prediction. The service is bundled with a simple static HTML frontend that consumes the same endpoint.

## Endpoints
### `POST` /predict
Generate a salary prediction for a single job posting. The request body must be a JSON object containing the feature fields expected by the model (see `data/Position_Salaries.csv` for the original column names).

**Parameters / Payload:**
JSON object with keys matching the training columns, e.g.
```json
{
  "Location": "San Francisco",
  "Company": "Acme Corp",
  "Position": "Data Scientist",
  "Years_of_Experience": 3,
  "Education_Level": "Masters",
  "Remote": false
}
```

**Response:**
```json
JSON object with the predicted salary.
```json
{ "predicted_salary": 123456.78 }
```
```

---
### `GET` /metadata
Return basic information about the deployed model, such as the training date, feature list, and model performance metrics stored in `models/metadata.json`.

**Parameters / Payload:**
None

**Response:**
```json
JSON object mirroring the contents of `models/metadata.json`, e.g.
```json
{
  "model_type": "RandomForestRegressor",
  "trained_on": "2023-11-01",
  "features": ["Location","Company","Position","Years_of_Experience","Education_Level","Remote"],
  "r2_score": 0.87
}
```
```

---
### `GET` /healthz
Lightweight health‑check endpoint used by orchestration tools. Returns 200 when the Flask app is running and the model file can be loaded.

**Parameters / Payload:**
None

**Response:**
```json
Plain‑text `OK` with HTTP 200.
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – malformed JSON, missing required fields, or invalid data types. |
| `404` | Not Found – the requested endpoint does not exist. |
| `500` | Internal Server Error – model loading failure, prediction exception, or unexpected server error. |


# Salary Predictor API

**Base URL:** `http://localhost:5000`  
**Authentication:** None – the API is open for local use. In production a token‑based scheme should be added.

## Overview
The Salary Predictor service provides a RESTful API for estimating compensation based on job attributes. It is built with Flask, loads a pre‑trained Random Forest model from `models/rf_regressor.pkl` and exposes endpoints for prediction and optional model retraining.

## Endpoints
### `GET` /
Health check returning a simple JSON confirming the service is running.

**Parameters / Payload:**
None

**Response:**
```json
{ "status": "ok" }
```

---
### `POST` /predict
Accepts job feature data and returns the estimated salary.

**Parameters / Payload:**
JSON object with keys matching the model's feature columns (e.g., "experience", "education_level", "city", "company_size", etc.).

**Response:**
```json
{ "predicted_salary": 85000.0 }
```

---
### `POST` /train
Triggers model retraining using the CSV dataset located at `data/Position_Salaries.csv`. Returns metadata about the new model.

**Parameters / Payload:**
Optional JSON with training hyper‑parameters (e.g., "n_estimators", "max_depth"). If omitted defaults are used.

**Response:**
```json
{ "message": "model retrained", "model_version": "2023-09-01", "rmse": 10234.5 }
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad request – missing or malformed JSON payload. |
| `404` | Endpoint not found. |
| `500` | Internal server error – model loading or prediction failure. |


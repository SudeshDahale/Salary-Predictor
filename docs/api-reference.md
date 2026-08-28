# Salary Predictor API

**Base URL:** `http://localhost:8000/api`  
**Authentication:** None – the API is open within the local deployment. Production deployments should place the service behind authentication/proxy if needed.

## Overview
The Salary Predictor service provides a Flask‑based REST API for estimating salary based on job attributes using a pre‑trained RandomForestRegressor model. The API is the primary interface for the monolithic application, which also serves a static HTML frontend.

**Base URL**: ``http://<host>:<port>/`` (as defined by the Flask ``app`` instance in ``backend/app.py``).

## Endpoints
### `GET` /health
Return a health‑check confirming the service is running and the model is loaded.

**Parameters / Payload:**
None

**Response:**
```json
{ "status": "ok", "model_loaded": true }
```

---
### `POST` /predict
Predict the salary for a single job description supplied in JSON format.

**Parameters / Payload:**
{
  "features": {
    "YearsExperience": <float>,
    "EducationLevel": "<string>",
    "JobTitle": "<string>",
    "Location": "<string>"
    // additional numeric/categorical columns that match the training CSV
  }
}

**Response:**
```json
{
  "predicted_salary": <float>,
  "model_version": "<string>"
}
```

---
### `POST` /train
Trigger a re‑training of the model using the CSV in ``data/Position_Salaries.csv``. Returns the new model version identifier.

**Parameters / Payload:**
None (the server reads the CSV directly). Optional JSON body can contain "reset": true to discard the existing model before retraining.

**Response:**
```json
{
  "message": "training completed",
  "model_version": "<string>",
  "accuracy": <float>
}
```

---
### `GET` /model
Download the current serialized model file.

**Parameters / Payload:**
None

**Response:**
```json
Binary stream of ``models/rf_regressor.pkl`` with ``Content‑Type: application/octet-stream``
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `404` | Endpoint not found. |
| `405` | Method not allowed for the requested URL. |


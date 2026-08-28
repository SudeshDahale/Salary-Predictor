# Salary Predictor API Reference

**Base URL:** `http://<host>:<port>/api`  
**Authentication:** None – the service is intended for internal use behind the front‑end. No API keys or tokens are required.

## Overview
The Salary Predictor is a monolithic Flask application that serves a machine‑learning model (RandomForestRegressor) trained on historic position salary data. The API is designed to be consumed by the static HTML front‑end located in `frontend/`. It exposes a single public endpoint for salary prediction and a health‑check endpoint. All requests and responses use JSON.

**Key modules**
- `backend/app.py` – Flask application defining the API routes.
- `backend/train_model.py` – Script that trains and serialises the model to `models/rf_regressor.pkl` and creates `models/metadata.json`.
- `models/rf_regressor.pkl` – Pickled RandomForestRegressor model.
- `models/metadata.json` – JSON file describing the feature schema used by the model.
- `frontend/index.html` – UI that POSTs user input to the API.

The API follows an API‑First approach: the front‑end interacts exclusively through the documented HTTP endpoints.


## Endpoints
### `POST` /api/predict
Return a salary prediction for a given job description. The request payload must conform to the feature schema defined in `models/metadata.json`.

**Parameters / Payload:**
JSON body containing the following fields (all required unless marked optional):
```json
{
  "position": "Software Engineer",          // string – job title / position name
  "experience_years": 3,                     // number – total years of professional experience
  "education_level": "Bachelor",           // string – one of the levels defined in metadata (e.g., "High School", "Bachelor", "Master", "PhD")
  "location": "San Francisco, CA",          // string – city and state or country code
  "company_size": "Medium",                // string – optional, values: "Small", "Medium", "Large"
  "skill_score": 0.78                        // number (0‑1) – optional, aggregated skill similarity score
}
```
The exact list of accepted features is derived from `models/metadata.json`; any missing or extra fields will result in a validation error.

**Response:**
```json
On success (HTTP 200) the service returns a JSON object with the predicted annual salary in USD:
```json
{
  "predicted_salary": 112500,
  "currency": "USD",
  "model_version": "1.0.0",
  "timestamp": "2026-08-28T14:32:10Z"
}
```
```

---
### `GET` /api/health
Simple health‑check endpoint used by monitoring tools and the front‑end to verify that the Flask service and the ML model are loaded correctly.

**Parameters / Payload:**
None

**Response:**
```json
Returns HTTP 200 with a short JSON payload:
```json
{ "status": "ok", "model_loaded": true }
```
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `404 Not Found` | The requested endpoint does not exist. |
| `405 Method Not Allowed` | The HTTP method used is not supported for the endpoint. |


# Salary Predictor API Reference

**Base URL:** `http://<host>:5000`  
**Authentication:** No authentication required – the service is open for demo purposes.

## Overview
The Salary Predictor provides a RESTful API built with Flask for salary estimation based on job title and related features. The API loads a pre‑trained Random Forest regressor stored in models/rf_regressor.pkl and returns predictions in JSON. An optional endpoint allows retraining the model using the CSV dataset in data/Position_Salaries.csv.

## Endpoints
### `POST` /predict
Accepts job‑related features and returns the estimated salary.

**Parameters / Payload:**
JSON body with fields: "position" (string, required), "experience_years" (number, optional), "education_level" (string, optional). Only fields used by the model are considered.

**Response:**
```json
JSON object with keys: "salary" (float) – predicted salary, "model_version" (string) – version from models/metadata.json.
```

---
### `POST` /retrain
Triggers model retraining using the CSV dataset. Returns status of the training job.

**Parameters / Payload:**
No request body required. Optional query parameter "async" (boolean) to run training asynchronously.

**Response:**
```json
JSON object with keys: "status" (string) – e.g., "started" or "completed", "model_version" (string) – new version identifier.
```

---
### `GET` /health
Health‑check endpoint that verifies the Flask app and model loading are operational.

**Parameters / Payload:**
None

**Response:**
```json
JSON object with keys: "status" (string) – "ok", "model_loaded" (boolean).
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – missing or malformed input parameters. |
| `500` | Internal Server Error – unexpected failure during prediction or training. |
| `404` | Not Found – requested endpoint does not exist. |


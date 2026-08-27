# Salary Predictor API Reference

**Base URL:** `http://<host>:<port>/api`  
**Authentication:** None – the API is publicly accessible within the deployment environment.

## Overview
The Salary Predictor provides a RESTful API to obtain salary predictions based on user-supplied job characteristics. The service is built with Flask, loads a pre‑trained Random Forest regression model (rf_regressor.pkl), and exposes a single prediction endpoint. It follows an API‑first monolithic architecture where the backend serves JSON responses to the frontend (index.html).

## Endpoints
### `POST` /predict
Returns a salary prediction for a single job posting based on the supplied feature payload.

**Parameters / Payload:**
JSON body with the following fields (all required unless noted):
- `years_experience` (float): Number of years of professional experience.
- `education_level` (string): One of `"High School"`, `"Bachelor"`, `"Master"`, `"PhD"`.
- `company_size` (string): One of `"Small"`, `"Medium"`, `"Large"`.
- `city` (string): City name where the job is located.
- `industry` (string): Industry sector (e.g., `"Technology"`, `"Finance"`).
- `position` (string): Job title (e.g., `"Data Scientist"`).
- `remote_ratio` (int, optional, default 0): Ratio of remote work (0, 50, 100).

**Response:**
```json
JSON object with the predicted salary (annual USD) and model metadata:
```json
{
  "predicted_salary": 112345.67,
  "model_version": "1.0",
  "confidence_interval": {
    "lower": 108000.00,
    "upper": 116700.00
  }
}
```
If the model does not provide a confidence interval, the field may be omitted.

```

---
### `GET` /health
Simple health‑check endpoint used by orchestration tools to verify that the Flask service is running and the model is loaded.

**Parameters / Payload:**
None.

**Response:**
```json
JSON payload indicating service status:
```json
{ "status": "ok", "model_loaded": true }
```
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `404` | Not Found – the requested route does not exist. |
| `405` | Method Not Allowed – HTTP method not supported for the endpoint. |


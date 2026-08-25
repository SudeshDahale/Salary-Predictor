# Salary Predictor API Reference

**Base URL:** `http://localhost:5000`  
**Authentication:** None

## Overview
The Salary Predictor API provides a single prediction endpoint that loads a pre‑trained RandomForestRegressor model and returns salary estimates for given job parameters. It runs on Flask and serves a static frontend for user interaction.

## Endpoints
### `POST` /predict
Predict salary based on input features such as job position, years of experience, and location.

**Parameters / Payload:**
JSON body with fields: position (string), years_experience (numeric), location (string, optional)

**Response:**
```json
JSON object containing predicted_salary (float) and model_version (string).
```

---
### `GET` /health
Health check endpoint to verify the API is running.

**Parameters / Payload:**


**Response:**
```json
JSON object with status: 'OK' and timestamp.
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – missing or malformed input data. |
| `500` | Internal Server Error – model loading or prediction failure. |


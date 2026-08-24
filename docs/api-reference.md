# Salary Predictor API Reference

**Base URL:** `http://localhost:5000`  
**Authentication:** None (public API)

## Overview
This document describes the Flask‑based REST API that powers the Salary Predictor application. The API loads a pre‑trained RandomForest regressor from the models directory and exposes endpoints for health checking, retrieving model metadata, and generating salary predictions based on user‑provided job attributes. All endpoints are unauthenticated and return JSON responses.

## Endpoints
### `GET` /health
Simple health‑check endpoint used by monitoring tools and the frontend to verify that the service is up and running.

**Parameters / Payload:**
None

**Response:**
```json
{ "status": "ok" }
```

---
### `GET` /metadata
Returns static metadata about the currently loaded model, such as version, training date, and the feature list used during training.

**Parameters / Payload:**
None

**Response:**
```json
{ "model_version": "1.0.0", "trained_on": "2023-08-15", "features": ["job_title","company","location","years_experience","education_level",... ] }
```

---
### `POST` /predict
Generates a salary forecast for a given job description. The request body must contain the feature values required by the model.

**Parameters / Payload:**
JSON object with the following keys (all required unless noted):
- job_title (string): Title of the position.
- company (string, optional): Name of the employer.
- location (string): Geographic location (city/state or country).
- years_experience (number): Total years of professional experience.
- education_level (string): Highest degree attained (e.g., "Bachelor", "Master", "PhD").
- other numeric/categorical features matching the training CSV columns.


**Response:**
```json
{ "predicted_salary": 84235.67, "model_version": "1.0.0", "input": { ...original request payload... } }
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – The JSON payload is missing required fields, contains invalid types, or fails validation. |
| `500` | Internal Server Error – An unexpected error occurred while loading the model or performing the prediction. |


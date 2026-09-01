# Salary‑Predicter API Reference

**Base URL:** `http://localhost:5000`  
**Authentication:** 

## Overview
The Salary-Predictor API provides endpoints for salary prediction using a pre‑trained Random Forest model and for retrieving model metadata. It is built with Flask and follows an API‑first monolithic architecture.

## Endpoints
### `POST` /predict
Predict salary based on job features

**Parameters / Payload:**
JSON body with keys: position (string), location (string), years_experience (float), education_level (string), company_size (string)

**Response:**
```json
JSON with fields: predicted_salary (float), model_version (string)
```

---
### `GET` /metadata
Retrieve model metadata

**Parameters / Payload:**
None

**Response:**
```json
JSON containing model_version, training_date, features, performance_metrics
```

---
### `GET` /health
Health check endpoint

**Parameters / Payload:**
None

**Response:**
```json
JSON with status: 'ok'
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request – missing or invalid input parameters |
| `500` | Internal Server Error – prediction failure or model loading error |


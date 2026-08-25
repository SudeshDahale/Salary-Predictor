# Salary Predictor    … … 

**Base URL:** `http://localhost:5000`  
**Authentication:** None

## Overview
API for      …  …  ... ... ...

## Endpoints
### `GET` /health
Get health status of the service

**Parameters / Payload:**
None

**Response:**
```json
JSON with status message
```

---
### `POST` /predict
Predict salary based on input features

**Parameters / Payload:**
JSON payload with required features (e.g., "years_experience", "education_level", "city")

**Response:**
```json
JSON with predicted salary
```

---


## Error Codes
| Code | Meaning |
| :--- | :--- |
| `400` | Bad Request: Missing or invalid input |
| `500` | None |


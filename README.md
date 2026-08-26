# Salary Predictor

Predict employee salaries using a trained RandomForest model via a Flask API and a simple web UI.

## Overview

The Salary Predictor project demonstrates an end‑to‑end machine‑learning workflow: a scikit‑learn RandomForest regressor is trained on the `Position_Salaries.csv` dataset, serialized, and served through a lightweight Flask API. A static HTML/JS front‑end consumes the `/predict` endpoint, allowing users to input job details and receive salary estimates in real time. The repository is organized as a monolithic code‑base with clear separation between the front‑end, back‑end, data, and model artefacts.

## Features

- Flask API (`backend/app.py`) exposing a `/predict` endpoint that returns JSON predictions.
- Training script (`backend/train_model.py`) to reproduce the RandomForest model and update `models/rf_regressor.pkl` and `models/metadata.json`.
- Pre‑trained RandomForest model (`models/rf_regressor.pkl`) with accompanying metadata for inference.
- Simple, responsive UI (`frontend/index.html`) built with HTML, CSS, and JavaScript that posts user input to the API.
- Jupyter notebook (`random_forest_regression.ipynb`) showing exploratory data analysis and model evaluation.

## Quick Start

```bash
```bash
# Clone the repository
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor

# Set up a virtual environment (optional but recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install back‑end dependencies
pip install -r backend/requirements.txt

# Run the Flask server (default runs on http://127.0.0.1:5000)
python backend/app.py
```

# In a separate terminal, open the UI
open frontend/index.html   # macOS
# or
xdg-open frontend/index.html   # Linux
# or simply open the file in any browser.
```
```

## Architecture

Monolith – API‑First: all components (data, model, Flask service, and static UI) live in a single repository. The Flask layer acts as the sole API surface, while the static front‑end consumes that API.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

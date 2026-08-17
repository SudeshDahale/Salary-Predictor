# Salary Predictor

A monolithic application for predicting salaries based on job position and experience.

## Overview

Salary Predictor is a Python-based application designed to estimate salary ranges for various job positions. Utilizing machine learning models, the application serves predictions through a user-friendly interface. The architecture is monolithic, where frontend, backend, data storage, and models are encapsulated within a single codebase, maintaining simplicity in development and deployment.

## Features

- Predict salaries based on user-inputted job position and experience level.
- Utilizes trained machine learning models for accurate predictions.
- Includes a user-friendly interface for seamless interaction.
- Supports CSV data import for model training and predictions.

## Quick Start

```bash
git clone https://github.com/SudeshDahale/Salary-Predictor.git
cd Salary-Predictor
pip install -r backend/requirements.txt
python backend/app.py
```

## Architecture

The Salary Predictor consists of a monolithic architecture where the frontend serves the user interface, while the backend handles application logic and model inference. The data module manages data storage for both training and making predictions, and the models module contains pre-trained models that are utilized by the backend for generating salary predictions.

---
*This file is kept in sync by [AutoScribe](https://github.com) — edits here may be overwritten on the next sync.*

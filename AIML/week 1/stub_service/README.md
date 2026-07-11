# Stub Service (Flask API)

## Overview

The Stub Service acts as the backend interface between the trained LightGBM forecasting model and the frontend application. It accepts a historical sales dataset in CSV format, performs input validation, generates the required forecasting features, loads the trained LightGBM model, and returns a 30-day sales forecast in JSON format.

---

# Objectives

- Provide a REST API for sales forecasting.
- Accept historical sales data through CSV upload.
- Validate the uploaded dataset before prediction.
- Generate a 30-day future sales forecast.
- Return forecast results in JSON format for frontend integration.

---

# Project Files

```
stub_service/
│
├── app.py
├── feature_engineering.py
├── lightgbm_daily_model.pkl
├── requirements.txt
└── README.md
```

---

# File Description

## app.py

The main Flask application responsible for:

- Initializing the Flask server.
- Loading the trained LightGBM model.
- Receiving uploaded CSV files.
- Validating the uploaded dataset.
- Performing recursive 30-day sales forecasting.
- Returning prediction results in JSON format.

---

## feature_engineering.py

This module contains reusable feature engineering functions used during model training.

The generated features include:

### Calendar Features

- Day
- Month
- Year
- Day of Week
- Week of Year
- Quarter

These features capture seasonal and calendar-based sales patterns.

---

## lightgbm_daily_model.pkl

Serialized LightGBM regression model generated after training.

The model is loaded using Joblib without retraining during API execution.

```
joblib.load("lightgbm_daily_model.pkl")
```

---

# API Endpoint

## Predict Sales

**Endpoint**

```
POST /predict
```

### Input

Multipart form-data

| Parameter | Type | Description |
|----------|------|-------------|
| file | CSV File | Historical sales dataset |

---

# Required Dataset Format

The uploaded CSV must contain the following columns.

| Column | Data Type |
|---------|-----------|
| Order Date | Date |
| Total amount | Numeric |

Example

| Order Date | Total amount |
|------------|-------------:|
| 2024-01-01 | 5400 |
| 2024-01-02 | 6200 |
| 2024-01-03 | 5800 |

---

# Input Validation

Before forecasting, the API validates the uploaded dataset.

Validation includes:

- Uploaded file exists.
- Required columns are present.
- Order Date contains valid dates.
- Total amount contains numeric values.
- Dataset contains at least 30 days of historical sales data.

If validation fails, the API returns an appropriate HTTP 400 response with an error message.

---

# Forecasting Workflow

```
Upload CSV
      │
      ▼
Read Dataset
      │
      ▼
Validate Input
      │
      ▼
Aggregate Historical Sales
      │
      ▼
Load LightGBM Model
      │
      ▼
Generate Calendar Features
      │
      ▼
Create Lag Features
      │
      ▼
Create Rolling Mean Features
      │
      ▼
Recursive 30-Day Forecast
      │
      ▼
Return JSON Response
```

---

# Recursive Forecasting

The forecasting process predicts one day at a time.

For each future day:

- Generate the next calendar date.
- Create calendar-based features.
- Compute lag features.
- Compute rolling mean features.
- Predict sales using the trained LightGBM model.
- Append the prediction to historical data.
- Repeat until 30 future days are generated.

This recursive approach enables forecasting beyond the available historical dataset.

---

# Output Format

The API returns predictions as JSON.

Example

```json
[
    {
        "Order Date": "2025-01-01",
        "Predicted Sales": 18452.63
    },
    {
        "Order Date": "2025-01-02",
        "Predicted Sales": 18973.41
    }
]
```

---

# Error Handling

The API returns descriptive error messages for invalid requests.

Examples include:

- Missing uploaded file
- Missing required columns
- Invalid Order Date values
- Invalid Total amount values
- Insufficient historical data

Example

```json
{
    "error": "Insufficient historical data.",
    "message": "At least 30 days of historical sales data are required to generate a 30-day forecast."
}
```

---

# Technologies Used

- Python
- Flask
- Pandas
- NumPy
- LightGBM
- Joblib

---

# Integration

The API is designed to integrate with the Flutter frontend.

Workflow

```
Flutter Application
        │
        ▼
Upload CSV
        │
        ▼
Flask API
        │
        ▼
LightGBM Model
        │
        ▼
30-Day Sales Forecast
        │
        ▼
JSON Response
        │
        ▼
Flutter User Interface
```

---

# Conclusion

The Stub Service provides a lightweight REST API for deploying the trained LightGBM forecasting model. It performs input validation, generates the required forecasting features, executes recursive forecasting for the next 30 days, and returns structured prediction results suitable for frontend integration.
# MarketMind AI - Sales Forecasting Module

## Overview

MarketMind AI is a sales forecasting module developed as part of the Small Business Sales Intelligence Platform internship project. The objective of this module is to analyze historical sales data, preprocess transaction records, build forecasting models, evaluate model performance, and expose the trained model through a Flask-based REST API for frontend integration.

The forecasting pipeline supports both daily and weekly sales prediction using the LightGBM regression algorithm. The trained model is deployed through a Flask API, enabling users to upload historical sales data and obtain a 30-day sales forecast.

---

# Project Objectives

- Perform Exploratory Data Analysis (EDA) on historical sales data.
- Build a reusable preprocessing pipeline.
- Generate daily and weekly aggregated datasets.
- Develop forecasting models using LightGBM.
- Evaluate forecasting performance using standard regression metrics.
- Deploy the trained model through a Flask REST API.
- Validate uploaded datasets before prediction.
- Generate recursive 30-day sales forecasts.

---

# Project Structure

```
AIML/
│
├── data/
│   ├── dataset.csv
│   ├── empty.csv
│   ├── inadequate_history_data.csv
│   ├── invalid_date_format.csv
│   ├── invalid_number_format.csv
│   └── ...
│
├── EDA/
│   ├── eda.ipynb
│   └── README.md
│
├── preprocessing/
│   ├── preprocessing.ipynb
│   ├── cleaned_dataset.csv
│   ├── daily_sales.csv
│   ├── weekly_sales.csv
│   └── README.md
│
├── forecasting_and_model_evaluation/
│   ├── lightGBM/
│   │   ├── forecasting_daily_lgbm.ipynb
│   │   ├── forecasting_weekly_lgbm.ipynb
│   │   ├── lightgbm_daily_model.pkl
│   │   ├── lightgbm_forecast.csv
│   │   ├── weekly_lightgbm_forecast.csv
│   │   └── README.md
│   │
│   └── prophet/
│       ├── forecasting.ipynb
│       ├── sales_forecast.csv
│       ├── model_evaluation.csv
│       └── README.md
│
├── stub_service/
│   ├── app.py
│   ├── feature_engineering.py
│   ├── lightgbm_daily_model.pkl
│   └── README.md
│
├── testing/
│
└── README.md
```

---

# Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- LightGBM
- Prophet
- Scikit-learn
- Flask
- Joblib

---

# Installation

## Clone Repository

```bash
git clone <repository-url>
```

Open the project folder.

```bash
cd AIML
```

---

## Create Virtual Environment (Optional)

Windows

```bash
python -m venv venv
```

Activate

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install pandas
pip install numpy
pip install matplotlib
pip install lightgbm
pip install prophet
pip install flask
pip install scikit-learn
pip install joblib
```

or

```bash
pip install -r requirements.txt
```

---

# Dataset Requirements

The uploaded CSV file must contain the following columns.

| Column | Data Type |
|----------|------------|
| Order Date | Date |
| Total amount | Numeric |

Example

| Order Date | Total amount |
|------------|-------------:|
| 2024-01-01 | 5600 |
| 2024-01-02 | 6200 |
| 2024-01-03 | 5800 |

---

# Running the Project

## Step 1 – Exploratory Data Analysis

Open

```
EDA/eda.ipynb
```

Run all notebook cells.

Outputs include

- Missing value analysis
- Duplicate detection
- Outlier analysis
- Correlation analysis
- Sales trend visualization

---

## Step 2 – Data Preprocessing

Open

```
preprocessing/preprocessing.ipynb
```

Run all notebook cells.

Outputs

- Cleaned dataset
- Daily sales dataset
- Weekly sales dataset

---

## Step 3 – Model Training

Daily Forecasting

```
forecasting_and_model_evaluation/lightGBM/forecasting_daily_lgbm.ipynb
```

Weekly Forecasting

```
forecasting_and_model_evaluation/lightGBM/forecasting_weekly_lgbm.ipynb
```

Outputs

- Trained LightGBM model
- MAE
- RMSE
- Actual vs Predicted visualization
- Prediction Error
- Feature Importance

---

## Step 4 – Start Flask API

Navigate to

```
stub_service
```

Run

```bash
python app.py
```

Server starts at

```
http://127.0.0.1:5000
```

---

# API Usage

## Forecast Endpoint

```
POST /predict
```

Input

Multipart Form Data

| Parameter | Description |
|------------|-------------|
| file | CSV file |

---

## Response

Example

```json
[
    {
        "Order Date":"2025-01-01",
        "Predicted Sales":18245.62
    },
    {
        "Order Date":"2025-01-02",
        "Predicted Sales":18492.30
    }
]
```

---

# Input Validation

The API validates the following conditions before prediction.

- CSV file uploaded
- Required columns present
- Valid Order Date values
- Numeric Total amount values
- Minimum 30 days of historical data

Invalid datasets return HTTP 400 responses with descriptive error messages.

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
Aggregate Daily Sales
      │
      ▼
Generate Features
      │
      ▼
Load LightGBM Model
      │
      ▼
Recursive 30-Day Forecast
      │
      ▼
Return JSON Response
```

---

# Model Evaluation

The forecasting models are evaluated using

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

Visualizations include

- Actual vs Predicted Sales
- Prediction Error
- Feature Importance

---

# Testing

The project includes test datasets for validating API behavior.

Test cases include

- Valid dataset
- Missing file
- Empty CSV
- Missing required column
- Invalid date format
- Invalid number format
- Insufficient historical data

Testing responses are available in the `testing` directory.

---

# Features

- Exploratory Data Analysis
- Data Cleaning
- Daily Sales Aggregation
- Weekly Sales Aggregation
- LightGBM Forecasting
- Prophet Forecasting
- Model Evaluation
- Recursive 30-Day Forecast
- REST API Deployment
- Input Validation
- JSON Response Generation

---

# Future Enhancements

- Hyperparameter tuning for LightGBM.
- Integration of holiday and promotional data.
- Automated model retraining.
- Comparison with foundation time-series models such as Amazon Chronos and Google TimesFM.
- Cloud deployment for production use.

---

# Conclusion

This project implements a complete machine learning workflow for sales forecasting, beginning with exploratory data analysis and preprocessing, followed by model training, evaluation, and deployment through a Flask REST API. The system validates user input, generates recursive 30-day forecasts using a trained LightGBM model, and provides structured JSON responses suitable for integration with frontend applications.
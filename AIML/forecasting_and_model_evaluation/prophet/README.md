# Sales Forecasting using Facebook Prophet

> **Milestone 1 – Day 4: Forecasting Prototype**

This project demonstrates a baseline sales forecasting model using **Facebook Prophet** to predict future daily sales trends from historical transaction data. The implementation focuses on preparing the dataset, analyzing seasonality, training a forecasting model, generating future predictions, and visualizing the results.

---

## Day 4 Objective

The objective of this task is to build a baseline sales forecasting model using Facebook Prophet. The model analyzes historical daily sales data to identify trends and seasonality, generates forecasts for the next 30 days, and establishes a strong foundation for model evaluation and advanced forecasting techniques in the next milestone.

---

## Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| Pandas | Data Processing and Analysis |
| Matplotlib | Data Visualization |
| Prophet | Time Series Forecasting |

---

## Dataset

The forecasting model uses the cleaned daily sales dataset generated during the preprocessing stage.

### Input Columns

| Column | Description |
|--------|-------------|
| Order Date | Date of transaction |
| Total amount | Daily sales |

Before training, the dataset is transformed into Prophet's required format.

| Original Column | Prophet Format |
|-----------------|----------------|
| Order Date | `ds` |
| Total amount | `y` |

---

## Workflow

### 1. Import Required Libraries

```python
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet
```

### 2. Load the Dataset

The cleaned daily sales dataset is loaded into the notebook.

```python
df = pd.read_csv(...)
```

### 3. Data Preparation

The dataset is prepared by:

- Renaming **Order Date** to `ds`
- Renaming **Total amount** to `y`
- Converting the date column into datetime format

This ensures compatibility with the Prophet forecasting model.

### 4. Seasonality Analysis

Both forecasting approaches were evaluated:

- Additive Seasonality
- Multiplicative Seasonality

The analysis indicated that **Multiplicative Seasonality** provides a better fit for the dataset, suggesting that seasonal variations increase as sales increase.

### 5. Model Training

The forecasting model is initialized as:

```python
Prophet(seasonality_mode="multiplicative")
```

The model automatically learns:

- Overall sales trend
- Weekly seasonality
- Yearly seasonality

### 6. Future Forecast Generation

Future dates are generated for the next **30 days**.

```python
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)
```

---

## Forecast Output

The generated forecast includes the following columns:

| Column | Description |
|--------|-------------|
| ds | Forecast date |
| yhat | Predicted sales |
| yhat_lower | Lower confidence interval |
| yhat_upper | Upper confidence interval |

These values provide both the predicted sales and the uncertainty associated with each prediction.

---

## Visualization

The notebook generates the following visualizations:

- Sales Forecast Plot
- Trend Analysis
- Weekly Seasonality
- Yearly Seasonality

These visualizations help interpret historical sales patterns and future forecasts.

---

## Output

The final forecast is exported as:

```text
sales_forecast.csv
```

The output file contains the predicted sales values and corresponding confidence intervals for each future date.

---

## Project Pipeline

```text
Raw Sales Data
      │
      ▼
Data Cleaning
      │
      ▼
Daily Sales Aggregation
      │
      ▼
Prepare Prophet Dataset (ds, y)
      │
      ▼
Seasonality Analysis
      │
      ▼
Train Prophet Model
      │
      ▼
Generate Future Dates
      │
      ▼
Predict Future Sales
      │
      ▼
Visualize Forecast
      │
      ▼
Export Forecast Results
```

---

## Key Features

- Baseline sales forecasting using Facebook Prophet
- Multiplicative seasonality detection
- 30-day future sales prediction
- Forecast confidence interval estimation
- Trend and seasonality visualization
- Exportable forecast results

---

## Future Improvements

The baseline forecasting model can be enhanced by integrating:

- XGBoost Regressor
- Random Forest Regressor
- ARIMA/SARIMA Models
- LSTM-based Forecasting
- Hyperparameter Optimization
- External factors such as holidays, promotions, and weather conditions

---

## Conclusion

A baseline sales forecasting model was successfully developed using **Facebook Prophet**. The workflow includes data preparation, seasonality analysis, model training, future prediction, visualization, and forecast export. This implementation provides a reliable foundation for evaluating forecasting performance and developing more advanced predictive models in future project milestones.



# Model Evaluation

> **Milestone 1 – Day 5**

## Overview

This notebook evaluates the baseline sales forecasting model developed using Facebook Prophet during Day 4. The objective is to measure the forecasting performance using standard evaluation metrics, identify the current model's limitations, and define the roadmap for improving forecasting accuracy in Milestone 2.

---

## Objective

The objectives of this task are to:

- Evaluate the baseline forecasting model.
- Measure prediction accuracy using MAE and RMSE.
- Compare predicted sales with historical sales.
- Identify the limitations of the baseline model.
- Define the roadmap for advanced forecasting models in Milestone 2.

---

## Evaluation Process

The evaluation follows the workflow below.

1. Generate predictions for the historical sales data.
2. Compare predicted values with actual sales.
3. Calculate evaluation metrics.
4. Visualize actual and predicted sales.
5. Export the evaluation results.
6. Document model limitations.
7. Define the Milestone 2 forecasting roadmap.

---

## Evaluation Metrics

The baseline model was evaluated using the following metrics.

| Metric | Purpose |
|---------|---------|
| Mean Absolute Error (MAE) | Measures the average absolute difference between actual and predicted sales. |
| Root Mean Squared Error (RMSE) | Measures prediction error while assigning greater penalty to larger deviations. |
| Mean Absolute Percentage Error (MAPE) | Provides the prediction error as a percentage of the actual sales values. |

---

## Results

| Metric | Value |
|---------|-------:|
| Mean Absolute Error (MAE) | 3132.43 |
| Root Mean Squared Error (RMSE) | 4123.88 |
| Mean Absolute Percentage Error (MAPE) | 166.76% |

---

## Actual vs Predicted Comparison

The historical sales values were compared against the corresponding predictions generated by the Prophet model. A line plot was created to visualize the forecasting performance and identify deviations between actual and predicted sales.

---

## Output

The evaluation results are exported as:

```text
model_evaluation.csv
```

The exported file contains:

- Date
- Actual Sales
- Predicted Sales

---

## Limitations

The baseline Prophet model has the following limitations:

- Forecasting accuracy is limited for the current dataset.
- The model relies only on historical sales information.
- External factors such as promotions, holidays, discounts and business events are not included.
- Significant day-to-day fluctuations are not captured effectively.
- The model serves as a baseline prototype for future improvements.

---

## Milestone 2 Roadmap

To improve forecasting accuracy, the following models will be explored during Milestone 2:

| Model | Purpose |
|--------|---------|
| XGBoost Regressor | Capture nonlinear relationships using engineered time-series features. |
| Random Forest Regressor | Improve prediction robustness through ensemble learning. |

Future work will also include feature engineering, hyperparameter tuning, and the incorporation of external business variables to improve forecasting performance.

---

## Deliverables

- Model evaluation notebook
- MAE, RMSE and MAPE calculations
- Actual vs Predicted visualization
- `model_evaluation.csv`
- Evaluation report
- Milestone 2 forecasting roadmap

---

## Conclusion

The baseline forecasting model was evaluated using standard regression metrics. The evaluation established a performance benchmark for the current implementation and identified opportunities for improvement. Based on the observed prediction errors, more advanced machine learning models such as XGBoost and Random Forest have been identified for implementation during Milestone 2, in accordance with the project roadmap. 1
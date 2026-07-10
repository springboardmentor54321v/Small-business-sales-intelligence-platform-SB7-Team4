# Day 2-Exploratory Data Analysis (EDA)

## Project
**MarketMind AI – Small Business Sales Intelligence Platform**

## AIML Module
**Forecasting & Time Series Analysis**

---

# Overview

This notebook performs **Exploratory Data Analysis (EDA)** on the Global Superstore sales dataset. The objective is to understand the dataset, assess its quality, perform preprocessing, identify trends and relationships, and prepare the data for the Sales Forecasting model.

The analysis includes:
- Dataset exploration
- Data preprocessing
- Missing value analysis
- Duplicate record analysis
- Data type conversion
- Statistical analysis
- Sales trend visualization
- Seasonality analysis
- Category-wise sales analysis
- Market-wise sales analysis
- Correlation analysis
- Outlier detection

---

# Dataset Information

**Dataset:** Global Superstore Dataset

The dataset contains historical sales transactions with customer, product, shipping, and sales information.

### Important Features Used

| Feature | Description |
|----------|-------------|
| Order Date | Date of transaction |
| Ship Date | Shipping date |
| Category | Product category |
| Quantity | Quantity purchased |
| Discount | Discount applied |
| Sales / Total Amount | Total transaction amount |
| unit_price | Unit price of the product |
| Market | Sales market |

---

# Libraries Used

- Pandas
- NumPy
- Matplotlib

---

# Data Preprocessing

The following preprocessing steps were performed before analysis:

## 1. Data Loading

The dataset was loaded using Pandas.

```python
df = pd.read_csv("../data/dataset.csv")
```

---

## 2. Dataset Inspection

The following methods were used to understand the structure of the dataset:

- `head()`
- `shape`
- `info()`
- `describe(include='all')`

These functions helped identify:

- Number of records
- Number of features
- Data types
- Statistical summary

---

## 3. Data Type Conversion

The following columns were converted into **Datetime** format.

- Order Date
- Ship Date

```python
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])
```

This conversion enables time-series analysis and feature extraction.

---

## 4. Missing Value Analysis

Missing values were identified using

```python
df.isnull().sum()
```

Observations:

- Most columns contained no missing values.
- Postal Code contained a significant number of missing values.

Since Postal Code is not required for forecasting, it was excluded from further analysis.

---

## 5. Duplicate Record Analysis

Duplicate records were checked using

```python
df.duplicated().sum()
```

Any duplicate transactions were removed before analysis.

---

# Statistical Analysis

Statistical measures were calculated using

```python
df.describe(include="all")
```

The analysis includes:

- Count
- Mean
- Standard Deviation
- Minimum
- Maximum
- Percentiles

for all numerical features.

---

# Exploratory Data Analysis

## 1. Sales Trend Over Time

Daily sales were aggregated based on **Order Date**.

Purpose:

- Understand overall business growth.
- Identify fluctuations in sales.
- Observe long-term sales trends.

Visualization:

- Line Chart

---

## 2. Monthly Seasonality

Monthly sales were analyzed to identify recurring sales patterns.

Purpose:

- Detect seasonal behaviour.
- Identify high-sales months.
- Support forecasting.

Visualization:

- Bar Chart

---

## 3. Weekly Seasonality

Sales were grouped by weekdays.

Purpose:

- Compare weekday and weekend sales.
- Identify busiest sales days.

Visualization:

- Bar Chart

---

## 4. Category-wise Sales Analysis

Sales were grouped according to product category.

Purpose:

- Identify best-performing categories.
- Compare product category performance.

Visualization:

- Bar Chart

---

## 5. Market-wise Sales Analysis

Sales were grouped by market.

Purpose:

- Compare regional performance.
- Identify markets with highest revenue.

Visualization:

- Bar Chart

---

## 6. Outlier Detection

A Box Plot was used to detect unusual transaction values.

Purpose:

- Detect extremely high or low sales.
- Identify potential data anomalies.

Visualization:

- Box Plot

---

## 7. Distribution Analysis

Histogram of Total Amount.

Purpose:

- Understand data distribution.
- Observe skewness.
- Detect concentration of sales values.

Visualization:

- Histogram

---

## 8. Correlation Analysis

Correlation was calculated among:

- Quantity
- unit_price
- Discount
- Total Amount

```python
corr = df[["Quantity","unit_price","Discount","Total amount"]].corr()
```

A Heatmap was generated to visualize relationships between numerical features.

Purpose:

- Measure linear relationships.
- Identify highly correlated variables.
- Understand the influence of sales-related attributes.

Visualization:

- Correlation Heatmap

---

# Key Findings

- Successfully loaded and explored the Global Superstore dataset.
- Converted **Order Date** and **Ship Date** into datetime format.
- Verified dataset structure and feature types.
- Performed descriptive statistical analysis.
- Reviewed missing values and duplicate records.
- Analyzed daily sales trends.
- Studied monthly and weekly seasonality.
- Compared sales across product categories.
- Compared sales across different markets.
- Detected outliers using Box Plot.
- Evaluated feature relationships using a Correlation Heatmap.

---

# Conclusion

The dataset was successfully explored and preprocessed for machine learning.

The EDA process provided insights into:

- Sales trends
- Seasonal patterns
- Product performance
- Market performance
- Feature relationships
- Data quality

# Day 3-Data Preprocessing Pipeline

## Project

**MarketMind AI – Small Business Sales Intelligence Platform**

## Module

**Forecasting & Time Series Analysis**

---

# Objective

The objective of this preprocessing pipeline is to transform the raw sales dataset into a clean and structured dataset suitable for time series forecasting.

The preprocessing script performs data cleaning, feature engineering, and sales aggregation so that the dataset can be directly used for machine learning models.

---

# Workflow

```
Raw Dataset
      │
      ▼
Data Inspection
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Sales Aggregation
      │
      ▼
Cleaned Dataset
```

---

# Dataset Loading

The dataset is loaded into a Pandas DataFrame.

```python
df = pd.read_excel("dataset.xlsx")
```

---

# Data Cleaning

## Date Conversion

The following columns are converted into datetime format.

- Order Date
- Ship Date

This enables time-based analysis and feature extraction.

---

## Missing Value Handling

Missing values are identified using

```python
df.isnull().sum()
```

The Postal Code column contains a large number of missing values and is not required for forecasting.

Therefore, it is removed from the dataset.

---

## Duplicate Removal

Duplicate records are identified using

```python
df.duplicated().sum()
```

Any duplicate rows are removed before further processing.

---

# Feature Engineering

Several date-based features are created from the Order Date column.

## Day

Extracts the day of the month.

Example

```
15
27
31
```

---

## Week

Extracts the ISO week number.

Example

```
Week 1
Week 12
Week 40
```

---

## Month

Extracts the month number.

Example

```
1
5
10
```

---

## Month Name

Extracts the complete month name.

Example

```
January
February
March
```

---

## Year

Extracts the year.

Example

```
2021
2022
```

---

## Day Name

Extracts the weekday.

Example

```
Monday
Wednesday
Friday
```

---

## Quarter

Creates quarterly information.

Example

```
Q1
Q2
Q3
Q4
```

---

## Season

A custom season feature is created based on the month.

Season mapping:

| Months | Season |
|---------|---------|
| Dec–Feb | Winter |
| Mar–May | Summer |
| Jun–Aug | Monsoon |
| Sep–Nov | Autumn |

This feature helps the forecasting model capture seasonal sales patterns.

---

# Sales Aggregation

## Daily Sales

Sales are aggregated by Order Date.

This converts multiple transactions occurring on the same day into a single daily sales value.

Output:

| Order Date | Total Amount |
|------------|--------------|
|2021-01-01|25000|

---

## Weekly Sales

Sales are aggregated using Year and Week.

Output:

| Year | Week | Total Amount |
|------|------|--------------|
|2021|1|180000|

Weekly aggregation is useful for medium-term forecasting and trend analysis.

---

# Output Files

The preprocessing pipeline generates the following files.

## cleaned_dataset.csv

Contains:

- Cleaned data
- Converted date columns
- Newly created date features
- Duplicate-free records

---

## daily_sales.csv

Contains daily aggregated sales.

Used for daily forecasting.

---

## weekly_sales.csv

Contains weekly aggregated sales.

Used for weekly forecasting.

---

# Deliverables

- Cleaned dataset
- Daily sales dataset
- Weekly sales dataset
- Reusable preprocessing pipeline

---

# Conclusion

The preprocessing pipeline converts raw transactional data into a structured format suitable for machine learning.

The processed dataset is now ready for:

- Exploratory Data Analysis
- Feature Engineering
- Time Series Forecasting
- Model Training

# Day 4, Part-1 Sales Forecasting using Facebook Prophet

> **Milestone 1 – Day 4: Forecasting Prototype**

This project demonstrates a baseline sales forecasting model using **Facebook Prophet** to predict future daily sales trends from historical transaction data. The implementation focuses on preparing the dataset, analyzing seasonality, training a forecasting model, generating future predictions, and visualizing the results.

---

## Day 4, Part-1 Objective

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



# Day 5,Part-1 Model Evaluation of the Prophet Model

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

## Deliverables

- Model evaluation notebook
- MAE, RMSE and MAPE calculations
- Actual vs Predicted visualization
- `model_evaluation.csv`
- Evaluation report

---

## Conclusion

The baseline forecasting model was evaluated using standard regression metrics. The evaluation established a performance benchmark for the current implementation and identified opportunities for improvement. Based on the observed prediction errors, more advanced machine learning models such as XGBoost and Random Forest have been identified for implementation during Milestone 2, in accordance with the project roadmap. 

# Day 4, Part-2 Baseline Sales Forecasting Prototype Using LightGBM

## Objective

The objective of Day 4 was to develop a baseline sales forecasting model using the cleaned sales dataset generated during the preprocessing stage. As specified in the Milestone 1 SRS, the forecasting prototype serves as the initial AI module for predicting future sales trends before integrating more advanced forecasting techniques in future milestones.

---

## Dataset

The forecasting model was developed using the preprocessed sales dataset generated during Day 3.

Datasets Used:

- `daily_sales.csv`
- `weekly_sales.csv`

Target Variable:

- `Total amount`

---

# Daily Sales Forecasting

## Model

LightGBM Regressor

## Data Preparation

The following preprocessing steps were applied before training the model:

- Converted `Order Date` to datetime format.
- Sorted the dataset chronologically.
- Created calendar-based features:
  - Day
  - Month
  - Year
  - Day of Week
  - Week of Year
  - Quarter
- Generated lag features:
  - Lag 1
  - Lag 7
  - Lag 30
- Generated rolling average features:
  - 7-day rolling mean
  - 30-day rolling mean
- Removed rows containing missing values created by lag and rolling operations.

---

## Training Procedure

- Train/Test Split
  - Training data: All observations except the last 30 days
  - Testing data: Final 30 days

Model:

- LightGBM Regressor

Training Parameters:

- n_estimators = 500
- learning_rate = 0.05
- max_depth = 8
- num_leaves = 31
- random_state = 42

---

## Forecast Output

The model generated predictions for the final 30 days of the dataset.

Outputs generated:

- Forecast values
- Actual vs Predicted visualization
- Feature importance analysis
- Forecast CSV file

---

# Weekly Sales Forecasting

## Model

LightGBM Regressor

## Data Preparation

The daily sales data was aggregated into weekly sales totals.

Feature engineering included:

- Year
- Week Number
- Week cyclical encoding
- Lag features
- Rolling statistics
- Expanding mean

Rows containing missing values were removed before model training.

---

## Training Procedure

- Training set: All weeks except the final 8 weeks
- Test set: Last 8 weeks

Model:

- LightGBM Regressor

Training Parameters:

- n_estimators = 800
- learning_rate = 0.03
- max_depth = 6
- num_leaves = 31
- subsample = 0.9
- colsample_bytree = 0.9

---

## Forecast Output

Generated outputs include:

- Weekly sales predictions
- Actual vs Predicted comparison graph
- Feature importance
- Weekly forecast CSV

---

## Deliverables

- Forecasting Notebook
- Daily Forecast CSV
- Weekly Forecast CSV
- Forecast Visualization
- Feature Importance Analysis

---

## Conclusion

Two baseline forecasting approaches were implemented using LightGBM.

The daily forecasting model captures short-term sales behaviour, whereas the weekly forecasting model reduces daily fluctuations by aggregating observations into weekly totals. Both models establish the forecasting baseline required for subsequent model evaluation.



# Day 5, Part-2 Model Evaluation of the LightGBM

## Objective

The objective of Day 5 was to evaluate the performance of the baseline forecasting models developed on Day 4 using standard regression metrics and compare forecasting performance across different aggregation levels.

---

# Evaluation Metrics

The following evaluation metrics were used:

## Mean Absolute Error (MAE)

Measures the average absolute difference between actual and predicted sales.

Lower values indicate better prediction accuracy.

---

## Root Mean Squared Error (RMSE)

Measures prediction error while assigning higher penalties to larger errors.

Lower RMSE indicates improved forecasting performance.

---

## Mean Absolute Percentage Error (MAPE)

Measures prediction accuracy as a percentage.

A lower MAPE indicates better forecasting performance.

---

# Daily Forecast Evaluation

## Model

LightGBM Regressor

### Performance

| Metric | Value |
|----------|---------|
| MAE | 3934.34 |
| RMSE | 5325.62 |
| MAPE | 38.57% |

### Observations

- The model successfully learned general sales patterns.
- Daily sales exhibited significant volatility.
- Sharp spikes and sudden drops reduced forecasting accuracy.
- Calendar and lag-based features improved learning but could not fully capture irregular daily behaviour.

---

# Weekly Forecast Evaluation

## Model

LightGBM Regressor

### Performance

| Metric | Value |
|----------|---------|
| MAE | 28925.79 |
| RMSE | 35751.13 |
| MAPE | 21.58% |

### Observations

- Weekly aggregation reduced day-to-day fluctuations.
- The model produced smoother forecasts.
- Weekly predictions aligned more closely with overall sales trends.
- Weekly forecasting achieved lower percentage error than daily forecasting.

---

# Comparative Analysis

| Metric | Daily Forecast | Weekly Forecast |
|----------|---------------|----------------|
| MAE | 3934.34 | 28925.79 |
| RMSE | 5325.62 | 35751.13 |
| MAPE | 38.57% | 21.58% |

Although the weekly model produced higher MAE and RMSE values due to larger weekly sales totals, it achieved a substantially lower MAPE, indicating better relative forecasting performance.

---

# Limitations

The following limitations were identified during evaluation:

- The dataset contains highly irregular sales patterns.
- Daily sales exhibit significant variability.
- Forecasting was performed using aggregated sales values without additional explanatory variables such as product category, discounts, customer behaviour or promotions.
- Large sales spikes remain difficult to predict using only historical sales values.

---

# Future Improvements

Future milestones may include:

- XGBoost
- Random Forest
- Advanced LightGBM tuning
- Transformer-based forecasting models
- Hyperparameter optimization
- Incorporating additional business features
- Time-series cross-validation

---

## Deliverables

- Model Evaluation Report
- Forecast Comparison
- Performance Metrics
- Visualization of Actual vs Predicted Sales

---

## Conclusion

The baseline forecasting models were successfully evaluated using MAE, RMSE and MAPE.

Among the evaluated approaches, weekly forecasting demonstrated better relative prediction accuracy by reducing the effect of daily sales fluctuations. The evaluation establishes a benchmark for future forecasting models planned in subsequent milestones.
# Day 4 - Baseline Sales Forecasting Prototype

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



# Day 5 - Model Evaluation

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
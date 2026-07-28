# Day 2 – Advanced Forecasting Models

## Objective

To improve the baseline sales forecasting model by implementing and comparing multiple machine learning algorithms using the preprocessed daily sales dataset.

---

## Dataset

Input Dataset:

- daily_sales.csv

The dataset was generated during the preprocessing stage by cleaning the raw transactional data and aggregating sales on a daily basis.

---

## Feature Engineering

The following features were created to improve forecasting performance:

- Day
- Month
- Year
- Day of Week
- Week of Year
- Quarter
- Lag 1
- Lag 7
- Lag 30
- Rolling Mean (7 Days)
- Rolling Mean (30 Days)

These features help the model learn seasonality, historical trends and recent sales behaviour.

---

## Models Implemented

The following forecasting models were developed and evaluated:

- LightGBM
- XGBoost
- Random Forest
- CatBoost

Each model was trained using the same processed dataset to ensure a fair comparison.

---

## Model Evaluation

The models were evaluated using:

- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

These metrics measure the prediction error and overall forecasting performance.

---

## Deliverables

- Forecasting notebooks
- Trained forecasting models
- Model evaluation results
- Performance comparison between multiple algorithms

---

## Outcome

Multiple machine learning models were successfully implemented and evaluated to identify the most suitable forecasting model for deployment.

# Day 3 – Model Selection and Forecast API Integration

## Objective

To identify the best-performing forecasting model and integrate it into the Flask Forecast API.

---

## Work Completed

### Model Comparison

The forecasting models were compared using MAE and RMSE.

Models compared:

- LightGBM
- XGBoost
- Random Forest
- CatBoost

---

### Final Model Selection

CatBoost was selected as the final forecasting model because it achieved the best overall forecasting performance and provided the lowest Mean Absolute Error among the evaluated models.

---

### Model Saving

The trained CatBoost model was saved as:

catboost_daily_model.pkl

This model is loaded by the Forecast API during prediction.

---

## Forecast API

The Forecast API was updated to:

- Accept CSV file uploads
- Validate uploaded files
- Verify required columns
- Automatically parse dates
- Handle invalid records
- Generate the next 30-day sales forecast
- Return prediction results in JSON format

---

## Testing

The Forecast API was successfully tested using Postman.

Input:

- daily_sales.csv

Output:

- Next 30 days predicted sales

---

## Deliverables

- CatBoost forecasting model
- Saved model (.pkl)
- Updated Flask Forecast API
- Working prediction endpoint

---

## Outcome

The forecasting pipeline was successfully integrated with the API, enabling automated future sales prediction.


# Day 4 – Forecast API Enhancement

## Objective

Enhance the Forecast API by improving the prediction response and providing users with a simple confidence indicator for the generated forecasts.

---

## Work Completed

### Forecast API Enhancement

The existing Forecast API was enhanced by updating the response returned to the user.

The API now provides:

- Forecast date
- Predicted sales
- Model confidence indicator

---

### Model Confidence

A simple confidence indicator was added to the API response to communicate the overall reliability of the forecasting model.

The confidence level is derived from the evaluation performance of the selected forecasting model.

Current Confidence Level:

- **High**

This indicates that the deployed CatBoost model demonstrated strong performance during evaluation and was selected as the production forecasting model.

---

## Sample API Response

```json
{
    "Order Date": "2015-01-01",
    "Predicted Sales": 749.45,
    "Model Confidence": "High"
}
```

---

## API Improvements

The enhanced Forecast API now:

- Accepts historical sales data as input
- Generates a 30-day sales forecast
- Returns predictions in JSON format
- Includes a model confidence indicator with every prediction

---

## Deliverables

- Updated Forecast API
- Enhanced JSON response
- Model confidence indicator
- Successfully tested API using Postman

---

## Outcome

The Forecast API was enhanced to provide not only future sales predictions but also a simple indication of the forecasting model's reliability, making the response more informative and user-friendly.
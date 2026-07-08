# Day 2: Exploratory Data Analysis (EDA) Documentation

## 1. Project Overview

- **Project Name:** MarketMind AI
- **Module:** Forecasting & Time Series Analysis
- **Tools Used:** `pandas`, `numpy`, `matplotlib.pyplot`

## 2. Dataset Characteristics

- **Source:** `marketmind_sales_dataset.csv`
- **Shape:** **200 rows × 13 columns**
- **Memory Usage:** ~32.5 KB

### Features
```text
transaction_id
invoice_id
transaction_date
customer_id
product_id
product_name
category
quantity
unit_price
discount
total_amount
payment_method
store_id
```

## 3. Data Cleaning & Preprocessing

### Data Type Conversion
- Converted `transaction_date` to `datetime`.
- Converted `unit_price` to numeric.

### Missing Value Handling
- Numeric columns (`quantity`, `unit_price`, `discount`, `total_amount`) → filled with **median**.
- Categorical columns → filled with **mode**.
- `transaction_date` missing values → filled with the median date.

### Duplicate Check
- **Duplicates Found:** `0`

## 4. Descriptive Statistics

### Categorical Insights
- Most purchased product: **Bread Loaf**
- Top category: **Grocery**
- Most common payment method: **Card**
- Most frequent store: **S002**

### Numeric Insights
- Average quantity: **9.4**
- Maximum quantity: **1000**
- Average `total_amount`: **1054.64**
- Maximum `total_amount`: **99999.0**

> Negative values in `quantity`, `unit_price`, and `discount` may represent refunds, data-entry issues, or accounting adjustments.

## 5. Exploratory Visualizations

- Sales Trend Over Time
- Monthly Seasonality
- Weekly Seasonality
- Category-wise Sales
- Payment Method Distribution
- Outlier Detection using Boxplot
- Correlation Matrix & Heatmap

### Correlation Summary
The strongest positive correlation observed was between **`unit_price`** and **`total_amount`** (≈ **0.14**), indicating an overall weak linear relationship among numeric variables.

---
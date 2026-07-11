# Exploratory Data Analysis (EDA)

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

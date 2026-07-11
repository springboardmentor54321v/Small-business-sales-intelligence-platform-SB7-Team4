# Data Preprocessing Pipeline

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

# API Testing Report

## Overview

This document summarizes the testing performed on the Flask-based sales forecasting API. The objective of testing was to verify that the API correctly validates user input, handles invalid requests, and generates forecasts only when valid historical data is provided.

---

# Test Environment

| Component | Description |
|-----------|-------------|
| Backend Framework | Flask |
| Programming Language | Python |
| API Testing Tool | Postman |
| Forecasting Model | LightGBM |
| Response Format | JSON |

---

# Test Cases

## Test Case 1 – Valid CSV Input

### Objective

Verify that the API accepts a valid CSV file and generates a 30-day sales forecast.

### Input

- CSV containing:
  - Order Date
  - Total amount
- Valid dates
- Numeric sales values
- At least 30 days of historical data

### Expected Result

- API successfully processes the dataset.
- Returns a JSON response containing the next 30 days of predicted sales.

### Status

**Pass**

---

## Test Case 2 – Missing File

### Objective

Verify that the API handles requests without an uploaded CSV file.

### Input

No file uploaded.

### Expected Result

The API returns an error indicating that no file was provided.

### Status

**Pass**

---

## Test Case 3 – Empty CSV File

### Objective

Verify that the API detects an empty CSV file.

### Input

CSV file containing headers but no data.

### Expected Result

The API returns an appropriate validation error.

### Status

**Pass**

---

## Test Case 4 – Missing Required Column

### Objective

Verify that the API validates the presence of required columns.

### Input

CSV without the **Total amount** column.

### Expected Result

The API returns an error indicating that the required column is missing.

### Status

**Pass**

---

## Test Case 5 – Invalid Date Format

### Objective

Verify that invalid values in the **Order Date** column are detected.

### Input

CSV containing invalid date values such as:

```
abc
invalid_date
2024-13-10
```

### Expected Result

The API returns an error indicating an invalid date format.

### Status

**Pass**

---

## Test Case 6 – Invalid Number Format

### Objective

Verify that non-numeric values in the **Total amount** column are rejected.

### Input

CSV containing values such as:

```
abc
xyz
₹5000
```

### Expected Result

The API returns an error indicating an invalid number format.

### Status

**Pass**

---

## Test Case 7 – Insufficient Historical Data

### Objective

Verify that the API requires sufficient historical data before forecasting.

### Input

CSV containing fewer than 30 days of historical sales.

### Expected Result

The API returns an error indicating that at least 30 days of historical data are required.

### Status

**Pass**

---

# Validation Performed

The API validates the following conditions before forecasting:

- CSV file is uploaded.
- Required columns are present.
- Order Date contains valid date values.
- Total amount contains numeric values.
- Dataset contains at least 30 days of historical data.

Only datasets that satisfy all validation checks are processed by the forecasting model.

---

# Forecast Verification

For a valid dataset, the API performs the following sequence:

1. Reads the uploaded CSV.
2. Validates the dataset.
3. Loads the trained LightGBM model.
4. Generates forecasting features.
5. Performs recursive forecasting.
6. Predicts sales for the next 30 days.
7. Returns the forecast in JSON format.

---

# Testing Summary

| Test Case | Result |
|-----------|--------|
| Valid CSV Upload | Pass |
| Missing File | Pass |
| Empty CSV | Pass |
| Missing Required Column | Pass |
| Invalid Date Format | Pass |
| Invalid Number Format | Pass |
| Insufficient Historical Data | Pass |

---

# Conclusion

The API successfully handled both valid and invalid input scenarios. All validation checks operated as expected, preventing invalid datasets from reaching the forecasting stage. For valid historical sales data, the API generated a 30-day sales forecast and returned the predictions in JSON format, demonstrating successful integration between the Flask backend and the trained LightGBM forecasting model.
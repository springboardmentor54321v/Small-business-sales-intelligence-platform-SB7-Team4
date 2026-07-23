# Day 9 - Anomaly Detection API

## Objective

Develop a Flask API to provide anomaly detection results based on the order date.

---

## Input File

- anomaly_detection_results.csv

Required Columns:

- Order Date
- Total amount
- Anomaly

---

## API Endpoint

### GET /

Checks whether the API is running.

**Response**

```json
{
    "message": "Anomaly Detection API is running.",
    "endpoint": "/check-anomaly"
}
```

---

### POST /check-anomaly

Returns anomaly information for a given order date.

**Request**

```json
{
    "Order Date": "2011-01-03"
}
```

**Successful Response**

```json
{
    "Order Date": "2011-01-03",
    "Total Sales": 1234.56,
    "Anomaly": false
}
```

---

## Validation

### 1. No JSON Data

**Response**

```json
{
    "error": "No JSON data received."
}
```

---

### 2. Missing Order Date

**Request**

```json
{}
```

**Response**

```json
{
    "error": "Order Date is required."
}
```

---

### 3. Invalid Order Date

**Request**

```json
{
    "Order Date": "2030-01-01"
}
```

**Response**

```json
{
    "error": "Order Date not found."
}
```

---

## Workflow

1. Load `anomaly_detection_results.csv`.
2. Start the Flask application.
3. Accept JSON input from the client.
4. Validate the request.
5. Search the dataset using the provided order date.
6. Return the total sales and anomaly status if found.
7. Return appropriate error messages for invalid requests.

---

## Technologies Used

- Python
- Flask
- Pandas

---

## Conclusion

A REST API was developed using Flask to retrieve anomaly detection results based on the order date. The API validates incoming requests, returns anomaly information for valid dates, and provides meaningful error messages for invalid or incomplete requests.
# Churn Risk API

## Objective

Develop a Flask API that returns the churn risk of a customer based on the churn analysis performed in Day 4.

---

## Implementation

### 1. Load Churn Dataset

- Loaded `customer_churn.csv` using Pandas.
- The dataset contains the churn risk assigned to each customer.

### 2. Flask Application

Created a Flask application to provide churn risk information through REST APIs.

### 3. API Endpoints

#### GET /

Checks whether the API is running.

**Response**

```json
{
    "message": "Customer Churn Risk API is running.",
    "endpoint": "/churn-risk"
}
```

---

#### POST /churn-risk

Accepts a Customer ID and returns the corresponding churn risk.

**Request**

```json
{
    "Customer ID": "AA-10315"
}
```

**Response**

```json
{
    "Customer ID": "AA-10315",
    "Risk": "Low Risk"
}
```

---

## Input Validation

The API performs the following validations:

### 1. No JSON Data

Returns an error if no JSON request body is provided.

**Response**

```json
{
    "error": "No JSON data received."
}
```

Status Code: **400 Bad Request**

---

### 2. Missing Customer ID

Returns an error if the `Customer ID` field is not included in the request.

**Request**

```json
{}
```

**Response**

```json
{
    "error": "Customer ID is required."
}
```

Status Code: **400 Bad Request**

---

### 3. Customer Not Found

Returns an error if the provided Customer ID does not exist in the dataset.

**Request**

```json
{
    "Customer ID": "XYZ123"
}
```

**Response**

```json
{
    "error": "Customer ID not found."
}
```

Status Code: **404 Not Found**

---

## Testing

The API was tested using Postman.

### Endpoint

```
POST http://127.0.0.1:5000/churn-risk
```

### Sample Request

```json
{
    "Customer ID": "AA-10315"
}
```

### Sample Response

```json
{
    "Customer ID": "AA-10315",
    "Risk": "Low Risk"
}
```

---

## Technologies Used

- Python
- Flask
- Pandas
- Postman

---

## Output

The API accepts a Customer ID as input, validates the request, retrieves the customer's churn risk from the dataset, and returns the result in JSON format.
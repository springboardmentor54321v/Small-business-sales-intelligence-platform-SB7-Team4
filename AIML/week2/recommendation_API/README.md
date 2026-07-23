# Product Recommendation API

## Objective

Develop a Flask API that provides product recommendations based on products that are frequently purchased together.

---

## Implementation

### 1. Load Recommendation Data

- Loaded the `product_recommendations.csv` file using Pandas.
- Stored the recommendation data in a DataFrame for fast lookup.

### 2. Create Flask Application

- Created a Flask application.
- Added a home endpoint (`/`) to verify that the API is running.

### 3. Create Recommendation Endpoint

- Implemented a POST endpoint:

```
/recommend-product
```

- Accepts a product name as JSON input.

### 4. Input Validation

Implemented the following validations:

- Check if JSON data is received.
- Check whether the `Product Name` field is present.
- Return an error if the product is not available in the recommendation dataset.

### 5. Recommendation Logic

- Read each product pair from the recommendation dataset.
- Compared the input product with both products in every pair.
- Collected all matching products as recommendations.
- Returned the recommendation list as a JSON response.

### 6. Response Generation

Returned the following information:

- Input Product Name
- Recommended Products

---

## API Endpoints

### GET /

Returns the API status.

**Response**

```json
{
    "message": "Product Recommendation API is running.",
    "endpoint": "/recommend-product"
}
```

---

### POST /recommend-product

Returns products that are frequently purchased together.

**Request**

```json
{
    "Product Name": "Staples"
}
```

**Response**

```json
{
    "Product Name": "Staples",
    "Recommendations": [
        "Hon Olson Stacker Chairs",
        "Newell 34",
        "Satellite Sectional Post Binders"
    ]
}
```

---

## Validation

### No JSON Data

**Response**

```json
{
    "error": "No JSON data received."
}
```

---

### Missing Product Name

**Request**

```json
{}
```

**Response**

```json
{
    "error": "Product Name is required."
}
```

---

### Product Not Found

**Request**

```json
{
    "Product Name": "Unknown Product"
}
```

**Response**

```json
{
    "error": "Product not found."
}
```
---

## Libraries Used

- Flask
- Pandas
- OS

---

## Result

Successfully developed a Flask API that accepts a product name as input and returns products that are frequently purchased together. The API includes input validation and returns appropriate HTTP status codes and JSON responses for valid and invalid requests.
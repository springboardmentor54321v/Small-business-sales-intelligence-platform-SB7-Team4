# Churn Risk Detection

## Objective

Develop a simple churn risk detection system to identify customers who are likely to stop purchasing based on their purchase history.

---

## Dataset

The implementation uses the cleaned transaction dataset generated during the preprocessing stage.

Required columns:
- Customer ID
- Order Date
- Order ID
- Total amount

---

## Implementation

### 1. Data Loading

- Loaded the cleaned transaction dataset using Pandas.
- Converted the `Order Date` column to datetime format.

### 2. Feature Creation

Customer-level information was generated using the following features:

- Last Purchase Date
- Purchase Frequency
- Total Spending
- Days Since Last Purchase

### 3. Churn Risk Classification

Customers were classified into three categories using a rule-based approach.

| Days Since Last Purchase | Risk Level |
|---------------------------|------------|
| 0 - 90 days | Low Risk |
| 91 - 180 days | Medium Risk |
| More than 180 days | High Risk |

### 4. Visualization

A bar chart was created to display the distribution of customers across different churn risk categories.

### 5. Output

The final customer churn information was saved as:

- `customer_churn.csv`

---

## Technologies Used

- Python
- Pandas
- Matplotlib
- Jupyter Notebook

---

## Output

The notebook generates:

- Customer-level churn analysis
- Risk classification (Low, Medium, High)
- Churn risk distribution chart
- `customer_churn.csv` containing the final results
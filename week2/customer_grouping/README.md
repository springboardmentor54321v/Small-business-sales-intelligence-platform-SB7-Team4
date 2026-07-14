# Customer Segmentation using K-Means

## Objective

The objective of this task is to group customers into different segments based on their purchasing behavior. Customer segmentation helps businesses identify high-value, regular, and low-value customers, enabling targeted marketing strategies and improved customer relationship management.

---

## Dataset

**Source:** `cleaned_dataset.csv`

The cleaned dataset generated during the preprocessing stage was used as the input dataset.

### Features Used

- Customer ID
- Order ID
- Total amount

The following customer-level features were generated:

- **Total Spending** – Sum of all purchases made by a customer.
- **Purchase Frequency** – Total number of orders placed by a customer.
- **Average Order Value** – Average amount spent per order.

---

## Methodology

### 1. Data Loading

- Loaded the cleaned dataset using Pandas.
- Verified the dataset structure and available columns.

### 2. Customer Feature Engineering

Grouped the transaction data by **Customer ID** to generate customer-level features:

- Total Spending
- Purchase Frequency
- Average Order Value

### 3. Feature Scaling

Standardized the numerical features using **StandardScaler** to ensure equal contribution during clustering.

### 4. Optimal Cluster Selection

Applied the **Elbow Method** by calculating the Within-Cluster Sum of Squares (WCSS) for cluster values ranging from 1 to 10.

The elbow point indicated that **3 clusters** provided the best balance between model complexity and clustering performance.

### 5. Customer Segmentation

Applied the **K-Means Clustering** algorithm with:

- Number of Clusters: 3
- Random State: 42
- n_init: 10

Each customer was assigned to one of the three clusters.

### 6. Cluster Visualization

A scatter plot was generated using:

- X-axis: Total Spending
- Y-axis: Purchase Frequency

This visualization provides an overview of the distribution of customers across the identified clusters.

### 7. Model Saving

The trained K-Means model was saved for future use using Joblib.

---

## Outputs

The following files were generated:

| File | Description |
|------|-------------|
| `customer_grouping.ipynb` | Customer segmentation implementation |
| `customer_segments.csv` | Customer dataset with assigned cluster labels |
| `kmeans_customer_model.pkl` | Trained K-Means model |

---

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Scikit-learn
- Joblib

---

## Results

The K-Means model successfully segmented customers into three distinct groups based on their purchasing behavior. The generated customer segments can be used for customer profiling, personalized marketing, and business decision-making.

---

## Conclusion

Customer segmentation was successfully performed using the K-Means clustering algorithm. Customer-level features were generated from the transaction data, standardized, and clustered into three groups. The trained model and segmented customer dataset were saved for future integration into the sales intelligence platform.
# Product Recommendation

## Objective

Develop a product recommendation module that identifies products frequently purchased together using historical sales data.

---

## Implementation

### 1. Load Dataset

- Loaded the cleaned sales dataset using Pandas.
- Verified that the required columns (`Order ID` and `Product Name`) are available.

### 2. Group Products by Order

- Grouped products based on their Order ID.
- Converted each order into a list of purchased products.

### 3. Generate Product Pairs

- Removed duplicate products within each order.
- Generated all possible unique product pairs using combinations.

### 4. Count Product Pair Frequency

- Counted the occurrence of each product pair across all orders.
- Sorted the pairs in descending order based on frequency.

### 5. Display Results

- Displayed the top 10 most frequently purchased product pairs.
- Generated a bar chart to visualize the most common product combinations.

### 6. Save Output

- Saved the recommendation results to:

```
product_recommendations.csv
```

---

## Output Files

- `product_recommendations.csv`
- `product_recommendation.ipynb`

---

## Libraries Used

- pandas
- matplotlib
- itertools
- collections

---

## Result

The module successfully identified the top product pairs that customers frequently purchased together. The generated CSV file and visualization can be used for building recommendation APIs and supporting cross-selling features.
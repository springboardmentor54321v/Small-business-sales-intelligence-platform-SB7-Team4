# Day 7 – Recommendation Engine Improvement

## Overview

Day 7 focuses on improving the product recommendation engine developed in the previous milestone.

The Week 2 recommendation system suggested products based only on whether two products had ever been purchased together.

In Week 3, the recommendation engine was enhanced by considering the frequency with which products were purchased together. Recommendations are ranked according to their co-occurrence frequency, allowing customers to receive more relevant suggestions.

---

# Objective

The objectives of Day 7 are:

- Improve the existing recommendation engine.
- Rank recommendations based on purchase frequency.
- Return only the most relevant recommendations.
- Compare the Week 2 and Week 3 recommendation approaches.
- Integrate the improved recommendation engine into the Flask API.

---

# Dataset

The cleaned transaction dataset from previous milestones was reused.

## Dataset Information

| Property | Value |
|----------|------:|
| Total Transactions | 9,994 |
| Total Orders | 5,009 |
| Total Products | 1,841 |

No additional datasets were introduced.

---

# Methodology

## 1. Shopping Basket Creation

Transactions were grouped using **Order ID**.

Each order was converted into a shopping basket containing the list of purchased products.

Example:

```
Order 101

Laptop
Mouse
Keyboard
```

becomes

```
Order 101

[Laptop, Mouse, Keyboard]
```

---

## 2. Product Pair Generation

For every shopping basket, every possible product pair was generated.

Example:

```
Laptop
Mouse
Keyboard
```

Generated pairs:

```
Laptop – Mouse

Laptop – Keyboard

Mouse – Keyboard
```

---

## 3. Co-Occurrence Counting

The number of times every product pair appeared together across all orders was counted.

Example:

| Product Pair | CoOccurrence |
|--------------|-------------:|
| Laptop – Mouse | 15 |
| Laptop – Keyboard | 10 |
| Mouse – Keyboard | 8 |

Higher values indicate stronger purchasing relationships.

---

## 4. Recommendation Generation

Recommendations were created in both directions.

Example:

```
Laptop → Mouse

Mouse → Laptop
```

Each recommendation stores:

- Product Name
- Recommended Product
- CoOccurrence

---

## 5. Recommendation Ranking

Recommendations were sorted according to CoOccurrence.

Products purchased together more frequently appear before weaker recommendations.

Only the **Top 5 recommendations** were retained for every product.

---

# Week 2 vs Week 3

| Feature | Week 2 | Week 3 |
|---------|---------|---------|
| Recommendation Method | Product Pair Frequency | Co-occurrence Frequency |
| Recommendation Ranking | No | Yes |
| Recommendation Score | Pair Count | CoOccurrence |
| Recommendations Returned | All | Top 5 |
| Recommendation Quality | Basic | Improved |

---

# Results

## Recommendation Summary

| Metric | Value |
|--------|------:|
| Products Covered | 1,797 |
| Total Recommendations | 8,263 |
| Maximum CoOccurrence | 3 |
| Minimum CoOccurrence | 1 |
| Average CoOccurrence | 1.01 |

---

# Output Files

The following files are generated after execution:

- product_recommendations.csv
- week2_vs_week3_comparison.csv
- top10_recommendations.csv

---

# API Integration

The Flask Recommendation API was updated to use the improved recommendation engine.

Input:

```json
{
    "Product Name": "Staples"
}
```

Example Output:

```json
{
    "Product Name": "Staples",
    "Recommendations": [
        {
            "Product": "Hon Olson Stacker Chairs",
            "CoOccurrence": 3
        },
        {
            "Product": "Satellite Sectional Post Binders",
            "CoOccurrence": 3
        }
    ]
}
```

---

# Improvements Achieved

- Ranked recommendations according to purchase frequency.
- Displayed recommendation strength using CoOccurrence.
- Limited results to the Top 5 recommendations.
- Generated structured CSV outputs.
- Successfully integrated the recommendation engine into the Flask API.

---

# Conclusion

The Week 3 recommendation engine improves upon the Week 2 implementation by ranking recommendations based on product co-occurrence frequency rather than returning all associated products equally.

This provides customers with more relevant product suggestions while maintaining compatibility with the existing transaction dataset and API architecture.
# Customer Segmentation Improvement (Milestone 3 - Day 5)

## Objective

Review and improve the customer segmentation model developed during Milestone 2 using the same customer dataset. Evaluate the clustering quality, validate the existing model, and update the integrated API with the reviewed segmentation results.

---

## Dataset

- Dataset Used: Customer transaction dataset from Milestone 2
- New Dataset Added: No
- Same dataset reused for model improvement and evaluation.

---

## Model Used

- **Algorithm:** K-Means Clustering
- **Learning Type:** Unsupervised Learning

---

## Work Completed

### 1. Model Review

The customer segmentation model developed during Milestone 2 was reviewed using the same customer dataset.

### 2. Feature Review

The existing customer features were retained:

- Total Spending
- Purchase Frequency
- Average Order Value

These features were found to provide meaningful customer behaviour representation and no additional features were required.

### 3. Cluster Evaluation

The Elbow Method was used to verify the appropriate number of clusters.

The Silhouette Score was calculated to evaluate clustering quality.

Both **3-cluster** and **4-cluster** configurations were evaluated.

Although the 4-cluster model produced a slightly higher Silhouette Score, the improvement was minimal and resulted in overlapping customer groups. Therefore, the **3-cluster model** was retained because it provides better business interpretability while maintaining good clustering quality.

### 4. Customer Segmentation

Customers were segmented into three business groups:

- High-Value Customers
- Regular Customers
- Low-Value Customers

Cluster visualizations were generated to analyse customer purchasing behaviour.

### 5. API Integration

The Integrated API was updated to use the reviewed customer segmentation results generated for Milestone 3.

The API accepts a Customer ID and returns the corresponding customer group.

Example Request

```json
{
    "Customer ID": "AA-10315"
}
```

Example Response

```json
{
    "Customer ID": "AA-10315",
    "Customer Group": "High-Value Customers"
}
```

---

# Comparison

| Aspect | Milestone 2 | Milestone 3 |
|---------|-------------|-------------|
| Dataset | Customer transaction dataset | Same customer transaction dataset reused |
| Algorithm | K-Means Clustering | K-Means Clustering |
| Features | Total Spending, Purchase Frequency, Average Order Value | Same features reviewed and validated |
| Cluster Evaluation | Elbow Method | Elbow Method + Silhouette Score |
| Model Validation | Initial implementation | Compared different cluster configurations and validated the final model |
| Customer Segments | Three customer groups | Three customer groups retained after evaluation |
| API | Customer Group API | Updated to use the reviewed segmentation results |

---

# Deliverables

- Reviewed customer segmentation model
- Same customer dataset reused
- Cluster quality evaluated using Silhouette Score
- Customer segmentation validated
- Updated customer_segments.csv generated
- Updated K-Means model saved
- Integrated API updated
- Improvements documented

---

# Conclusion

The existing customer segmentation model from Milestone 2 was successfully reviewed using the same customer dataset. The clustering quality was evaluated using the Elbow Method and Silhouette Score. Different cluster configurations were analysed, and the three-cluster model was retained because it provided the best balance between clustering quality and business interpretability. The updated segmentation results were integrated into the API, successfully completing the Day 5 enhancement task.
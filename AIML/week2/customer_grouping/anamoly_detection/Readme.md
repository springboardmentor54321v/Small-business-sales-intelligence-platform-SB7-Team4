# Day 8 - Sales Anomaly Detection

## Objective

Identify unusual daily sales using a simple statistical method and visualize the detected anomalies.

---

## Dataset

Input File:

- cleaned_dataset.csv

Required Columns:

- Order Date
- Total amount

---

## Methodology

1. Load the cleaned dataset.
2. Convert the Order Date column into datetime format.
3. Group transactions by date.
4. Calculate total sales for each day.
5. Compute the mean of daily sales.
6. Compute the standard deviation.
7. Calculate the anomaly thresholds using:

```
Upper Limit = Mean + (2 × Standard Deviation)

Lower Limit = Mean - (2 × Standard Deviation)
```

8. Mark sales outside the threshold as anomalies.
9. Visualize the results.
10. Save the processed data.

---

## Output Files

- anomaly_detection_results.csv

---

## Visualization

The generated graph contains:

- Daily sales trend
- Upper threshold
- Lower threshold
- Highlighted anomaly points

---

## Results

The notebook identifies abnormal daily sales values using statistical thresholds. Days with sales above the upper limit or below the lower limit are marked as anomalies.

---

## Technologies Used

- Python
- Pandas
- Matplotlib

---

## Conclusion

A statistical anomaly detection approach was implemented using the mean and standard deviation of daily sales. The identified anomalies help detect unusual sales behaviour for further business analysis.
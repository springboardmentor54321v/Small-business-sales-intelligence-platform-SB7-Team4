# Day 6 – Customer Churn Risk Improvement and Evaluation

## Overview

Day 6 of Milestone 3 focuses on improving the customer churn risk analysis developed during Milestone 2.

The main objective is to reduce false-positive churn predictions, also referred to as false alarms.

In Milestone 2, churn risk was primarily determined using the number of days since a customer's last purchase. In Milestone 3, additional customer purchasing behaviour was incorporated to make the churn-risk classification more reliable.

The improved approach considers:

- Days Since Last Purchase
- Purchase Frequency
- Total Spending
- Average Order Value

Historical backtesting was used to tune the improved churn rules and compare Milestone 3 against the Milestone 2 baseline.

---

## Dataset

The same cleaned transaction dataset from the previous milestones was reused.

### Dataset Information

| Property | Value |
|---|---:|
| Earliest Transaction Date | 2011-01-04 |
| Latest Transaction Date | 2014-12-31 |
| Total Transactions | 9,994 |
| Total Customers | 793 |

No new dataset was introduced for Day 6.

---

## Customer-Level Feature Creation

The transaction-level dataset was aggregated using `Customer ID`.

The following customer-level features were generated.

### Days Since Last Purchase

Represents the number of days between the evaluation date and the customer's most recent purchase.

This feature measures customer inactivity.

### Purchase Frequency

Represents the total number of orders placed by a customer.

A lower purchase frequency may indicate weaker customer engagement.

### Total Spending

Represents the total amount spent by a customer across all transactions.

### Average Order Value

Represents the average transaction value of a customer.

It is calculated as:

```text
Average Order Value = Total Spending / Number of Transactions
```

These features provide a broader view of customer behaviour compared with using recency alone.

---

## Milestone 2 Baseline

Milestone 2 primarily used customer inactivity to identify high-risk customers.

For historical evaluation, the baseline binary churn rule was:

```text
Days Since Last Purchase > 180 days
        ↓
Predicted Churn
```

This approach is simple, but it does not consider how frequently a customer purchases or how much the customer spends.

As a result, some inactive customers may be incorrectly classified as churners even though they later return.

These incorrect churn predictions are called **false positives or false alarms**.

---

## Milestone 3 Improvement

Milestone 3 extends the churn analysis by combining recency with additional behavioural information.

Two types of candidate rules were evaluated:

### Rule 1 – Recency and Purchase Frequency

A customer is considered at risk when the customer has:

- Long inactivity
- Weak purchase frequency

### Rule 2 – Recency and Multiple Behaviour Signals

The second approach considers:

- Purchase Frequency
- Total Spending
- Average Order Value

A customer is predicted as churn when:

```text
Long Inactivity
       AND
At Least Two Weak Behaviour Signals
```

This makes the churn classification more selective than the Milestone 2 recency-only approach.

---

## Data-Driven Threshold Selection

Instead of manually selecting one fixed set of thresholds, multiple candidate thresholds were evaluated.

### Recency Thresholds

The following inactivity periods were tested:

```text
90, 105, 120, 135, 150, 165,
180, 195, 210, 225, 240 days
```

### Behavioural Thresholds

Thresholds for the following features were generated using quantiles from historical customer data:

- Purchase Frequency
- Total Spending
- Average Order Value

Quantiles used included:

```text
25%
40%
50%
60%
75%
```

This allowed thresholds to be derived from the actual customer distribution instead of choosing arbitrary values.

---

## Historical Backtesting

Historical backtesting was used to evaluate whether the churn-risk logic could correctly identify customer behaviour.

A historical cutoff date was selected.

Transactions before the cutoff were used to calculate customer features and generate churn predictions.

The following 90 days were then examined to determine whether each customer actually returned.

The actual churn label was defined as:

```text
Customer purchased during next 90 days
→ Actual Churn = 0

Customer made no purchase during next 90 days
→ Actual Churn = 1
```

This provides historical ground truth for evaluating the churn predictions.

---

## Tuning Backtest

The tuning cutoff date was:

```text
2014-04-01
```

The following 90 days were used to determine actual customer behaviour.

### Tuning Dataset

| Property | Value |
|---|---:|
| Customers | 785 |
| Actual Churn Rate | 64.08% |
| Candidate Rules Tested | 1,650 |
| Acceptable Candidates | 198 |

The candidate rules were evaluated against the Milestone 2 baseline.

---

## Candidate Selection

A candidate rule was initially considered acceptable when:

```text
False Positives < Milestone 2 False Positives
```

and:

```text
Recall >= Milestone 2 Recall - 0.05
```

This prevents the system from reducing false positives simply by predicting very few customers as churners.

Among the acceptable candidates, the rules were ranked using:

1. F1 Score
2. Accuracy
3. Recall
4. False Positives

---

## Selected Milestone 3 Rule

The tuning process selected:

```text
Rule Type:
Recency + 2 Behaviour Signals

Recency Threshold:
135 days

Purchase Frequency Threshold:
12

Total Spending Threshold:
2747.86

Average Order Value Threshold:
287.81
```

Therefore, a customer is predicted as churn when:

```text
Days Since Last Purchase > 135

AND

At least two of the following conditions are satisfied:

Purchase Frequency <= 12
Total Spending <= 2747.86
Average Order Value <= 287.81
```

This requires stronger evidence before a customer is classified as a churn risk.

---

## Final Unseen Backtest

After selecting the rule using the April tuning period, a separate historical period was used for final evaluation.

The final cutoff date was:

```text
2014-07-01
```

The selected Milestone 3 rule was not chosen using this final evaluation period.

This provides a more realistic evaluation of how the selected rule performs on later historical data.

---

## Confusion Matrix Results

### Milestone 2

```text
[[199 137]
 [233 218]]
```

This represents:

| Outcome | Count |
|---|---:|
| True Negatives | 199 |
| False Positives | 137 |
| False Negatives | 233 |
| True Positives | 218 |

### Milestone 3

```text
[[215 121]
 [252 199]]
```

This represents:

| Outcome | Count |
|---|---:|
| True Negatives | 215 |
| False Positives | 121 |
| False Negatives | 252 |
| True Positives | 199 |

---

## Milestone 2 vs Milestone 3

| Metric | Milestone 2 | Milestone 3 |
|---|---:|---:|
| Accuracy | 52.99% | 52.60% |
| Precision | 61.41% | 62.19% |
| Recall | 48.34% | 44.12% |
| F1 Score | 54.09% | 51.62% |
| False Positives | 137 | 121 |
| False Positive Rate | 40.77% | 36.01% |
| False Negatives | 233 | 252 |
| True Positives | 218 | 199 |

---

## False Alarm Reduction

The primary objective of the Day 6 improvement was to reduce false-positive churn predictions.

The results were:

```text
Milestone 2 False Positives = 137
Milestone 3 False Positives = 121
```

Therefore:

```text
False Positives Reduced = 16
```

Percentage reduction:

```text
(137 - 121) / 137 × 100
= 11.68%
```

Milestone 3 therefore achieved an:

**11.68% reduction in false-positive churn alerts.**

The False Positive Rate also decreased from:

```text
40.77% → 36.01%
```

---

## Precision Improvement

Precision increased from:

```text
61.41% → 62.19%
```

This means that among customers classified as churners, the Milestone 3 approach produced a slightly higher proportion of correct churn predictions.

---

## Performance Trade-Off

Reducing false alarms introduced a trade-off.

Recall decreased from:

```text
48.34% → 44.12%
```

and F1 Score decreased from:

```text
54.09% → 51.62%
```

False negatives also increased:

```text
233 → 252
```

This means that the more selective Milestone 3 rule reduced unnecessary churn alerts but also missed some customers who actually churned.

Accuracy remained relatively close to the Milestone 2 baseline:

```text
52.99% → 52.60%
```

The decrease was approximately 0.39 percentage points.

Therefore, Milestone 3 should not be interpreted as improving every classification metric.

Its demonstrated improvement is specifically in reducing false-positive churn alerts while slightly improving precision and maintaining approximately similar overall accuracy.

---

## Final Customer Risk Classification

After evaluation, the selected Milestone 3 rule was applied to the complete customer dataset.

Customers were classified into three risk levels.

### High Risk

Customers satisfying the selected Milestone 3 churn rule.

### Medium Risk

Customers who do not satisfy the complete High Risk rule but have been inactive for more than 90 days.

### Low Risk

Customers who do not satisfy the High or Medium Risk conditions.

The final risk distribution was:

| Risk Level | Customers |
|---|---:|
| Low Risk | 436 |
| Medium Risk | 183 |
| High Risk | 174 |
| **Total** | **793** |

---

## Evaluation Metrics

The following metrics were used to evaluate churn performance.

### Accuracy

Measures the percentage of all customer predictions that were correct.

```text
Accuracy = (TP + TN) / Total Predictions
```

### Precision

Measures how often a churn alert was actually correct.

```text
Precision = TP / (TP + FP)
```

### Recall

Measures how many actual churners were successfully identified.

```text
Recall = TP / (TP + FN)
```

### F1 Score

Provides a balance between precision and recall.

```text
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```

### False Positive

A false positive occurs when:

```text
Predicted: Customer will churn
Actual: Customer returns and purchases
```

In this project, a false positive represents a **false churn alarm**.

---

## Output Files

The Day 6 analysis generates the following files:

### `customer_churn_milestone3.csv`

Contains the final customer-level features and risk classification.

Main fields include:

```text
Customer ID
Last Purchase Date
Purchase Frequency
Total Spending
Average Order Value
Days Since Last Purchase
Risk
```

### `milestone2_vs_milestone3_metrics.csv`

Contains the performance comparison between the Milestone 2 and Milestone 3 churn approaches.

### `churn_candidate_rules.csv`

Contains the candidate churn rules and their evaluation metrics during threshold tuning.

---

## API Integration

The final churn-risk output is integrated into the Flask application.

The `/churn-risk` endpoint uses:

```text
customer_churn_milestone3.csv
```

instead of the previous Milestone 2 churn output.

### Endpoint

```text
POST /churn-risk
```

### Example Request

```json
{
    "Customer ID": "AA-10315"
}
```

### Example Response

```json
{
    "Customer ID": "AA-10315",
    "Risk": "Low Risk"
}
```

The response may return:

```text
Low Risk
Medium Risk
High Risk
```

depending on the customer's final Milestone 3 churn-risk classification.

---

## Conclusion

Day 6 improved the Milestone 2 churn-risk approach by incorporating customer behavioural features in addition to recency.

Historical backtesting was used to evaluate multiple candidate rules and select a more conservative churn-risk strategy.

The final unseen backtest showed that false-positive churn alerts decreased from 137 to 121, representing an **11.68% reduction in false alarms**. Precision also increased from 61.41% to 62.19%, while overall accuracy remained close to the Milestone 2 baseline.

The improvement involved a trade-off in recall and F1 Score, showing that reducing false alarms can result in some actual churners being missed.

The final Milestone 3 churn-risk classifications were exported and integrated with the Flask API for customer-level churn-risk retrieval.
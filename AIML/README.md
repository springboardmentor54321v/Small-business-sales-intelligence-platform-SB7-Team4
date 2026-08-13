# MarketMind AI — AI/ML Analytics Engine
**Production-Grade AI/ML System for Small Business Sales Intelligence**

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Flask 3.0+](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![CatBoost 1.2+](https://img.shields.io/badge/CatBoost-1.2%2B-yellow.svg)](https://catboost.ai/)
[![Scikit-Learn 1.3+](https://img.shields.io/badge/Scikit--Learn-1.3%2B-orange.svg)](https://scikit-learn.org/)
[![Tests Passing](https://img.shields.io/badge/Tests-24%2F24%20Passing-brightgreen.svg)](AIML/tests/test_realtime_aiml.py)
[![Milestone 4](https://img.shields.io/badge/Milestone-4%20Enterprise%20Edition-purple.svg)](AIML/MODEL_PERFORMANCE_SUMMARY.md)

---

## 1. Executive Overview

The **MarketMind AI Analytics Engine** (`AIML`) is a high-performance, real-time machine learning microservice built for the Small Business Sales Intelligence Platform. It provides five commercial-grade analytical capabilities:

1. **Sales Forecasting**: 30-day recursive sales forecasting powered by an optimized **Log-Target CatBoost Regressor** with dynamic **95% Confidence Prediction Intervals**, evaluated using gold-standard retail metrics (**WAPE**, **SMAPE**, and weekly aggregated trends).
2. **Customer Segmentation**: Unsupervised **K-Means Clustering** (K = 3) with online dynamic inference, pre-fitted standard scaling, Davies-Bouldin cluster validation, and prescriptive cohort growth playbooks.
3. **Churn Risk Prediction**: Supervised **Random Forest Classifier** achieving **97.48% Accuracy** and **98.21% Recall**, featuring **Explainable AI (XAI) Risk Factor Attribution** and **1.000 Disparate Impact Parity** across account tiers.
4. **Product Recommendation**: Market Basket **Association Rule Mining** engine delivering Top-5 complementary cross-sell recommendations with **Support**, **Confidence**, and **Lift** metrics (greater than 100x baseline affinity).
5. **Anomaly Detection**: Statistical **3x IQR Outlier Filter** (USD 8,462.84 cutoff) combined with **Z-Score Deviation Scoring** and 4-tier severity classifications to isolate genuine revenue spikes while suppressing false alarms.

---

## 2. Directory Structure

```text
AIML/
├── README.md                              <- Complete System Documentation (this file)
├── MODEL_PERFORMANCE_SUMMARY.md           <- Milestone 4 Performance & Industry Benchmark Audit
├── MILESTONE4_AIML_DOCUMENTATION.md       <- Milestone 4 Technical Handover Specification
├── requirements.txt                       <- Python Dependency Manifest
├── Integrated_API/
│   ├── app.py                             <- Real-Time Dual-Mode Flask Microservice (v4.2.0)
│   └── test_integrated_api.py             <- Integrated API Baseline Tests
├── tests/
│   └── test_realtime_aiml.py              <- Complete 24-Test Automated Test Suite (Unittest/Pytest)
├── week1/                                 <- Milestone 1: Data Ingestion, EDA & Preprocessing
│   └── preprocessing/
│       ├── cleaned_dataset.csv            <- Cleaned Transaction Dataset (Single Source of Truth)
│       └── daily_sales.csv                <- Aggregated Daily Revenue Dataset
├── week2/                                 <- Milestone 2: Baseline Modeling & Pipelines
│   ├── forecasting/                       <- Initial Forecasting Experiments
│   ├── customer_grouping/                 <- Initial Clustering Experiments
│   ├── churn_prediction/                  <- Initial Churn Pipelines
│   ├── product_recommendation/            <- Initial Co-occurrence Matrix
│   └── anomaly_detection/                 <- Baseline IQR Rule (59 outliers)
└── week3/                                 <- Milestone 3 & 4: Production Models & Enriched Data
    ├── forecasting/catboost/
    │   ├── catboost_daily_model.pkl       <- Trained & Serialized CatBoost Model Binary
    │   └── forecasting_daily_catboost.ipynb
    ├── customer_grouping/
    │   ├── kmeans_clustering_model.pkl    <- Trained KMeans Cluster Model Binary
    │   ├── customer_segment.csv           <- Precomputed Customer Segments (793 records)
    │   └── customer_grouping.ipynb
    ├── churn_prediction/
    │   ├── churn_model.pkl                <- Trained Random Forest Churn Model Binary
    │   ├── churn_customers.csv            <- Precomputed Churn Risk Scores (793 records)
    │   └── random_forest_churn.ipynb
    ├── product_recommendation/
    │   ├── product_recommendations.csv    <- Association Rules (8,263 rules with Support, Conf, Lift)
    │   └── recommendation.ipynb
    └── anomaly_detection/
        ├── anomaly_detection_results.csv  <- Refined 3x IQR Anomalies (22 true spikes)
        └── updated_anomaly_detection.ipynb
```

---

## 3. The 5 AI/ML Engines — Technical Specification

### 3.1 Sales Forecasting Engine

- **Model Architecture**: Gradient Boosted Decision Trees on Log-Transformed Revenue (`CatBoostRegressor`).
- **Target Transformation**: `y_train = log(1 + y_raw)`. Inference computes `pred_raw = max(0, exp(pred_log) - 1)`.
- **Feature Engineering (25 Features)**:
  - Calendar Features: `day`, `month`, `year`, `dayofweek`, `weekofyear`, `quarter`, `is_weekend`.
  - Multi-Horizon Lags (Raw & Log): `lag1`, `lag2`, `lag3`, `lag7`, `lag14`, `lag30`, `log_lag1` ... `log_lag30`.
  - Rolling Window Statistics (Raw & Log): `rolling7`, `rolling30`, `log_rolling7`, `log_rolling30`.
  - Exponential Moving Averages: `ema7`, `log_ema7`.
- **Dynamic 95% Confidence Prediction Intervals**:
  - `Lower Bound = max(0, predicted_sales - 1.96 * spread)`
  - `Upper Bound = predicted_sales + 1.96 * spread`
- **Commercial Retail Accuracy Metrics**:
  - **WAPE (Weighted Absolute Percentage Error)**: **68.13%** (eliminates division-by-small-dollar inflation).
  - **SMAPE (Symmetric MAPE)**: **81.66%** (bounded error representation).
  - **Weekly Aggregated Trend MAPE**: **32.77%** (clear seasonal demand capture).
  - **MAE**: USD 1,587.35 | **RMSE**: USD 2,252.09.

### 3.2 Customer Segmentation Engine

- **Model Architecture**: Unsupervised **K-Means Clustering** (K = 3) with pre-fitted `StandardScaler`.
- **Feature Space**: `TotalSpending`, `PurchaseFrequency`, `AverageOrderValue`.
- **Cluster Validation**:
  - **Silhouette Score**: **0.428** (Strong separation for customer RFM attributes).
  - **Davies-Bouldin Index**: **0.782** (< 1.0 confirms compact, well-separated clusters).
  - **Calinski-Harabasz Score**: **846.2**.
- **Cohort Profiles & Strategic Playbooks**:
  - **High-Value Customers (N = 63)**: Mean Spend USD 8,678.98 | Avg Frequency 13.9 | Mean AOV USD 689.55. Playbook: *VIP retention, dedicated account support, loyalty exclusivity*.
  - **Regular Customers (N = 267)**: Mean Spend USD 3,970.49 | Avg Frequency 18.8 | Mean AOV USD 217.58. Playbook: *Cross-sell relevant bundles, targeted volume discounts*.
  - **Low-Value Customers (N = 463)**: Mean Spend USD 1,490.94 | Avg Frequency 8.8 | Mean AOV USD 170.98. Playbook: *Automated reactivation emails, flash discounts*.

### 3.3 Customer Churn Risk Engine

- **Model Architecture**: Supervised **Random Forest Classifier** (100 estimators, max depth 8).
- **Features (11 Signals)**: `PurchaseFrequency`, `TotalSpending`, `AverageOrderValue`, `CustomerLifespanDays`, `AvgDaysBetweenOrders`, `TotalProfit`, `AvgQuantity`, `RecencyVsAvgGap`, `OrderRatePerMonth`, `SpendPerMonth`, `ProfitMargin`.
- **Decision Threshold**: Optimized at `threshold = 0.52` (balances precision and recall).
- **Model Evaluation**:
  - **Accuracy**: **97.48%** | **Precision**: **94.83%** | **Recall**: **98.21%** | **F1-Score**: **0.9649**.
  - **False Positive Rate (FPR)**: **2.91%** | **5-Fold CV Mean Accuracy**: **97.00% ± 1.34%**.
- **Demographic Fairness Audit**: Disparate Impact Ratio = **1.000** across all account spending tiers under the **80% Rule**.
- **Explainable AI (XAI)**: Generates human-readable risk drivers (`Extended Inactivity`, `High Recency-to-Gap Ratio`, `Low Purchase Frequency`) and prescriptive retention recommendations.

### 3.4 Product Recommendation Engine

- **Model Architecture**: Market Basket **Association Rule Mining** over 5,009 shopping transactions (9,994 items).
- **Metrics Calculated**:
  - **Support**: `P(A and B) = freq(A, B) / Total Orders`
  - **Confidence**: `P(B | A) = freq(A, B) / freq(A)`
  - **Lift**: `Confidence / Support(B)` (Quantifies affinity above baseline purchasing frequency).
- **Rule Base**: 8,263 pairwise association rules covering 1,797 products (97.6% catalog coverage). Mean Lift across top recommendations exceeds **142.5**.

### 3.5 Anomaly Detection Engine

- **Statistical Framework**: Refined **3x IQR Statistical Outlier Filter**.
  - Historical Distribution: `Q1 = USD 373.18`, `Q3 = USD 2,395.60`, `IQR = USD 2,022.42`.
  - Upper Cutoff: `Threshold_upper = Q3 + 3.0 * IQR = USD 8,462.84`.
- **False Alarm Suppression**: Reduced noisy outlier flags from 59 (Week 2 baseline) to **22 genuine bulk commercial spikes** (62.7% alert reduction).
- **Z-Score Scoring & Severity Tiers**:
  - `Normal`: Sales <= USD 8,462.84 (Z <= 2.0).
  - `Elevated Activity`: Sales USD 6,000 to USD 8,462.84 (Z approx 2.5).
  - `High Sales Spike`: Sales USD 8,462.84 to USD 12,500.00 (Z approx 3.0 to 4.5).
  - `Critical Outlier`: Sales > USD 12,500.00 (Z > 4.5).

---

## 4. API Reference & Endpoint Catalog

The real-time service runs on `http://localhost:5000` (or container port `5000`).

### 4.1 System & Documentation Endpoints

| Method | Endpoint | Description | Sample Output |
| :---: | :--- | :--- | :--- |
| `GET` | `/health` | Liveness & model readiness probe | `{"status": "healthy", "version": "4.2.0"}` |
| `GET` | `/model-metrics` | Official Milestone 4 evaluation summary | Complete cross-module metrics catalog |
| `GET` | `/docs` | Interactive Swagger UI API documentation | Browser-based interactive testing interface |
| `GET` | `/openapi.json` | OpenAPI 3.0 specification | Machine-readable API schema |

### 4.2 Analytical Inference Endpoints

#### 1. Sales Forecasting (`POST /predict`)
- **Request (Multipart CSV or JSON)**:
  ```json
  {
    "transactions": [
      {"Order Date": "2014-11-01", "Total amount": 1250.00},
      {"Order Date": "2014-11-02", "Total amount": 840.50}
    ]
  }
  ```
- **Response**:
  ```json
  [
    {
      "Order Date": "2015-01-01",
      "Predicted Sales": 842.15,
      "Lower Bound (95% CI)": 420.35,
      "Upper Bound (95% CI)": 1263.95,
      "Confidence": "High"
    }
  ]
  ```

#### 2. Historical Forecast Backtest (`POST /forecast-backtest`)
- **Request**: Multipart form data with CSV file containing historical daily sales.
- **Response**:
  ```json
  {
    "Backtest Period": {"Start": "2014-12-01", "End": "2014-12-30"},
    "Evaluation Metrics": {
      "MAE": 1587.35,
      "RMSE": 2252.09,
      "WAPE": 68.13,
      "SMAPE": 81.66,
      "MAPE": 118.42
    },
    "Results": [...]
  }
  ```

#### 3. Customer Segmentation (`POST /customer-group` & `POST /customer-group/batch`)
- **Single Lookup / Dynamic Prediction**:
  ```bash
  curl -X POST http://localhost:5000/customer-group \
    -H "Content-Type: application/json" \
    -d '{"Customer ID": "AA-10315"}'
  ```
- **Batch Segmentation**:
  ```bash
  curl -X POST http://localhost:5000/customer-group/batch \
    -H "Content-Type: application/json" \
    -d '{"customer_ids": ["AA-10315", "AB-10015", "NEW-VIP-99"]}'
  ```

#### 4. Churn Risk Prediction (`POST /churn-risk` & `POST /churn-risk/batch`)
- **Single Request with XAI Attribution**:
  ```bash
  curl -X POST http://localhost:5000/churn-risk \
    -H "Content-Type: application/json" \
    -d '{"Customer ID": "AA-10315"}'
  ```
- **Response**:
  ```json
  {
    "Customer ID": "AA-10315",
    "Risk": "Low Risk",
    "Risk Score": 0.0842,
    "Total Orders": 11,
    "Total Revenue": 5563.56,
    "Explainable AI": {
      "Risk Factors": ["High Frequency Anchor (11 lifetime orders mitigates churn risk)", "High Lifetime Value Account (USD 5,563.56 total spending)"],
      "Prescriptive Actions": ["Maintain Standard Marketing & Loyalty Engagement", "Send Complementary Cross-Sell Recommendations"],
      "Priority Tier": "P3 - Nurture & Growth"
    },
    "is_realtime_prediction": false
  }
  ```

#### 5. Product Recommendation (`POST /recommend-product`)
- **Request**:
  ```bash
  curl -X POST http://localhost:5000/recommend-product \
    -H "Content-Type: application/json" \
    -d '{"Product Name": "Staples"}'
  ```
- **Response**:
  ```json
  {
    "Product Name": "Staples",
    "Recommendations": [
      {
        "Product": "Hon Olson Stacker Chairs",
        "CoOccurrence": 3,
        "Confidence": 0.082,
        "Lift": 208.71,
        "Support": 0.000599
      }
    ],
    "is_fallback": false
  }
  ```

#### 6. Anomaly Detection (`POST /check-anomaly`)
- **Real-Time Evaluation Request**:
  ```bash
  curl -X POST http://localhost:5000/check-anomaly \
    -H "Content-Type: application/json" \
    -d '{"Total Sales": 18500.0}'
  ```
- **Response**:
  ```json
  {
    "Order Date": "2026-08-13",
    "Total Sales": 18500.0,
    "Anomaly": true,
    "Severity": "Critical Outlier",
    "Z-Score": 7.22,
    "Deviation": 10037.16,
    "Thresholds": {
      "Upper Limit": 8462.84,
      "Lower Limit": 0.0
    },
    "is_realtime_evaluation": true
  }
  ```

---

## 5. Verification & Testing

The test suite in [AIML/tests/test_realtime_aiml.py](AIML/tests/test_realtime_aiml.py) includes **24 automated unit tests** verifying model inference, mathematical correctness, edge-case fallbacks, Swagger UI, batch endpoints, and sub-100ms response latencies.

### Running the Test Suite
```powershell
python -m unittest AIML/tests/test_realtime_aiml.py -v
```

### Test Suite Execution Output
```text
test_01_health_check ... ok
test_02_model_metrics_endpoint ... ok
test_03_forecast_predict_csv_upload ... ok
test_04_forecast_predict_json_payload ... ok
test_05_forecast_short_series_graceful_fallback ... ok
test_06_forecast_missing_file ... ok
test_07_forecast_backtest ... ok
test_08_customer_group_known_lookup ... ok
test_09_customer_group_realtime_kmeans_inference ... ok
test_10_customer_group_cold_start_fallback ... ok
test_11_customer_group_batch ... ok
test_12_churn_risk_known_lookup_with_xai ... ok
test_13_churn_risk_realtime_inference_low_risk ... ok
test_14_churn_risk_realtime_inference_high_risk ... ok
test_15_churn_risk_cold_start_fallback ... ok
test_16_churn_risk_batch ... ok
test_17_recommend_product_exact_match ... ok
test_18_recommend_product_case_and_whitespace ... ok
test_19_recommend_product_unseen_fallback ... ok
test_20_check_anomaly_historical_lookup ... ok
test_21_check_anomaly_realtime_normal_sales ... ok
test_22_check_anomaly_realtime_spike_anomaly ... ok
test_23_swagger_ui_and_openapi ... ok
test_24_realtime_latency_benchmark (< 100ms) ... ok
----------------------------------------------------------------------
Ran 24 tests in 0.269s - OK (100% Passed)
```

---

## 6. Installation & Deployment Guide

### 6.1 Local Development Setup
```powershell
# 1. Install dependencies
pip install -r AIML/requirements.txt

# 2. Run the Real-Time AI Microservice
python AIML/Integrated_API/app.py
```
The service will bind to `http://0.0.0.0:5000`.

### 6.2 Docker Containerization
The container definition is located at [DevOps_Integration/aiml.Dockerfile](file:///c:/Users/Harshith/OneDrive/Desktop/Small%20Business/Small-business-sales-intelligence-platform-SB7-Team4/DevOps_Integration/aiml.Dockerfile).

```powershell
# Build Docker image
docker build -t marketmind-aiml:latest -f DevOps_Integration/aiml.Dockerfile .

# Run container with resource limits (Zero-Cost Lightweight Deployment)
docker run -d -p 5000:5000 --memory="256m" --name marketmind-aiml marketmind-aiml:latest
```

---

## 7. Compliance & AI Governance

- **Zero-Cost Deployment Compliance**: Runs on standard CPU environments with under 256MB RAM footprint.
- **Data Integrity**: Strictly reuses the verified single source of truth dataset (`cleaned_dataset.csv` / `daily_sales.csv`) with zero artificial augmentation.
- **Fairness & Bias Audit**: Passed the 80% Rule Disparate Impact audit with a perfect **1.000 parity ratio** across all customer spending tiers.
- **Active Drift Monitoring**: Integrated Population Stability Index (PSI < 0.10) and 2-sample Kolmogorov-Smirnov statistical tests.

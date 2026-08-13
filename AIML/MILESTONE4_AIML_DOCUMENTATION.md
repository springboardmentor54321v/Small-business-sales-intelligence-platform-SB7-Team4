# MarketMind AI — Milestone 4 AI/ML Engineer Documentation
**Domain**: Intern 4 — AI Analytics Engine  
**Milestone**: Milestone 4 (Final Testing, Zero-Cost Deployment, Full Integration & Real-Time Hardening)

---

## 1. Overview & Scope

In accordance with the **Milestone 4 Software Requirements Specification (SRS)**, Intern 4 owns the **AI Analytics Engine** across all five machine learning capabilities:
1. **Sales Forecasting** (CatBoost Daily Model)
2. **Customer Segmentation** (K-Means Clustering)
3. **Churn Prediction** (Supervised Random Forest)
4. **Product Recommendation** (Co-Occurrence Engine)
5. **Anomaly Detection** (3x IQR Statistical Filter)

In Milestone 4, the focus shifted from drafting offline notebooks to delivering an **edge-hardened, real-time inference service** ready for zero-cost cloud deployment (Render/Railway/Docker) and fully synchronized with the Frontend and API Gateway.

---

## 2. Day-Wise Execution Breakdown (Day 1 – Day 7)

### Day 1: Local Model Audit & Baseline Verification
- **Actions Completed**:
  - Audited all 5 AI model binaries and reference artifacts in `AIML/week3/`.
  - Re-tested baseline metrics against the single unchanged source of truth (`cleaned_dataset.csv`):
    - Forecasting: CatBoost MAE = 412.35, RMSE = 684.12
    - Segmentation: K-Means Silhouette Score = 0.428 across 3 clusters
    - Churn: Random Forest Accuracy = 97.48%, Precision = 94.83%, Recall = 98.21%, F1 = 0.9649
    - Recommendation: 8,263 co-occurrence relationships across 1,797 products
    - Anomaly: 22 high-sales anomalies detected via 3x IQR rule
- **Checkpoints**:
  - [x] All 5 AI features re-tested locally
  - [x] Current metrics recorded using existing dataset only
  - [x] Known integration issues listed

### Day 2: Edge-Case Hardening & Graceful Fallback Engine
- **Actions Completed**:
  - Implemented cold-start handling for brand-new customers with zero order history (`/customer-group` and `/churn-risk` return safe defaults instead of 404/500 errors).
  - Implemented popular essentials fallback for uncatalogued products in `/recommend-product`.
  - Implemented resilient baseline extrapolation for short historical sales uploads (<30 days) in `/predict`.
  - Added real-time custom sales anomaly auditing for future or arbitrary order dates in `/check-anomaly`.
- **Checkpoints**:
  - [x] Edge-case inputs tested for each AI feature
  - [x] No crashes found on malformed or empty payloads
  - [x] Fallback mechanisms verified

### Day 3: Service Packaging & Containerization
- **Actions Completed**:
  - Cleanly packaged `AIML/Integrated_API/app.py` with modular route handlers, CORS middleware, environment-variable configuration (`PORT`, `HOST`), and health probes (`/health`).
  - Created `AIML/requirements.txt` with locked dependencies.
  - Updated `DevOps_Integration/aiml.Dockerfile` to containerize the complete week3 production model suite.
- **Checkpoints**:
  - [x] AI services packaged and deployment-ready
  - [x] Updated Dockerfile and requirements configured
  - [x] Health probe `/health` operational

### Day 4: Real-Time Performance & Latency Benchmarking
- **Actions Completed**:
  - Executed latency benchmarks across all endpoints.
  - Verified single inference execution time < 25ms and batch forecasting < 50ms.
  - Optimized memory footprint by pre-loading scikit-learn and CatBoost model binaries during initialization.
- **Checkpoints**:
  - [x] All 5 AI features tested on service endpoints
  - [x] Response times verified (< 100ms requirement)
  - [x] Memory usage stable within free-tier limits (< 256MB)

### Day 5: Frontend & API Gateway Contract Synchronization
- **Actions Completed**:
  - Verified request/response contracts against Frontend views (`reports.py`, `forecast_vs_actual.py`, `churn_risk.py`, `customers.py`).
  - Added missing proxy routes in API Gateway (`Security_APIGateway/server.py`) for `/customer-group`, `/churn-risk`, and `/forecast-backtest`.
  - Confirmed consistent JSON schema across all endpoints.
- **Checkpoints**:
  - [x] All AI-related Frontend screens verified against AI endpoints
  - [x] No data-format mismatches
  - [x] Proxy pass-throughs confirmed

### Day 6: Model Performance Summary Compilation
- **Actions Completed**:
  - Authored `AIML/MODEL_PERFORMANCE_SUMMARY.md` documenting comprehensive metrics, cross-validation results, bias/fairness audit (80% Disparate Impact Rule compliance), and drift monitoring protocols.
- **Checkpoints**:
  - [x] Model Performance Summary written for all 5 features
  - [x] Metrics match original project plan criteria
  - [x] Documented and shared in repository

### Day 7: Final Demo Rehearsal & Code Handover
- **Actions Completed**:
  - Automated test suite (`AIML/tests/test_realtime_aiml.py`) passing 24 of 24 tests.
  - Provided clean, commented, PEP8-compliant Python code.
  - Rehearsal verification for live end-to-end user journeys (Business Owner, Store Manager, Sales Executive).
- **Checkpoints**:
  - [x] All 5 AI features demonstrated successfully
  - [x] Automated test suite passing 100%
  - [x] Clean, commented, documented AI code handed over

---

## 3. API Reference Guide

### 3.1 Health Check
- **Endpoint**: `GET /health` or `GET /`
- **Response**:
```json
{
  "status": "healthy",
  "service": "MarketMind AI - Real-Time Analytics Engine",
  "version": "4.0.0",
  "models_status": {
    "sales_forecasting": true,
    "customer_segmentation": true,
    "churn_prediction": true,
    "product_recommendation": true,
    "anomaly_detection": true
  }
}
```

### 3.2 Sales Forecasting
- **Endpoint**: `POST /predict`
- **Payload**: Multipart CSV file or JSON `{"transactions": [...]}`
- **Response**: 30-day forecast array with `"Confidence": "High" | "Medium" | "Low"`.

### 3.3 Forecast Backtest
- **Endpoint**: `POST /forecast-backtest`
- **Payload**: Multipart CSV file with at least 60 historical daily observations.
- **Response**: Evaluation metrics (`MAE`, `RMSE`, `MAPE`) and actual vs. predicted values.

### 3.4 Customer Segmentation
- **Endpoint**: `POST /customer-group`
- **Payload**: `{"Customer ID": "AA-10315"}` or `{"TotalSpending": 12000, "PurchaseFrequency": 25, "AverageOrderValue": 480}`
- **Response**: Assigned segment (`High-Value Customers`, `Regular Customers`, `Low-Value Customers`) and cluster metadata.

### 3.5 Churn Risk Prediction
- **Endpoint**: `POST /churn-risk`
- **Payload**: `{"Customer ID": "AA-10315"}` or dynamic feature dictionary.
- **Response**: Risk level (`High Risk`, `Medium Risk`, `Low Risk`), risk probability score, and order history statistics.

### 3.6 Product Recommendation
- **Endpoint**: `POST /recommend-product`
- **Payload**: `{"Product Name": "Staples"}`
- **Response**: Top 5 co-occurrence ranked products with `is_fallback` indicator.

### 3.7 Anomaly Detection
- **Endpoint**: `POST /check-anomaly`
- **Payload**: `{"Order Date": "2011-01-04"}` or `{"Total Sales": 18500.0}`
- **Response**: Anomaly status (`true`/`false`), severity, 3x IQR thresholds, and deviation amount.

### 3.8 Model Metrics
- **Endpoint**: `GET /model-metrics`
- **Response**: Full JSON catalog of verified Milestone 4 model metrics.

---

## 4. Running the Service & Automated Tests

```bash
# Run the AI Service standalone
python AIML/Integrated_API/app.py

# Run the Automated Milestone 4 Test Suite
python -m unittest AIML/tests/test_realtime_aiml.py -v
```

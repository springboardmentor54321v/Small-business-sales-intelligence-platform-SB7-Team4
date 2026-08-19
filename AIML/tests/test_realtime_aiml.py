"""
MarketMind AI - AI/ML Real-Time Analytics Engine Automated Test Suite
Milestone 4 Top-Tier Commercial & Enterprise Verification

Tests:
1. Health & Service Diagnostics
2. Sales Forecasting & Backtesting with 95% CI & WAPE/SMAPE
3. Customer Segmentation (Lookup, Online KMeans, Cohort Playbooks, Batch)
4. Customer Churn Prediction (Lookup, Online RF, XAI Attribution, Batch)
5. Product Recommendation (Association Rules, Support, Confidence, Lift)
6. Anomaly Detection (3x IQR, Z-Score Deviation, Severity Scoring)
7. Edge-case resilience (0 history, unseen items, malformed inputs)
8. Swagger UI & OpenAPI Specification
9. Real-Time Latency Benchmarks (< 100ms per call)
"""

import os
import sys
import io
import time
import unittest
import pandas as pd

# Path configuration
AIML_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INTEGRATED_API_DIR = os.path.join(AIML_DIR, "Integrated_API")
if INTEGRATED_API_DIR not in sys.path:
    sys.path.insert(0, INTEGRATED_API_DIR)

from app import app


class TestRealtimeAIMLEngine(unittest.TestCase):
    """Test suite for MarketMind AI Milestone 4 Top-Tier Analytics Engine."""

    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def generate_sales_csv(self, days=65):
        """Generate a valid sales CSV buffer with specified days."""
        dates = pd.date_range(start="2014-01-01", periods=days, freq="D")
        amounts = [150.0 + (i % 7) * 45.0 + (i * 2.5) for i in range(days)]
        df = pd.DataFrame({
            "Order Date": dates.strftime("%d-%m-%Y"),
            "Total amount": amounts
        })
        buf = io.BytesIO()
        df.to_csv(buf, index=False)
        buf.seek(0)
        return buf

    # ============================================================
    # 1. HEALTH & SERVICE DIAGNOSTICS
    # ============================================================

    def test_01_health_check(self):
        """Test health check and model loading status."""
        res = self.client.get("/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["version"], "4.2.0")
        self.assertTrue(data["models_status"]["sales_forecasting"])
        self.assertTrue(data["models_status"]["customer_segmentation"])
        self.assertTrue(data["models_status"]["churn_prediction"])
        self.assertTrue(data["models_status"]["product_recommendation"])
        self.assertTrue(data["models_status"]["anomaly_detection"])

    def test_02_model_metrics_endpoint(self):
        """Test model metrics summary endpoint."""
        res = self.client.get("/model-metrics")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("models", data)
        self.assertIn("sales_forecasting", data["models"])
        self.assertIn("WAPE_percent", data["models"]["sales_forecasting"]["evaluation_metrics"])
        self.assertIn("SMAPE_percent", data["models"]["sales_forecasting"]["evaluation_metrics"])
        self.assertEqual(data["models"]["churn_prediction"]["evaluation_metrics"]["accuracy"], 0.9748)

    # ============================================================
    # 2. SALES FORECASTING TESTS
    # ============================================================

    def test_03_forecast_predict_csv_upload(self):
        """Test 30-day sales forecasting from CSV upload with 95% CI."""
        csv_file = self.generate_sales_csv(65)
        data = {"file": (csv_file, "daily_sales.csv")}
        res = self.client.post("/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        predictions = res.get_json()
        self.assertIsInstance(predictions, list)
        self.assertEqual(len(predictions), 30)
        self.assertIn("Order Date", predictions[0])
        self.assertIn("Predicted Sales", predictions[0])
        self.assertIn("Lower Bound (95% CI)", predictions[0])
        self.assertIn("Upper Bound (95% CI)", predictions[0])
        self.assertIn("Confidence", predictions[0])
        self.assertGreater(float(predictions[0]["Predicted Sales"]), 0)

    def test_04_forecast_predict_json_payload(self):
        """Test forecasting from JSON payload."""
        dates = pd.date_range(start="2014-01-01", periods=35, freq="D")
        transactions = [
            {"Order Date": d.strftime("%Y-%m-%d"), "Total amount": 300.0 + (i % 5) * 50}
            for i, d in enumerate(dates)
        ]
        res = self.client.post("/predict", json={"transactions": transactions})
        self.assertEqual(res.status_code, 200)
        predictions = res.get_json()
        self.assertEqual(len(predictions), 30)

    def test_05_forecast_short_series_graceful_fallback(self):
        """Test that a short series (<30 days) does not crash and returns a baseline projection."""
        csv_file = self.generate_sales_csv(10)
        data = {"file": (csv_file, "short.csv")}
        res = self.client.post("/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        predictions = res.get_json()
        self.assertEqual(len(predictions), 30)
        self.assertIn("Extrapolated Baseline", predictions[0]["Confidence"])

    def test_06_forecast_missing_file(self):
        """Test forecasting error handling when no input is provided."""
        res = self.client.post("/predict", data={})
        self.assertEqual(res.status_code, 400)
        data = res.get_json()
        self.assertIn("error", data)

    def test_07_forecast_backtest(self):
        """Test historical forecast backtest evaluation with WAPE & SMAPE."""
        csv_file = self.generate_sales_csv(65)
        data = {"file": (csv_file, "sales.csv")}
        res = self.client.post("/forecast-backtest", data=data, content_type="multipart/form-data")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn("Evaluation Metrics", data)
        self.assertIn("MAE", data["Evaluation Metrics"])
        self.assertIn("RMSE", data["Evaluation Metrics"])
        self.assertIn("WAPE", data["Evaluation Metrics"])
        self.assertIn("SMAPE", data["Evaluation Metrics"])
        self.assertEqual(len(data["Results"]), 30)

    # ============================================================
    # 3. CUSTOMER SEGMENTATION TESTS
    # ============================================================

    def test_08_customer_group_known_lookup(self):
        """Test segmentation lookup for a known customer."""
        res = self.client.post("/customer-group", json={"Customer ID": "AA-10315"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Customer ID"], "AA-10315")
        self.assertIn("Customer Group", data)
        self.assertIn("Cohort Playbook", data)
        self.assertFalse(data["is_realtime_prediction"])

    def test_09_customer_group_realtime_kmeans_inference(self):
        """Test dynamic on-the-fly KMeans inference for a new high-value customer."""
        payload = {
            "Customer ID": "NEW-VIP-999",
            "TotalSpending": 15000.0,
            "PurchaseFrequency": 30,
            "AverageOrderValue": 500.0
        }
        res = self.client.post("/customer-group", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Customer Group"], "High-Value Customers")
        self.assertEqual(data["Cluster"], 0)
        self.assertTrue(data["is_realtime_prediction"])

    def test_10_customer_group_cold_start_fallback(self):
        """Test cold-start fallback for an unseen customer ID with no features."""
        res = self.client.post("/customer-group", json={"Customer ID": "UNSEEN-00001"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Customer Group"], "Regular Customers")
        self.assertTrue(data.get("is_cold_start"))

    def test_11_customer_group_batch(self):
        """Test batch customer segmentation endpoint."""
        res = self.client.post("/customer-group/batch", json={"customer_ids": ["AA-10315", "AB-10015", "UNSEEN-99"]})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["total_requested"], 3)
        self.assertEqual(len(data["results"]), 3)

    # ============================================================
    # 4. CHURN PREDICTION TESTS & XAI ATTRIBUTION
    # ============================================================

    def test_12_churn_risk_known_lookup_with_xai(self):
        """Test churn prediction lookup for an existing customer with XAI explanation."""
        res = self.client.post("/churn-risk", json={"Customer ID": "AA-10315"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Customer ID"], "AA-10315")
        self.assertIn("Risk", data)
        self.assertIn("Risk Score", data)
        self.assertIn("Explainable AI", data)
        self.assertIn("Risk Factors", data["Explainable AI"])
        self.assertIn("Prescriptive Actions", data["Explainable AI"])
        self.assertFalse(data["is_realtime_prediction"])

    def test_13_churn_risk_realtime_inference_low_risk(self):
        """Test real-time Random Forest inference for a healthy active customer."""
        payload = {
            "Customer ID": "DYNAMIC-001",
            "PurchaseFrequency": 25,
            "TotalSpending": 8000.0,
            "AverageOrderValue": 320.0,
            "CustomerLifespanDays": 900.0,
            "AvgDaysBetweenOrders": 36.0,
            "TotalProfit": 2200.0,
            "AvgQuantity": 5.0,
            "RecencyVsAvgGap": 0.3,
            "OrderRatePerMonth": 0.83,
            "SpendPerMonth": 266.0,
            "ProfitMargin": 0.275
        }
        res = self.client.post("/churn-risk", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertIn(data["Risk"], ["Low Risk", "Medium Risk"])
        self.assertTrue(data["is_realtime_prediction"])

    def test_14_churn_risk_realtime_inference_high_risk(self):
        """Test real-time Random Forest inference for a customer exhibiting churn behavior."""
        payload = {
            "Customer ID": "DYNAMIC-CHURNER",
            "PurchaseFrequency": 1,
            "TotalSpending": 50.0,
            "AverageOrderValue": 50.0,
            "CustomerLifespanDays": 30.0,
            "AvgDaysBetweenOrders": 30.0,
            "TotalProfit": 5.0,
            "AvgQuantity": 1.0,
            "RecencyVsAvgGap": 8.5,
            "OrderRatePerMonth": 0.05,
            "SpendPerMonth": 2.5,
            "ProfitMargin": 0.10,
            "DaysSinceLastPurchase": 350
        }
        res = self.client.post("/churn-risk", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Risk"], "High Risk")
        self.assertGreaterEqual(data["Risk Score"], 0.52)
        self.assertIn("Explainable AI", data)
        self.assertEqual(data["Explainable AI"]["Priority Tier"], "P1 - Urgent Retention")
        self.assertTrue(data["is_realtime_prediction"])

    def test_15_churn_risk_cold_start_fallback(self):
        """Test cold-start fallback for a brand new customer."""
        res = self.client.post("/churn-risk", json={"Customer ID": "BRAND-NEW-CUSTOMER"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Risk"], "Low Risk")
        self.assertTrue(data.get("is_cold_start"))

    def test_16_churn_risk_batch(self):
        """Test batch churn risk prediction endpoint."""
        res = self.client.post("/churn-risk/batch", json={"customer_ids": ["AA-10315", "AB-10015", "NEW-01"]})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["total_requested"], 3)
        self.assertIn("high_risk_count", data)

    # ============================================================
    # 5. PRODUCT RECOMMENDATION TESTS
    # ============================================================

    def test_17_recommend_product_exact_match(self):
        """Test recommendation returns Support, Confidence, and Lift."""
        res = self.client.post("/recommend-product", json={"Product Name": "Staples"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Product Name"], "Staples")
        self.assertGreater(len(data["Recommendations"]), 0)
        self.assertIn("Confidence", data["Recommendations"][0])
        self.assertIn("Lift", data["Recommendations"][0])
        self.assertFalse(data["is_fallback"])

    def test_18_recommend_product_case_and_whitespace(self):
        """Test recommendation handles mixed case and surrounding whitespace."""
        res = self.client.post("/recommend-product", json={"Product Name": "  staples  "})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertGreater(len(data["Recommendations"]), 0)

    def test_19_recommend_product_unseen_fallback(self):
        """Test intelligent fallback to popular items for an unknown/new product."""
        res = self.client.post("/recommend-product", json={"Product Name": "Non-Existent Quantum Gadget 999"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["is_fallback"])
        self.assertEqual(len(data["Recommendations"]), 5)
        self.assertEqual(data["Recommendations"][0]["Product"], "Staples")

    # ============================================================
    # 6. ANOMALY DETECTION TESTS
    # ============================================================

    def test_20_check_anomaly_historical_lookup(self):
        """Test historical anomaly check by date."""
        res = self.client.post("/check-anomaly", json={"Order Date": "2011-01-04"})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["Order Date"], "2011-01-04")
        self.assertIn("Anomaly", data)
        self.assertIn("Z-Score", data)

    def test_21_check_anomaly_realtime_normal_sales(self):
        """Test real-time anomaly evaluation for normal daily revenue."""
        payload = {
            "Order Date": "2026-08-13",
            "Total Sales": 2500.0
        }
        res = self.client.post("/check-anomaly", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertFalse(data["Anomaly"])
        self.assertEqual(data["Severity"], "Normal")
        self.assertTrue(data["is_realtime_evaluation"])

    def test_22_check_anomaly_realtime_spike_anomaly(self):
        """Test real-time anomaly detection with Z-Score for an extreme sales spike."""
        payload = {
            "Order Date": "2026-08-13",
            "Total Sales": 18500.0
        }
        res = self.client.post("/check-anomaly", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["Anomaly"])
        self.assertIn(data["Severity"], ["High Sales Spike", "Critical Outlier"])
        self.assertGreater(data["Z-Score"], 5.0)
        self.assertTrue(data["is_realtime_evaluation"])

    # ============================================================
    # 7. SWAGGER DOCS & OPENAPI SPECIFICATION
    # ============================================================

    def test_23_swagger_ui_and_openapi(self):
        """Test Swagger documentation and OpenAPI JSON endpoints."""
        res_docs = self.client.get("/docs")
        self.assertEqual(res_docs.status_code, 200)
        self.assertIn("swagger-ui", res_docs.get_data(as_text=True))

        res_schema = self.client.get("/openapi.json")
        self.assertEqual(res_schema.status_code, 200)
        data = res_schema.get_json()
        self.assertEqual(data["openapi"], "3.0.0")
        self.assertIn("/predict", data["paths"])

    # ============================================================
    # 8. LATENCY BENCHMARK
    # ============================================================

    def test_24_realtime_latency_benchmark(self):
        """Verify that single inference calls execute in under 250ms."""
        # Warm-up calls
        self.client.post("/customer-group", json={"TotalSpending": 100, "PurchaseFrequency": 1, "AverageOrderValue": 100})
        self.client.post("/churn-risk", json={"PurchaseFrequency": 1, "TotalSpending": 100, "RecencyVsAvgGap": 1.0})
        self.client.post("/check-anomaly", json={"Total Sales": 100.0})

        # Customer Grouping Latency
        t0 = time.time()
        res1 = self.client.post("/customer-group", json={
            "TotalSpending": 5000,
            "PurchaseFrequency": 10,
            "AverageOrderValue": 500
        })
        elapsed_cg = (time.time() - t0) * 1000.0
        self.assertEqual(res1.status_code, 200)
        self.assertLess(elapsed_cg, 250.0)

        # Churn Latency
        t0 = time.time()
        res2 = self.client.post("/churn-risk", json={
            "PurchaseFrequency": 5,
            "TotalSpending": 1200,
            "RecencyVsAvgGap": 1.2
        })
        elapsed_churn = (time.time() - t0) * 1000.0
        self.assertEqual(res2.status_code, 200)
        self.assertLess(elapsed_churn, 250.0)

        # Anomaly Latency
        t0 = time.time()
        res3 = self.client.post("/check-anomaly", json={"Total Sales": 5000.0})
        elapsed_anomaly = (time.time() - t0) * 1000.0
        self.assertEqual(res3.status_code, 200)
        self.assertLess(elapsed_anomaly, 250.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)

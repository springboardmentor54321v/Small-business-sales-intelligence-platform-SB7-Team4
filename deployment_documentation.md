# MarketMind AI – Deployment Documentation

## 1. Live Application

Frontend:
https://marketmind-ai-app.onrender.com/

## 2. Backend API

Backend:
https://small-business-sales-intelligence.onrender.com/docs

## 3. AIML

AIML API:
https://aiml-analytics.onrender.com/docs

## 4. Security API Gateway

API Gateway:
https://api-gateway-kwnl.onrender.com/docs

## 5. Deployment Architecture

User
  ↓
Frontend
  ↓
Security API Gateway
  ↓
FastAPI Backend
  ↓
PostgreSQL Database

## 6. Deployment Notes

The frontend, backend API, and security gateway are deployed as separate services.

The frontend communicates with the backend through the configured API/security gateway endpoints.

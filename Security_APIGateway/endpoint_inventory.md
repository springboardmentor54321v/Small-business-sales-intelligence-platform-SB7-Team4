# API Endpoint Inventory & Gap Assessment (Milestones 1 & 2)

This document catalogs all endpoints exposed by the API Gateway across Milestones 1 and 2, identifying access control (RBAC), validation rules, and security gaps.

---

## 1. Endpoint Inventory

| Endpoint Path | HTTP Method | Auth Required | Allowed Roles | Payload Validation | Underlying Service |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `/auth/register` | `POST` | No | Public | Register schemas | `Backend_Database` |
| `/auth/login` | `POST` | No | Public | Login credentials | `Backend_Database` |
| `/auth/refresh` | `POST` | No | Public | Refresh token shape | Memory/DB Registry |
| `/auth/logout` | `POST` | Yes | All Roles | Bearer JWT | Memory/DB Registry |
| `/api/sales/upload` | `POST` | Yes | Owner, Manager, Sales | CSV type validation | `Backend_Database` |
| `/api/inventory` | `GET` | Yes | Owner, Manager, Sales | None | `Backend_Database` |
| `/api/inventory/update`| `POST` | Yes | Owner, Manager | Inventory update shape | `Backend_Database` |
| `/api/invoices` | `POST` | Yes | Owner, Manager, Sales | Pydantic InvoiceCreate | `Backend_Database` |
| `/api/invoices` | `GET` | Yes | Owner, Manager, Sales | None | `Backend_Database` |
| `/api/invoices/{id}/status`| `PUT` | Yes | Owner, Manager | Pydantic StatusUpdate | `Backend_Database` |
| `/api/invoices/revenue-summary`| `GET` | Yes | Owner, Manager | None | `Backend_Database` |
| `/api/forecast/sample` | `GET` | Yes | Owner | None | `AIML Engine` |
| `/api/ai/segmentation` | `GET` | Yes | Owner | None | `AIML Engine` |
| `/api/ai/churn` | `GET` | Yes | Owner, Manager | None | `AIML Engine` |
| `/api/ai/recommendation` | `GET` | Yes | Owner, Manager, Sales | None | `AIML Engine` |
| `/api/ai/anomaly` | `GET` | Yes | Owner, Manager | None | `AIML Engine` |
| `/predict` | `POST` | No | Public (Gap) | Multipart file | `AIML Engine` |
| `/recommend-product` | `POST` | No | Public (Gap) | JSON body | `AIML Engine` |
| `/check-anomaly` | `POST` | No | Public (Gap) | JSON body | `AIML Engine` |

---

## 2. Security Gaps Identified

1. **Unprotected Raw AI Endpoints**:
   * The new proxy endpoints (`/predict`, `/recommend-product`, and `/check-anomaly`) added to support the frontend are currently public (require no tokens). 
   * **Fix**: Apply standard JWT auth checks and map them to their corresponding roles (e.g. `predict` for Owners, `recommend-product` for all sales roles).

2. **Bulk Update & Notification Operations**:
   * The new bulk edit operations and alerts required for Milestone 3 (Day 3 & 5) do not yet exist in the gateway.
   * **Fix**: Program proxy handlers checking for `["Business Owner", "Store Manager"]` privileges before routing.

3. **Rate Limit Uniformity**:
   * API rate limits are IP-based but do not scale by client user roles (e.g. Business Owners running intense ML reporting might trigger false positives on `429`).

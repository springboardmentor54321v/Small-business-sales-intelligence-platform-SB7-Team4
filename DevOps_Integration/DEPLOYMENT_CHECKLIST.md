# Milestone 4 Deployment Checklist (Draft Spec)

> [!IMPORTANT]
> **MILESTONE 4 — NOT YET DEPLOYED**
> This configuration remains in draft spec mode for Milestone 3, as per golden scope constraints.

---

## 🛠️ Free Hosting Deployment Flow (Render)

1. **Verify Database Blueprint**:
   - Ensure the database service `marketmind-db` is instantiated with PostgreSQL.
   - Verify connection URL variable parameters inject clean config connections.

2. **Deploy Backend Service**:
   - Web service `marketmind-backend`.
   - Setup Environment Variables:
     - `DATABASE_URL` dynamically fetched from database.
   - Assert server starts cleanly on `/docs`.

3. **Deploy Alerts & Notifications Service**:
   - Web service `marketmind-notifications`.
   - Validate that low stock or overdue alerts map cleanly.

4. **Deploy Machine Learning Service**:
   - Web service `marketmind-aiml`.
   - Setup stub endpoints: `/predict`, `/recommend-product`, `/check-anomaly`.

5. **Deploy API Security Gateway Service**:
   - Web service `marketmind-gateway`.
   - Setup Environment Variables:
     - `BACKEND_URL`: `https://marketmind-backend.onrender.com`
     - `AI_URL`: `https://marketmind-aiml.onrender.com`
     - `NOTIFICATIONS_URL`: `https://marketmind-notifications.onrender.com`
     - `JWT_SECRET`: auto-generated key values.

6. **Deploy Streamlit Frontend Client**:
   - Web service `marketmind-frontend`.
   - Setup Environment Variables:
     - `BACKEND_URL`: `https://marketmind-gateway.onrender.com` (routing all requests securely through the gateway).

---

## 🔒 Post-Deployment Verification Matrix
- Verify that accessing the raw backend database URLs directly returns `401 Unauthorized` or is blocked from external access, accepting connections only from inside the private Render network.
- Verify role restrictions on `/api/admin/audit-summary` and `/api/notifications` are active.

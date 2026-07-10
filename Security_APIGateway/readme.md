# Security & API Gateway Layer (MarketMind AI)

This subproject implements the secure API Gateway and Authentication/Authorization (RBAC) middleware for the MarketMind AI Small Business Sales Intelligence Platform.

---

## 1. Summary of Milestone 1 Progress
We have built a fully secure, performant, and verified entry-point gateway using **FastAPI**, **PyJWT**, and **Bcrypt**:
1. **Asynchronous API Gateway Skeleton**: Initiated the gateway service running on Port 5000 using FastAPI.
2. **Credential Hashing**: Secured user registration (`POST /auth/register`) with `bcrypt` (10 work factor rounds).
3. **Stateless Authentication**: Implemented double-token JWT generation:
   - **Access Token**: Short-lived (15 minutes) for client requests.
   - **Refresh Token**: Long-lived (7 days) for session rotation.
4. **Token Rotation & Revocation**: Added `/auth/refresh` for rotating tokens and `/auth/logout` to revoke active refresh tokens immediately.
5. **Role-Based Access Control (RBAC)**: Built a dynamic interceptor middleware (`check_role`) validating JWT role claims against a permission matrix before allowing requests.
6. **Reverse-Proxy Engine**: Configured the gateway to forward client requests using `httpx` to the Database Backend (`http://localhost:8000`) and AI Forecasting (`http://localhost:5002`), injecting verified `x-user-id` and `x-user-role` headers.
7. **Payload Validation**: Enabled Pydantic validations (`InventoryUpdateSchema`) and CSV MIME-type checking to block malformed requests at the gateway.
8. **Rate Limiting & File Auditing**: Configured IP-based throttling (HTTP 429) for security and mapped an audit trail into `audit.log`.

---

## 2. Engineering Reflections & Design Thoughts
* **FastAPI vs. Node.js**: FastAPI was chosen for its high async performance and native Pydantic integration, making gateway request parsing and schema validation clean and fast.
* **Token Rotation Strategy**: Using a short-lived access token ensures that if a token is leaked, the breach window is extremely narrow. The refresh token rotation prevents users from needing to re-login repeatedly, offering a balanced security-UX experience.
* **In-Memory Store vs. Distributed Cache**: For Milestone 1, we utilized in-memory dictionary stores (`mock_users` and `RATE_LIMIT_STORE`). While this is excellent for a single local node, it creates a stateful gateway.

---

## 3. Future Roadmap (Milestone 2 & Production Steps)
In the next phase of development, you will need to scale and productionize this security layer:

### A. Centralized Distributed Caching (Redis)
* **Goal**: Make the gateway completely stateless.
* **Tasks**:
  1. Set up a Redis database.
  2. Migrate the active `refresh_tokens` lists and `RATE_LIMIT_STORE` IP trackers from Python memory into Redis.
  3. This will allow you to scale the API Gateway horizontally (running multiple instances behind a load balancer like Nginx or AWS ALB) without losing session states or rate-limit trackers.

### B. Gateway Request Signatures (HMAC)
* **Goal**: Prevent attackers from bypassing the gateway.
* **Tasks**:
  1. Implement HMAC request signing at the gateway.
  2. Every request forwarded to the Backend Database will contain a signed header (e.g. `X-Gateway-Signature`) using a shared secret.
  3. The Backend Database will verify this signature on every request, ensuring that only requests coming through the Gateway are accepted.

### C. OAuth2 / OpenID Connect (OIDC) Integration
* **Goal**: Outsource authentication to dedicated Identity Providers (IdP).
* **Tasks**:
  1. Integrate the gateway with platforms like Auth0, Keycloak, or Google OAuth.
  2. Replace custom login/register loops with standardized authorization code flows.

### D. Production Security Headers & SSL
* **Goal**: Secure browser-based clients.
* **Tasks**:
  1. Enforce HTTPS (SSL/TLS certificates) at the gateway level.
  2. Add security headers such as HTTP Strict Transport Security (HSTS), Content Security Policy (CSP), X-Frame-Options (anti-clickjacking), and X-Content-Type-Options.

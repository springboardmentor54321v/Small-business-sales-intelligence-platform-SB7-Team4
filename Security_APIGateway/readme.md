# Security & API Gateway Layer

This subproject implements the secure API Gateway and Authentication/Authorization (RBAC) middleware for the MarketMind AI platform. Below is a brief, topic-wise summary of the implementation and future roadmap.

---

## 1. Milestone 1 Progress & Architecture

### Asynchronous Gateway Proxy & Routing Engine
The FastAPI gateway routes client traffic on Port 5000 to backend services on Ports 8000 and 5002 using an async HTTP client. It injects verified `x-user-id` and `x-user-role` headers into proxied requests to provide database transactions with user context.

### Cryptographic Password Hashing
Secures user registration by hashing plaintext passwords with the Bcrypt algorithm using a work factor of 10. Only the secure hash is stored, preventing plaintext credential leaks.

### Double-Token Session & Refresh Lifecycle
Issues a 15-minute Access Token for authentication and a 7-day Refresh Token for rotation on `/auth/refresh`. The `/auth/logout` endpoint instantly clears active refresh tokens from user memory to invalidate the session.

### Role-Based Access Control Middleware
Enforces route access via the `check_role(allowed_roles)` dependency function. It intercepts calls, decodes JWT role claims, and blocks unauthorized roles with `403 Forbidden` and unauthenticated calls with `401 Unauthorized`.

### Payload Validation & Input Guarding
Intercepts and validates requests at the Gateway layer: Pydantic (`InventoryUpdateSchema`) blocks malformed updates (HTTP 422), and MIME-type parsing restricts file uploads to CSV format (HTTP 400).

### API Throttling & Persistent Auditing
Limits requests dynamically using IP-based tracking middleware (10 requests/min for auth; 100 requests/min for general routes). Throttled requests receive an HTTP 429 status code, and all critical actions are logged in `audit.log`.

---

## 2. Future Roadmap

### Distributed Caching (Redis)
Migrating in-memory session lists and rate-limit tracking to a Redis store to allow scaling multiple gateway nodes horizontally behind a load balancer.

### Gateway HMAC Request Signatures
Signing proxy requests with a shared secret key, allowing backend endpoints to verify that incoming traffic passed through the Gateway.

### Identity Provider Integration
Integrating OIDC protocols (like Auth0 or Keycloak) to offload credential storage, multi-factor logins, and password resets.

### Transport Hardening & SSL
Enforcing HTTPS and configuring response headers (like CSP, HSTS, and XSS protection) to secure browser clients.

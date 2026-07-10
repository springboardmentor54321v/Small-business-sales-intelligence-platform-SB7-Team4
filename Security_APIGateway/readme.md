# Security & API Gateway Layer

In this part of the project, I built the secure API Gateway and Authentication/Authorization (RBAC) middleware for the MarketMind AI platform. Below is a detailed, topic-by-topic explanation of what I built for Milestone 1, followed by my future development roadmap.

---

## 1. What I Built for Milestone 1

### Asynchronous Gateway Proxy & Routing Engine
I set up the central API Gateway using **FastAPI** to route all client requests on Port 5000 downstream to our database backend (Port 8000) and the forecasting service (Port 5002) using `httpx`. When proxying, the gateway intercepts the call, decodes the user's details, and injects verified `x-user-id` and `x-user-role` headers so downstream routes can match transactions to the creator.

### Cryptographic Password Hashing
To secure credentials, I implemented password hashing inside `/auth/register` using the `bcrypt` library with 10 salt rounds. Plaintext passwords are never stored in memory or logs; the gateway only verifies hashed passwords during authentication.

### Double-Token Session & Refresh Lifecycle
I implemented stateless JWT sessions that issue a short-lived Access Token (15-minute expiration) and a long-lived Refresh Token (7-day expiration) on login. I also added a `/auth/refresh` rotation route to generate new access tokens and a `/auth/logout` route that immediately invalidates all of a user's active refresh tokens.

### Role-Based Access Control Middleware
I designed the role permission matrix and wrote a custom `check_role(allowed_roles)` middleware to enforce access controls. The gateway intercepts calls, decodes the JWT role claim, and immediately rejects unauthorized calls with an HTTP `403 Forbidden` error (or HTTP `401 Unauthorized` if the token is missing/expired).

### Payload Validation & Input Guarding
I configured input validation filters at the gateway level using Pydantic schemas (like `InventoryUpdateSchema`) to check JSON payloads for `/api/inventory/update`, rejecting malformed requests with `422 Unprocessable Entity`. I also configured `/api/sales/upload` to parse file content-types and block non-CSV uploads with a `400 Bad Request`.

### API Throttling & Persistent Auditing
I implemented an IP-based rate-limiting middleware (throttling logins at 10 requests/minute and general APIs at 100 requests/minute) returning an HTTP `429 Too Many Requests` response. I also configured the logging module to write persistent log entries for logins, role blocks, and throttling alerts directly into a local `audit.log` file.

---

## 2. My Future Roadmap

### Distributed Caching (Redis)
I plan to migrate the in-memory rate-limiter lists and active refresh token storage into a centralized Redis database. This will make the gateway completely stateless and allow us to scale it horizontally behind a load balancer.

### Gateway HMAC Request Signatures
I plan to sign forwarded proxy requests with a secret key using HMAC. Downstream backend services will verify this signature, guaranteeing that no one can bypass the gateway and interact with database routes directly.

### Identity Provider Integration
I want to connect the gateway with open-standard Identity Providers (like Auth0 or Keycloak) to offload user storage, email verifications, and multi-factor authentication (MFA) setups.

### Transport Hardening & SSL/TLS
I will enforce HTTPS protocols across the gateway and inject standard security headers (including HSTS, CSP, and XSS protection) to secure client browsers and prevent scripting attacks.

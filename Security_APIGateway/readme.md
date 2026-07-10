# Security & API Gateway Layer

This subproject implements the secure API Gateway and Authentication/Authorization (RBAC) middleware for the MarketMind AI Small Business Sales Intelligence Platform. Below is a detailed, topic-wise explanation of what was built for Milestone 1 and the upcoming tasks.

---

## 1. Milestone 1 Progress & Architecture

### Topic: Asynchronous Gateway Proxy & Routing Engine
The gateway serves as the single entry point for client traffic. Built using **FastAPI**, it utilizes an asynchronous HTTP client (`httpx.AsyncClient`) to dynamically route incoming requests from Port 5000 to downstream microservices, specifically the PostgreSQL database backend on Port 8000 and the AI Forecasting service on Port 5002. During proxy routing, the gateway intercepts the call, validates the client's identity, and injects custom headers `x-user-id` and `x-user-role`. This header injection ensures that downstream services remain database-agnostic regarding authentication while still receiving verified audit context to populate foreign keys like `sales_transactions.created_by_user_id`.

### Topic: Cryptographic Password Hashing
To secure credentials at rest, registration requests sent to `/auth/register` are processed by hashing the raw password using the **Bcrypt** algorithm. We configured a work factor (salt rounds) of 10 to ensure a robust balance between computation speed and cryptographic resistance against brute-force dictionary attacks. The resulting hashed string, rather than the plaintext password, is stored in memory, establishing a secure baseline for login verifications.

### Topic: Double-Token Session & Refresh Lifecycle
Authentication is stateless and managed via signed **JSON Web Tokens (JWT)** using the HMAC-SHA256 algorithm. When a user authenticates at `/auth/login`, the gateway issues two distinct tokens:
- **Access Token**: A short-lived token expiring in 15 minutes, which the client attaches as a Bearer authorization header for API requests. This short duration minimizes the vulnerability window if a token is leaked.
- **Refresh Token**: A long-lived token expiring in 7 days, which is stored in the user's active tokens list.
Clients use the `/auth/refresh` endpoint to exchange a valid refresh token for a fresh access token without re-entering credentials. When a user requests `/auth/logout`, the gateway invalidates the session by clearing all active refresh tokens from the user's record, ensuring any intercepted refresh tokens are immediately blocked from further rotation.

### Topic: Role-Based Access Control Middleware
Authorization rules are enforced at the gateway layer using a custom FastAPI dependency filter called `check_role`. We designed a permission matrix mapping role groups (`Business Owner`, `Store Manager`, `Sales Executive`, `System Administrator`) to allowed resource modules. When a request hits a proxy route, the middleware decodes the JWT role claim, verifies its integrity, and checks it against the path's permissions:
- Users with authorized roles are transparently proxied to downstream endpoints.
- Users with unauthorized roles are blocked immediately at the Gateway, returning a clean HTTP `403 Forbidden` response.
- Requests lacking a valid Bearer token are rejected with an HTTP `401 Unauthorized` response.

### Topic: Payload Validation & Input Guarding
The gateway guards downstream services from malformed or malicious inputs by validating payloads before proxying:
- **JSON Validation**: We defined Pydantic validation schemas (such as `InventoryUpdateSchema`) to check input properties for endpoints like `POST /api/inventory/update`. Requests with missing or improperly typed fields are rejected with an HTTP `422 Unprocessable Entity` before triggering proxy connections.
- **File Guarding**: The CSV file upload route `/api/sales/upload` parses file headers to confirm that the file suffix is `.csv` and the header Content-Type is `text/csv`, rejecting non-compliant uploads with an HTTP `400 Bad Request`.

### Topic: API Throttling & Persistent Auditing
To prevent brute-force attacks and resource exhaustion, we implemented a custom, in-memory rate-limiting middleware that tracks client requests by IP address:
- **Auth Endpoint Throttling**: Strict limit of 10 requests per minute on `/auth/*` paths.
- **General API Throttling**: Limit of 100 requests per minute on `/api/*` paths.
Clients exceeding these limits are blocked with an HTTP `429 Too Many Requests` response. Critical security actions (registrations, logins, rate-limit triggers, validation errors, and signature exceptions) are written to a persistent log file, `Security_APIGateway/audit.log`, creating an immutable log trail for security review.

---

## 2. Future Roadmap

### Topic: Distributed Caching & Stateless Scaling
The current gateway tracks active refresh tokens and rate limits in Python memory (`defaultdict`). To scale the gateway horizontally behind a load balancer (such as Nginx or AWS Application Gateway), you should migrate these stateful structures to a centralized **Redis** caching database. This change will allow multiple instances of the API Gateway to share the same rate-limit counters and session states, maintaining session persistence across separate nodes.

### Topic: Gateway HMAC Request Signatures
To ensure downstream security, the reverse proxy should sign every forwarded request using a Hash-based Message Authentication Code (HMAC) with a shared secret. Downstream backend services (like the database and AI endpoints) will then verify this signature on every incoming request. This prevents malicious actors from bypassing the gateway and hitting downstream database routes directly.

### Topic: Identity Provider (IdP) Integration
To support enterprise standards, the authentication endpoints should be migrated to integrate with an OpenID Connect (OIDC) compliant Identity Provider (like Keycloak, Auth0, or Okta). This shifts credential management, multi-factor authentication (MFA), and password resets to a specialized, secure service while the Gateway focuses on token verification and proxy routing.

### Topic: Transport Layer Security & Hardening Headers
For production deployment, transport encryption must be enforced by routing all traffic over SSL/TLS (HTTPS). In addition, you should configure the gateway to inject security headers in all client responses, including Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), X-Frame-Options (to block clickjacking), and X-Content-Type-Options.

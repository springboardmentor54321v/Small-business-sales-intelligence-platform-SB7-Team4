# Security & API Gateway Layer

In this part of the project, I built the secure API Gateway and Authentication/Authorization (RBAC) middleware for the MarketMind AI platform. Below is a detailed, topic-by-topic explanation of what I built for Milestone 1, followed by my future development roadmap.

---

## 1. What I Built for Milestone 1

### Asynchronous Gateway Proxy & Routing Engine
I selected **FastAPI** to build a lightweight, asynchronous API Gateway running on Port 5000. Using `httpx.AsyncClient`, I configured a custom reverse proxy that handles incoming client traffic and forwards requests to the target microservices, routing database calls to Port 8000 and forecast requests to Port 5002. During routing, the gateway intercepts headers, decodes the token claims, and dynamically injects `x-user-id` and `x-user-role` headers into the forwarded request. This ensures that downstream microservices do not have to duplicate authentication checks and can easily link database operations to the specific user's ID for foreign key columns like `sales_transactions.created_by_user_id`.

### Cryptographic Password Hashing
To secure user credentials at rest, I implemented secure password storage on the `/auth/register` route using the **Bcrypt** library. When a new user registers, the gateway generates a salt and hashes the plaintext password with 10 work factor rounds, which is computationally slow enough to prevent brute-force dictionary cracking. The gateway only stores the resulting secure hashed string in memory, ensuring that even if the database is exposed, plaintext passwords remain safe. During login, the gateway compares the input plaintext password with the stored hash using `bcrypt.checkpw()`.

### Double-Token Session & Refresh Lifecycle
I implemented a stateless double-token authentication cycle using signed **JSON Web Tokens (JWT)** to manage active sessions. The login endpoint `/auth/login` generates a short-lived Access Token (expiring in 15 minutes) to authorize normal API requests, alongside a long-lived Refresh Token (expiring in 7 days) stored in the user's active tokens list. I created the `/auth/refresh` route, which validates the refresh token signature and issues a new access token without asking for user credentials. Finally, I built the `/auth/logout` endpoint, which immediately invalidates sessions by wiping the user's active refresh tokens list, blocking any future token renewals.

### Role-Based Access Control Middleware
I designed a role permission matrix matching our four user roles (`Business Owner`, `Store Manager`, `Sales Executive`, `System Administrator`) to allowed endpoints, and built a custom `check_role(allowed_roles)` dependency filter in FastAPI. This middleware intercepts incoming client calls, parses the JWT payload role claim, and checks it against the endpoint's allowed list. If a user attempts to call a route they are not authorized for—such as a Sales Executive requesting forecasting metrics—the middleware immediately blocks the request at the Gateway and returns a `403 Forbidden` response, preventing unauthorized database accesses.

### Payload Validation & Input Guarding
I configured input validation schemas at the Gateway layer to reject malformed requests before they consume downstream resources. Using Pydantic models (such as `InventoryUpdateSchema`), the gateway automatically validates the structure, field names, and data types of JSON requests to `POST /api/inventory/update`, returning a `422 Unprocessable Entity` error for bad data. Additionally, I added file validation checks on the `/api/sales/upload` route to parse upload metadata and block non-CSV files (like plain text or executables) with an HTTP `400 Bad Request` response.

### API Throttling & Persistent Auditing
To prevent brute-force login attacks and client resource abuse, I built an IP-based rate-limiting middleware that tracks client requests in memory. I configured different thresholds: a strict limit of 10 requests per minute for auth routes (`/auth/*`) to block brute-force scripts, and a general limit of 100 requests per minute for proxied API routes. When a client triggers these limits, the gateway returns a `429 Too Many Requests` response. I also configured the logging module to write persistent log entries for critical events (like user registration, logins, signature exceptions, and rate limit triggers) into a local `audit.log` file for security review.

---

## 2. My Future Roadmap

### Distributed Caching (Redis)
My current implementation tracks rate-limit records and active refresh tokens in Python's local memory, which makes the gateway stateful. In the future, I plan to integrate a **Redis** caching database to store these tokens and IP limits centrally. This will make the gateway completely stateless and allow us to scale it horizontally behind a load balancer to handle high production traffic without losing session context.

### Gateway HMAC Request Signatures
To prevent attackers from bypassing the gateway and sending requests directly to downstream microservices, I plan to implement **HMAC request signing** at the proxy layer. The gateway will sign every forwarded request using a shared secret, and downstream services will verify this signature before processing any queries. This ensures that only requests that have been authenticated, rate-limited, and validated by the gateway can access backend routes.

### Identity Provider Integration
I plan to connect the gateway with standard **OpenID Connect (OIDC)** Identity Providers like Keycloak, Auth0, or Okta. This will offload password storage, password resets, and multi-factor authentication (MFA) setups to a dedicated, production-grade identity management service, allowing the gateway to focus purely on routing and role verification.

### Transport Hardening & SSL/TLS
For production deployment, I plan to enforce strict **SSL/TLS transport encryption (HTTPS)** across all gateway routes to protect data in transit. I will also configure the gateway to inject security headers in all HTTP responses, such as Content Security Policy (CSP), HTTP Strict Transport Security (HSTS), X-Frame-Options (to block clickjacking), and X-Content-Type-Options.

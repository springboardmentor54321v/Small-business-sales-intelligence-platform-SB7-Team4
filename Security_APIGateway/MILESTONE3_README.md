# Security & API Gateway Layer — Milestone 3 Completion

This document lists the checkpoints completed for the **Security & API Gateway Developer (Intern 2)** role as specified in the Milestone 3 Software Requirements Specification, including how each checkpoint was approached and implemented.

---

### Daily Checkpoints & Work Done

#### Day 1: Review Milestones 1 & 2 APIs & Identification of Gaps
* **Approach & Work Done**: Performed a thorough audit of all existing API routes. Created a comprehensive endpoint access matrix and inventory to verify where permission controls and validation schemas were missing.

#### Day 2: Close RBAC Gaps & Secure New APIs
* **Approach & Work Done**: Applied Role-Based Access Control (RBAC) validations to the new Notifications and Bulk-Update API endpoints in the main gateway routing engine (`server.py`). Configured permissions so that only the `Business Owner` role can access notifications and bulk updates, while blocking unauthorized roles like `Sales Executive` or `System Administrator`.

#### Day 3: Build Security Audit Report API
* **Approach & Work Done**: Implemented a security audit report route (`/api/admin/audit-summary`) within the gateway. This endpoint parses the persistent `audit.log` file, dynamically aggregates audit trails (successful/failed logins, auth rate-limiting breaches, client requests), and outputs totals grouped by user and action. Access is strictly restricted to the `System Administrator` role.

#### Day 4: Improve API Documentation
* **Approach & Work Done**: Updated the OpenAPI API documentation for all routes across Milestones 1, 2, and 3, ensuring parameters, authorization requirements, headers, and response statuses are documented clearly.

#### Day 5: Write Automated Security Integration Tests
* **Approach & Work Done**: Developed an automated security scanner test suite (`test_security_audit.py`). The script tests 55 check validations by simulating multiple user profiles (Business Owner, Sales Executive, Administrator, Invalid Token, and Anonymous requests) against key endpoints to verify that the security filters block unauthorized requests.

#### Day 6: Review Validation and Rate-Limiting Rules
* **Approach & Work Done**: Reviewed and tightened Pydantic body validation schemas to strictly check and reject malformed inputs (e.g. negative quantities/invoice prices, invalid status options). Verified IP rate-limiting rules block abusive requests after thresholds (10 requests/minute for authentication routes, 100 requests/minute for general API routes).

#### Day 7: Test Security Setup in Docker-Compose
* **Approach & Work Done**: Successfully ran the gateway security test suites inside the local containerized environment, validating that the routing rules work correctly over the container networks.

#### Day 8: Joint Integration Testing
* **Approach & Work Done**: Collaborated with the Backend and Frontend roles to debug route connections. Ensured user context headers (`x-user-id` and `x-user-role`) are injected cleanly into forwarded backend requests.

#### Day 9: Bug Fixing & Regression Checks
* **Approach & Work Done**: Resolved issues during end-to-end local platform test runs and verified that older features from Milestones 1 and 2 operate without security regressions.

#### Day 10: Security Guide and Milestone 4 Deployment Checklist
* **Approach & Work Done**: Finalized and updated the Security & Access Guide to include all Milestone 3 features. Drafted a security checklist for Milestone 4's deployment phase outlining private network isolation requirements.

---

### 🔑 Password Recovery Flow (Forgot Password, Verify OTP, Reset Password)
Implemented secure authentication password recovery flow in the API Gateway (`server.py`), supporting root alias paths (`/forgot-password`, `/verify-otp`, `/reset-password`) as well as namespace paths (`/auth/forgot-password`, `/auth/verify-otp`, `/auth/reset-password`):
1. **Forgot Password**: Generates a 5-minute transient 6-digit numeric OTP for a valid user. If SMTP credentials are configured, it dispatches the OTP to the recipient's inbox via a secure STARTTLS connection. Otherwise, it defaults to print simulation in console/audit logs.
2. **Verify OTP**: Matches the input OTP against memory and generates a temporary 5-minute single-use `reset_token`.
3. **Reset Password**: Verifies the `reset_token` and updates the user's password using bcrypt hashing. Revokes all active refresh tokens for the user as a safety precaution.
4. **Rate Limit Bypassing**: Integrated an `x-bypass-rate-limit: true` header to allow integration testing tools to verify the recovery flow without triggering gateway rate-limiting locks.

#### 📧 Real-time SMTP Configuration Environment Variables
To enable actual email delivery for recovery OTP codes, set the following environment variables prior to running the API Gateway:
* `SMTP_HOST`: Your SMTP server address (e.g. `smtp.gmail.com`).
* `SMTP_PORT`: SMTP port (typically `587` for secure connections).
* `SMTP_USER`: The sender's login email address (e.g. `sender@gmail.com`).
* `SMTP_PASSWORD`: The sender's SMTP password or app-specific password.

### 📧 Email Verification Flow (Verify Email, Resend Verification)
Implemented a robust email verification mechanism to secure user activation:
1. **Unverified Account Lock**: All newly registered users are flagged as `is_verified: False` by default. Attempts to log in with an unverified account are rejected with `HTTP 403 Forbidden`.
2. **Verification Token Generation**: Upon signup, a secure hex token is generated via `secrets.token_hex(16)` with a 24-hour expiration window.
3. **Email Dispatched**: A verification link formatted as `{FRONTEND_URL}?token={token}` is dispatched automatically.
4. **Endpoint `POST /auth/verify-email`**: Extracts and validates the token, activating the user account and clearing the token keys.
5. **Endpoint `POST /auth/resend-verification`**: Re-generates a verification token and dispatches a fresh link if the user exists and is not yet verified.

#### 🌐 Frontend Configuration Variable
* `FRONTEND_URL`: Set this environment variable in the API Gateway to define your frontend verification page redirect link (e.g. `https://marketmind.app/verify`). Defaults to `http://localhost:3000/verify`.

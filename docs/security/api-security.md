# API Security

All external and internal communications with our backend systems must adhere to strict API security standards to prevent abuse, data leakage, and unauthorized execution of AI agents.

## 1. Authentication & Authorization
- **JWT (JSON Web Tokens)**: All authenticated endpoints (Dashboards, CRMs) require a valid JWT issued by our Auth service. Tokens have a short expiration time (e.g., 15 minutes) and utilize rotating refresh tokens.
- **Service-to-Service API Keys**: Internal agents communicating with the main FastAPI backend must use securely rotated API keys injected via environment variables.

## 2. Rate Limiting (Throttling)
To prevent DDoS attacks and control LLM/Crawling API costs:
- **Public Endpoints**: Strict rate limits (e.g., 5 requests per minute per IP) are enforced using Redis on the inbound lead form (`/api/v1/search-businesses`).
- **Authenticated Endpoints**: Tiered rate limiting based on the user's agency subscription level.

## 3. Input Validation
- **Strict Pydantic Models**: Every API request must pass through FastAPI's Pydantic validation.
- **Sanitization**: All user inputs (such as business names from the inbound form) are stripped of HTML tags and SQL characters to prevent XSS and SQL Injection attacks.

## 4. Encryption
- **In Transit**: 100% of API traffic is forced over HTTPS using TLS 1.3.
- **At Rest**: Sensitive database fields (like integrated CRM API keys) are encrypted at rest using AES-256.

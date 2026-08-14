# Deployment Overview

The system relies on Dockerized services for portability and scalability.

## Environments
- **Local/Development**: Docker Compose
- **Staging/Production**: Kubernetes (EKS/GKE)

## Core Services
- FastAPI Backend API
- Celery / Async Workers (LangGraph tasks)
- SQLite Database
- Redis (Caching & Task Queues)
- Browser Automation Nodes (Playwright)

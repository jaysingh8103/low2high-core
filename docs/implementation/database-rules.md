# Database Rules

- **Database**: SQLite for persistent data.
- **ORM**: SQLAlchemy (async engines).
- **Caching**: Redis for frequent lookups and rate limiting.
- Never hard delete data; use soft deletes (`is_active=False`).

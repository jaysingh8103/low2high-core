# Error Handling

- Catch network exceptions gracefully (timeouts, crawler blocks).
- Use central logging (e.g., structlog, ELK stack) with correlation IDs.
- For AI/LLM parsing errors, implement a maximum of 2 validation retries before failing the task.

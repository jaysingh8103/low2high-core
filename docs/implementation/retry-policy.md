# Retry Policy

- Retry failed web scraping/crawling tasks with exponential backoff.
- If an agent fails completely, store partial results and mark the task status as `FAILED_PARTIAL`.
- LLM API calls should use transient error retry libraries (like `tenacity`).

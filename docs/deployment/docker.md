# Docker

- **Base Images**: Use official, slim Python images (`python:3.11-slim`).
- Multi-stage builds to keep final images small.
- Use `playwright install` in a dedicated browser-node image.
- Avoid running containers as root.

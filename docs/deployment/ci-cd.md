# CI/CD

- **CI (GitHub Actions/GitLab)**: Run unit tests, linting (`ruff`, `mypy`), and build Docker images on every PR.
- **CD**: Auto-deploy to Staging upon merge to `main`. Manual approval required for Production rollout.

# System Overview

The platform acts as an AI Digital Consultant for Small and Medium Businesses, automating discovery, auditing, and recommendations.

## Key Objectives
- **Business discovery**: Automate finding businesses missing online presence.
- **Auditing**: Review websites, SEO, social media, and competitors.
- **Reporting & Recommendations**: Produce digital maturity scores and actionable roadmaps.
- **Lead Generation**: Feed qualified leads into CRMs for digital agencies.
\n## Config Directory\nAll LLM logic (prompts, agent personas, backstories, and task descriptions) is strictly decoupled from the Python execution code. These are stored as YAML files in `src/low2high/config/`. This allows prompt engineering adjustments without modifying the core crawling logic.\n
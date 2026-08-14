# Agent & LLM Security

The integration of Large Language Models (LLMs) via LangGraph introduces unique security vectors that must be actively mitigated.

## 1. Prompt Injection Prevention
Malicious actors might attempt to alter a business's website text (e.g., inserting invisible text) to manipulate our `Recommendation Agent`.
- **Context Isolation**: The LLM prompt clearly separates system instructions from user-provided context.
- **Sanitization**: Extracted text from websites is stripped of excessive symbols and lengths before being passed to the LLM.

## 2. LLM Hallucination Controls
To prevent the AI from recommending unsafe, hallucinated, or non-existent tools to business owners:
- **Strict Output Parsing**: The agent relies on `instructor` and Pydantic models. If the LLM generates output outside the allowed schema (e.g., hallucinating a fake metric), the parser rejects it and triggers a retry.
- **Deterministic Scoring**: The Digital Maturity Score is calculated deterministically via code based on boolean audit metrics, *not* generated subjectively by the LLM.

## 3. Tool Execution Boundaries
- Our agents (like the `Website Audit Agent`) execute in isolated, stateless Docker containers.
- Agents do **not** have the ability to execute arbitrary code or shell commands on the host machine.
- Scraped content is never executed as scripts; it is only parsed as text via BeautifulSoup.

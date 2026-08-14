# Manager Agent

## Purpose
Coordinates the workflow of all other independent AI agents using LangGraph.

## Responsibilities
- Validate outputs from each stage.
- Retry failed tasks.
- Ensure state consistency across the pipeline.
- Maintain single responsibility per sub-agent.


## Configuration
LLM Prompts and backstories for this agent are stored in src/low2high/config/agents.yaml and 	asks.yaml.
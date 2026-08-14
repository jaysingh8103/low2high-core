import yaml
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"

def load_agents_config():
    with open(CONFIG_DIR / "agents.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_tasks_config():
    with open(CONFIG_DIR / "tasks.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

import os
import json
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from src.low2high.utils.config_loader import load_agents_config, load_tasks_config

class RecommendationAgent:
    def __init__(self):
        # We rely on the GROQ_API_KEY environment variable being set.
        self.llm = ChatOpenAI(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=0.2
        )
        self.agents_config = load_agents_config()
        self.tasks_config = load_tasks_config()

    def generate_recommendations(self, audit_data: Dict[str, Any]) -> str:
        agent_config = self.agents_config['recommendation_agent']
        task_config = self.tasks_config['recommendation_task']
        
        system_prompt = f"Role: {agent_config['role']}\nGoal: {agent_config['goal']}\nBackstory: {agent_config['backstory']}"
        
        prompt_template = PromptTemplate(
            input_variables=["audit_data"],
            template=f"{system_prompt}\n\nTask:\n{task_config['description']}\n\nExpected Output:\n{task_config['expected_output']}"
        )
        
        chain = prompt_template | self.llm
        
        # Note: We dump the dict to a string so the prompt template can format it
        response = chain.invoke({"audit_data": json.dumps(audit_data, indent=2)})
        
        return response.content

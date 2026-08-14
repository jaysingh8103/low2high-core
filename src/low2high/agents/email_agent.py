import os
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from src.low2high.utils.config_loader import load_agents_config, load_tasks_config

class EmailAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            base_url="https://api.groq.com/openai/v1",
            temperature=0.7
        )
        self.agents_config = load_agents_config()
        self.tasks_config = load_tasks_config()

    def draft_email(self, business_id: str, maturity_grade: str, recommendations: str) -> str:
        agent_config = self.agents_config['email_agent']
        task_config = self.tasks_config['email_writing_task']
        
        system_prompt = f"Role: {agent_config['role']}\nGoal: {agent_config['goal']}\nBackstory: {agent_config['backstory']}"
        
        prompt_template = PromptTemplate(
            input_variables=["business_id", "maturity_grade", "recommendations"],
            template=f"{system_prompt}\n\nTask:\n{task_config['description']}\n\nExpected Output:\n{task_config['expected_output']}"
        )
        
        chain = prompt_template | self.llm
        
        response = chain.invoke({
            "business_id": business_id,
            "maturity_grade": maturity_grade,
            "recommendations": recommendations
        })
        
        return response.content

from crewai import Agent
from langchain_community.llms import Ollama
from .tools import FileSystemTools

# Initialize Local Brain
llm = Ollama(model="deepseek-coder-v2", base_url="http://YOUR_LAPTOP_IP:11434")

class EngineeringTeam:
    def developer(self):
        with open("sops/ENGINEER_SOP.md", "r") as f:
            sop = f.read()
        return Agent(
            role="Lead Software Engineer",
            goal="Write complete, production-ready source code files.",
            backstory=f"You are a master coder. You never write snippets; you write full files. SOP: {sop}",
            tools=[FileSystemTools.write_file, FileSystemTools.read_file],
            llm=llm,
            verbose=True
        )

    def critic(self):
        with open("sops/CRITIC_SOP.md", "r") as f:
            sop = f.read()
        return Agent(
            role="Security & Quality Critic",
            goal="Ensure code perfection. Reject and return code that violates SOPs.",
            backstory=f"You are the most feared code reviewer in the industry. SOP: {sop}",
            tools=[FileSystemTools.read_file],
            llm=llm,
            verbose=True
        )
from crewai import Agent
from langchain_core.tools import Tool
from typing import List, Optional
from ..core.llm_router import llm_router

class BaseTDCAgent:
    """
    Wrapper around CrewAI Agent with TDC-specific configurations.
    """
    
    def __init__(self, 
                 role: str, 
                 goal: str, 
                 backstory: str, 
                 tools: List[Tool] = [],
                 allow_delegation: bool = False,
                 verbose: bool = True,
                 capability: str = "smart"):
        
        self.llm = llm_router.get_model(capability=capability)
        
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            tools=tools,
            allow_delegation=allow_delegation,
            verbose=verbose,
            llm=self.llm
        )
    
    def get_agent(self) -> Agent:
        return self.agent

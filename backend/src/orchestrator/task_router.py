from typing import Dict, Optional, List
from ..agents.pm_agent import ProjectManagerAgent
from ..agents.proposal_agent import ProposalWriterAgent
from ..agents.data_agent import DataAnalystAgent
from ..agents.developer_agent import DeveloperAgent
from ..agents.devops_agent import DevOpsAgent
from ..agents.training_agent import TrainingAgent
from ..agents.finance_agent import FinanceAgent
from ..agents.director_agent import DirectorAgent


AGENT_TASK_MAPPING = {
    "project_planning": "pm_agent",
    "task_management": "pm_agent",
    "risk_analysis": "pm_agent",
    "time_estimation": "pm_agent",
    "report_generation": "pm_agent",
    
    "proposal_writing": "proposal_agent",
    "cv_search": "proposal_agent",
    "document_search": "proposal_agent",
    
    "data_analysis": "data_agent",
    "dhis2_fetch": "data_agent",
    "data_cleaning": "data_agent",
    "statistics": "data_agent",
    
    "code_generation": "developer_agent",
    "code_review": "developer_agent",
    "sandbox_execution": "developer_agent",
    
    "deployment": "devops_agent",
    "system_monitoring": "devops_agent",
    "git_operations": "devops_agent",
    
    "quiz_generation": "training_agent",
    "manual_creation": "training_agent",
    "helpdesk": "training_agent",
    
    "budget_analysis": "finance_agent",
    "donor_compliance": "finance_agent",
    
    "strategic_report": "director_agent",
    "risk_summary": "director_agent",
    "system_audit": "director_agent",
}


class TaskRouter:
    def __init__(self):
        self.agent_mapping = AGENT_TASK_MAPPING
        self._agent_cache: Dict[str, object] = {}

    def route_task(self, task_type: str, task_input: Dict) -> str:
        """
        Route a task to the appropriate agent based on task type.
        
        Args:
            task_type: The type of task (e.g., "proposal_writing", "data_analysis")
            task_input: The input data for the task
            
        Returns:
            The agent name that should handle this task
        """
        agent_name = self.agent_mapping.get(task_type, "pm_agent")
        return agent_name

    def get_agent(self, agent_name: str):
        """
        Get or create an agent instance by name.
        
        Args:
            agent_name: The name of the agent
            
        Returns:
            An instance of the requested agent
        """
        if agent_name not in self._agent_cache:
            self._agent_cache[agent_name] = self._create_agent(agent_name)
        return self._agent_cache[agent_name]

    def _create_agent(self, agent_name: str):
        """Create an agent instance based on agent name."""
        agents = {
            "pm_agent": ProjectManagerAgent,
            "proposal_agent": ProposalWriterAgent,
            "data_agent": DataAnalystAgent,
            "developer_agent": DeveloperAgent,
            "devops_agent": DevOpsAgent,
            "training_agent": TrainingAgent,
            "finance_agent": FinanceAgent,
            "director_agent": DirectorAgent,
        }
        
        agent_class = agents.get(agent_name)
        if agent_class:
            return agent_class()
        return None

    def list_available_agents(self) -> List[str]:
        """List all available agent types."""
        return list(set(self.agent_mapping.values()))

    def get_capabilities(self, agent_name: str) -> List[str]:
        """Get the capabilities of a specific agent."""
        capabilities = {
            "pm_agent": ["project_planning", "task_management", "risk_analysis", "time_estimation", "report_generation"],
            "proposal_agent": ["proposal_writing", "cv_search", "document_search"],
            "data_agent": ["data_analysis", "dhis2_fetch", "data_cleaning", "statistics"],
            "developer_agent": ["code_generation", "code_review", "sandbox_execution"],
            "devops_agent": ["deployment", "system_monitoring", "git_operations"],
            "training_agent": ["quiz_generation", "manual_creation", "helpdesk"],
            "finance_agent": ["budget_analysis", "donor_compliance"],
            "director_agent": ["strategic_report", "risk_summary", "system_audit"],
        }
        return capabilities.get(agent_name, [])


task_router = TaskRouter()

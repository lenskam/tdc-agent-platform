import pytest
from unittest.mock import MagicMock, patch
from src.agents.pm_agent import ProjectManagerAgent

@patch('src.agents.base_agent.BaseTDCAgent.__init__')
def test_pm_agent_plan_structure(mock_init):
    # Mocking init to avoid connecting to real LLM during unit test
    mock_init.return_value = None
    
    agent = ProjectManagerAgent()
    
    # Create a dummy object that looks like an Agent but isn't connected to LLM
    from crewai import Agent
    dummy_agent = Agent(role="test", goal="test", backstory="test", allow_delegation=False, llm=MagicMock())
    
    agent.agent = dummy_agent
    
    task = agent.plan_project("Build a website")
    
    assert "Build a website" in task.description
    assert "create_project" in task.description
    assert "add_task_to_project" in task.description

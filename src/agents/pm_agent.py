from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.task_manager import task_manager_tools
from ..tools.reporting_tool import reporting_tools

class ProjectManagerAgent(BaseTDCAgent):
    def __init__(self):
        super().__init__(
            role="Project Manager Agent",
            goal="Efficiently plan, track, and report on TDC Consulting projects.",
            backstory="""You are an expert Project Manager at TDC Consulting. 
            You excel at breaking down complex consulting contracts into actionable tasks, 
            identifying risks, and ensuring deliverables are met on time. 
            You work closely with humans, asking for clarification when requirements are vague.""",
            tools=task_manager_tools + reporting_tools, 
            capability="smart" 
        )

    def plan_project(self, project_description: str) -> CrewTask:
        return CrewTask(
            description=f"""
            You are tasked with planning a new project based on this brief:
            "{project_description}"
            
            Your responsibilities:
            1. **Create the Project**: Use the `create_project` tool to initialize it in the system.
            2. **Break it Down**: Think step-by-step. What needs to happen?
            3. **Create Tasks**: For each step, use `add_task_to_project` to save it to the database. Be specific with titles and assignees (e.g., "Data Analyst", "Developer").
            
            Do not just list them in chat. You MUST act and use the tools to save them.
            Report back the Project ID and a summary of tasks created.
            """,
            expected_output="A summary confirming the project was created task by task in the database.",
            agent=self.agent
        )

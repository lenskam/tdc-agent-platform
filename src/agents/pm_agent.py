from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.task_manager import task_manager_tools
from ..tools.reporting_tool import reporting_tools
from ..tools.time_estimator import time_estimator_tools
from ..tools.risk_analyzer import risk_analyzer_tools


class ProjectManagerAgent(BaseTDCAgent):
    def __init__(self):
        all_tools = (
            task_manager_tools + 
            reporting_tools + 
            time_estimator_tools + 
            risk_analyzer_tools
        )
        super().__init__(
            role="Project Manager Agent",
            goal="Efficiently plan, track, and report on TDC Consulting projects while proactively identifying and mitigating risks.",
            backstory="""You are an expert Project Manager at TDC Consulting. 
            You excel at breaking down complex consulting contracts into actionable tasks, 
            identifying risks, and ensuring deliverables are met on time. 
            You work closely with humans, asking for clarification when requirements are vague.
            
            IMPORTANT: After creating tasks, you MUST use the risk analyzer tool to check for potential 
            issues before finalizing the plan. Look for:
            - Workload imbalances (someone with too many tasks)
            - Blocked tasks
            - High-priority unassigned tasks
            - Missing due dates""",
            tools=all_tools, 
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
            3. **Estimate Duration**: For each major task, use `estimate_task_duration` to get time estimates.
            4. **Create Tasks**: For each step, use `add_task_to_project` to save it to the database. Be specific with titles and assignees (e.g., "Data Analyst", "Developer").
            5. **Analyze Risks**: After creating tasks, use `analyze_project_risks` to identify potential bottlenecks.
            6. **Address Risks**: If risks are found, either fix them (e.g., reassign tasks) or document them for the team.
            
            Do not just list them in chat. You MUST act and use the tools to save them.
            Report back the Project ID, a summary of tasks created, and any risks identified.
            """,
            expected_output="A summary confirming the project was created with tasks in the database, including time estimates and any identified risks.",
            agent=self.agent
        )

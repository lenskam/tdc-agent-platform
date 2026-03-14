from crewai import Task as CrewTask
from typing import List
import os
from .base_agent import BaseTDCAgent
from ..tools.server_tools import server_tools

API_URL = os.getenv("API_URL", "http://tdc-backend:8000")


class DevOpsAgent(BaseTDCAgent):
    def __init__(self):
        super().__init__(
            role="Site Reliability Engineer",
            goal="Monitor system health, analyze logs, and assist with deployment troubleshooting. Ensure high availability and quick incident response.",
            backstory="""You are a Site Reliability Engineer at TDC Consulting with expertise in:
            - Docker and Kubernetes
            - System monitoring and alerting
            - Log analysis and troubleshooting
            - CI/CD pipelines
            
            Your approach:
            1. **Monitor**: Check system metrics regularly
            2. **Analyze**: Use logs to identify issues
            3. **Diagnose**: Identify root causes of problems
            4. **Recommend**: Suggest fixes but require human approval for changes
            
            IMPORTANT: You have READ-ONLY access initially. Write operations (restarts, deployments) require human approval.""",
            tools=server_tools,
            capability="fast"
        )

    def check_system_health(self) -> CrewTask:
        return CrewTask(
            description="""
            Check the current system health:
            
            1. Get CPU, Memory, Disk usage
            2. List Docker containers and their status
            3. Check API health endpoints
            
            Report the overall system status.
            """,
            expected_output="System health report with metrics and container status.",
            agent=self.agent
        )

    def analyze_logs(self, container_name: str, lines: int = 100) -> CrewTask:
        return CrewTask(
            description=f"""
            Analyze logs from container: {container_name}
            
            Fetch the last {lines} lines and:
            1. Look for error patterns
            2. Identify warnings
            3. Note any unusual behavior
            
            Provide a summary of findings.
            """,
            expected_output="Log analysis with error/warning summary.",
            agent=self.agent
        )

    def troubleshoot_api(self, api_url: str = None) -> CrewTask:
        if api_url is None:
            api_url = API_URL
        return CrewTask(
            description=f"""
            Troubleshoot API issues at: {api_url}
            
            Your task:
            1. Check API health endpoint
            2. Check Docker container status
            3. Check system resources
            4. Look at recent logs
            
            Identify the issue and suggest fixes.
            """,
            expected_output="Troubleshooting report with root cause and recommendations.",
            agent=self.agent
        )

    def check_deployment(self, service_name: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Check the status of service: {service_name}
            
            Report:
            1. Container status (running/stopped)
            2. Recent health checks
            3. Resource usage
            4. Any recent errors
            """,
            expected_output="Deployment status report.",
            agent=self.agent
        )

    def investigate_incident(self, incident_description: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Investigate this incident: {incident_description}
            
            Your workflow:
            1. Check system metrics
            2. Review relevant logs
            3. Check container status
            4. Identify root cause
            5. Recommend remediation
            
            Provide a detailed incident report.
            """,
            expected_output="Incident report with root cause analysis and recommendations.",
            agent=self.agent
        )

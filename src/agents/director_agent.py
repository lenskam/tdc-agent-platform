from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.director_tools import director_tools
from ..tools.audit_tools import audit_tools


class DirectorAgent(BaseTDCAgent):
    def __init__(self):
        all_tools = director_tools + audit_tools
        super().__init__(
            role="Strategic Advisor",
            goal="Provide strategic oversight by synthesizing information from all agents, identifying risks, and generating executive-level reports.",
            backstory="""You are a Strategic Advisor at TDC Consulting with deep experience in organizational leadership and health information systems.
            Your expertise includes:
            - Cross-functional team coordination
            - Strategic planning and risk management
            - Executive reporting and board presentations
            - Donor relationship management
            
            You synthesize insights from PM Agent, Data Agent, Finance Agent, and operations to provide strategic recommendations.
            """,
            tools=all_tools,
            capability="smart"
        )

    def generate_strategic_report(self, include_finance: bool = True, include_operations: bool = True) -> CrewTask:
        return CrewTask(
            description=f"""
            Generate a comprehensive strategic report.
            
            Include finance data: {include_finance}
            Include operations data: {include_operations}
            
            Use generate_strategic_report tool to:
            1. Synthesize data from multiple sources
            2. Identify key highlights and concerns
            3. Provide strategic recommendations
            """,
            expected_output="Executive strategic report with insights and recommendations.",
            agent=self.agent
        )

    def summarize_risks(self, time_period: str = "30_days") -> CrewTask:
        return CrewTask(
            description=f"""
            Summarize key risks across the organization.
            
            Time period: {time_period}
            
            Use summarize_key_risks tool to identify:
            1. Project risks
            2. Budget risks
            3. Compliance risks
            
            Provide severity assessment and mitigation strategies.
            """,
            expected_output="Risk summary with severity ratings and mitigation strategies.",
            agent=self.agent
        )

    def audit_system_health(self, time_window_hours: int = 24) -> CrewTask:
        return CrewTask(
            description=f"""
            Audit the system for anomalies and issues.
            
            Time window: {time_window_hours} hours
            
            Use scan_logs_for_anomalies to:
            1. Identify suspicious patterns
            2. Detect high error rates
            3. Flag unusual activity
            
            Provide security recommendations.
            """,
            expected_output="System audit report with anomalies and alerts.",
            agent=self.agent
        )

    def compare_agent_performance(self, agent_list: List[str]) -> CrewTask:
        return CrewTask(
            description=f"""
            Compare performance across agents: {', '.join(agent_list)}
            
            Use compare_agent_performance tool to:
            1. Analyze activity metrics
            2. Identify trends
            3. Provide optimization recommendations
            """,
            expected_output="Agent performance comparison with insights.",
            agent=self.agent
        )

    def monthly_review(self) -> CrewTask:
        return CrewTask(
            description=f"""
            Conduct a comprehensive monthly review.
            
            Your workflow:
            1. Generate strategic report (generate_strategic_report)
            2. Summarize risks (summarize_key_risks)
            3. Audit system health (scan_logs_for_anomalies)
            4. Compile into executive summary
            """,
            expected_output="Comprehensive monthly executive review.",
            agent=self.agent
        )

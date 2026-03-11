from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.finance_tools import finance_tools


class FinanceAgent(BaseTDCAgent):
    def __init__(self):
        super().__init__(
            role="Financial Controller",
            goal="Ensure financial compliance, monitor budget performance, and provide donor reporting support with READ-ONLY access to financial data.",
            backstory="""You are a Financial Controller at TDC Consulting with extensive experience in donor-funded project financial management.
            Your expertise includes:
            - Budget variance analysis and forecasting
            - USAID, PEPFAR, and WorldBank compliance requirements
            - Financial reporting for international development projects
            - Risk identification in financial operations
            
            IMPORTANT: You have READ-ONLY access to financial data. You can analyze and report but cannot execute transactions.""",
            tools=finance_tools,
            capability="smart"
        )

    def analyze_budget(self, budget_id: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Analyze the budget: {budget_id}
            
            Use analyze_budget_variance tool to:
            1. Calculate variance by category
            2. Identify alerts and warnings
            3. Provide recommendations
            
            Focus on over-budget items and significant underspend.
            """,
            expected_output="Budget variance analysis with alerts and recommendations.",
            agent=self.agent
        )

    def check_donor_compliance(self, donor_name: str, category: str = "reporting") -> CrewTask:
        return CrewTask(
            description=f"""
            Check compliance requirements for: {donor_name}
            
            Category: {category}
            
            Use check_donor_guidelines tool to retrieve:
            1. Reporting requirements
            2. Eligibility criteria
            3. Budget restrictions
            4. Compliance keywords
            """,
            expected_output="Donor compliance requirements summary.",
            agent=self.agent
        )

    def generate_donor_report(self, budget_id: str, donor_name: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Generate a donor compliance report for: {donor_name}
            
            Budget period: {budget_id}
            
            Use generate_donor_report tool to create a report that:
            1. Summarizes budget status
            2. Lists compliance items
            3. Identifies next steps
            """,
            expected_output="Donor-specific compliance report.",
            agent=self.agent
        )

    def review_financial_health(self, budget_ids: List[str]) -> CrewTask:
        return CrewTask(
            description=f"""
            Review financial health across budgets: {', '.join(budget_ids)}
            
            For each budget:
            1. Use analyze_budget_variance
            2. Identify trends
            3. Flag concerns
            
            Provide an overall assessment of organizational financial health.
            """,
            expected_output="Comprehensive financial health review.",
            agent=self.agent
        )

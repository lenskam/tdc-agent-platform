from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.dhis2_tools import dhis2_tools
from ..tools.data_processor import data_processor_tools


class DataAnalystAgent(BaseTDCAgent):
    def __init__(self):
        all_tools = dhis2_tools + data_processor_tools
        super().__init__(
            role="Senior Data Analyst",
            goal="Provide accurate data insights, ensure data quality, and generate actionable analytics for health information systems.",
            backstory="""You are a Senior Data Analyst at TDC Consulting with extensive experience in DHIS2 and health information systems.
            You specialize in data quality assurance, statistical analysis, and generating meaningful insights from health data.
            
            Your expertise includes:
            - DHIS2 analytics and metadata management
            - Data cleaning and quality assurance using Pandas
            - Statistical analysis and outlier detection
            - Health indicator interpretation
            
            You always ensure data privacy and use local processing for sensitive data.
            Only use LLMs for code generation and interpreting aggregate statistics.""",
            tools=all_tools,
            capability="smart"
        )

    def fetch_health_data(self, indicators: str, period: str, org_unit: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Fetch health data from DHIS2 for analysis.
            
            Indicators: {indicators}
            Period: {period}
            Organisation Unit: {org_unit}
            
            Use the fetch_dhis2_analytics tool to retrieve the data.
            Provide a summary of the data including record counts and key values.
            """,
            expected_output="Summary of fetched health data with key metrics.",
            agent=self.agent
        )

    def analyze_dataset(self, file_path: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Analyze the dataset at: {file_path}
            
            Your task:
            1. Generate descriptive statistics using generate_statistics
            2. Detect outliers using detect_outliers
            3. Identify data quality issues (missing values, duplicates)
            4. Provide actionable insights
            
            Use the data_processor tools to perform the analysis.
            """,
            expected_output="Comprehensive data analysis with statistics and insights.",
            agent=self.agent
        )

    def clean_data(
        self,
        file_path: str,
        remove_duplicates: bool = True,
        fill_nulls_method: str = "mean"
    ) -> CrewTask:
        return CrewTask(
            description=f"""
            Clean the dataset at: {file_path}
            
            Cleaning steps:
            - Remove duplicates: {remove_duplicates}
            - Fill null values: {fill_nulls_method}
            
            Use the clean_dataset tool to process the data.
            Report on what was cleaned and provide the output file path.
            """,
            expected_output="Cleaning report with output file path and summary.",
            agent=self.agent
        )

    def check_data_quality(self, file_path: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Perform a comprehensive data quality check on: {file_path}
            
            Check for:
            1. Missing values and their distribution
            2. Duplicate records
            3. Outliers in numeric columns
            4. Data type consistency
            
            Use generate_statistics and detect_outliers tools.
            Provide a quality score and recommendations.
            """,
            expected_output="Data quality report with score and recommendations.",
            agent=self.agent
        )

    def full_analysis(self, file_path: str, dhis2_indicators: str = "") -> CrewTask:
        return CrewTask(
            description=f"""
            Perform a complete data analysis workflow on: {file_path}
            
            {f'Also fetch related data from DHIS2 indicators: {dhis2_indicators}' if dhis2_indicators else ''}
            
            Your workflow:
            1. Generate descriptive statistics
            2. Detect outliers and anomalies
            3. Check data quality
            4. Clean the data if needed
            5. Provide key insights and recommendations
            
            Use appropriate tools at each step.
            Produce a comprehensive analysis report.
            """,
            expected_output="Complete analysis report with insights and recommendations.",
            agent=self.agent
        )

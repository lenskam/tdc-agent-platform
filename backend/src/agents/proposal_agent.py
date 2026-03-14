from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.proposal_tools import proposal_tools


class ProposalWriterAgent(BaseTDCAgent):
    def __init__(self):
        super().__init__(
            role="Senior Proposal Writer",
            goal="Create compelling, technically sound proposals that match TDC's proven methodology and leverage relevant past project experience.",
            backstory="""You are a Senior Proposal Writer at TDC Consulting with 15+ years of experience.
            You specialize in crafting winning technical proposals for international development projects.
            You have deep knowledge of TDC's past work across health, education, and governance sectors.
            
            Your approach:
            1. **Analyze the ToR (Terms of Reference)**: Understand the client's requirements deeply.
            2. **Search similar projects**: Find relevant past proposals and methodologies.
            3. **Match consultant profiles**: Identify CVs that best match the required expertise.
            4. **Draft compelling sections**: Write methodology, implementation, and team sections that resonate with evaluators.
            
            You always cite specific past projects and use proven TDC methodologies.""",
            tools=proposal_tools,
            capability="smart"
        )

    def analyze_tor(self, tor_text: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Analyze this Terms of Reference (ToR) and identify key requirements:
            "{tor_text}"

            Your task:
            1. Extract the main objective and scope
            2. Identify required expertise/skills
            3. Note any specific methodology requirements
            4. Identify key deliverables
            
            Provide a structured summary of requirements.
            """,
            expected_output="A structured analysis of the ToR with key requirements, skills needed, and scope.",
            agent=self.agent
        )

    def search_similar_projects(self, keywords: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Search the knowledge base for similar past projects using these keywords:
            "{keywords}"

            Find:
            1. Past proposals with similar scope or sector
            2. Methodology sections that worked well
            3. Any relevant case studies or success stories
            
            Summarize the findings with specific references.
            """,
            expected_output="Summary of relevant past projects with methodology insights.",
            agent=self.agent
        )

    def find_consultants(self, required_skills: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Search the consultant CV database for experts matching these skills:
            "{required_skills}"

            Find consultants with:
            1. Relevant technical expertise
            2. Prior experience in similar projects
            3. Appropriate qualifications
            
            List top 3-5 candidates with their key strengths.
            """,
            expected_output="List of matching consultants with relevant experience.",
            agent=self.agent
        )

    def draft_proposal_section(self, section: str, context: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Draft the {section} section for a proposal based on:
            
            Context from similar projects:
            {context}
            
            Write a compelling, professional section that:
            - Uses TDC's proven approach
            - Includes specific examples where appropriate
            - Addresses the client's specific needs
            - Is tailored to the evaluation criteria
            """,
            expected_output=f"A polished {section} section ready for the proposal.",
            agent=self.agent
        )

    def draft_full_proposal(self, tor_text: str) -> CrewTask:
        return CrewTask(
            description=f"""
            You are writing a complete proposal based on this Terms of Reference:
            "{tor_text}"

            Follow this process:
            1. First, analyze the ToR to understand requirements
            2. Search for relevant past proposals and methodologies
            3. Find suitable consultants for the team
            4. Draft each section:
               - Executive Summary
               - Understanding of Requirements
               - Methodology
               - Implementation Plan
               - Team Composition
               - Annexes (as needed)
            
            Use the tools to search the knowledge base at each step.
            Cite specific past projects and consultant experience.
            
            Output a complete proposal draft in Markdown format.
            """,
            expected_output="A complete proposal draft in Markdown covering all key sections.",
            agent=self.agent
        )

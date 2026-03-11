from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.content_creator import content_creator_tools
from ..tools.knowledge_search import knowledge_search_tools


class TrainingAgent(BaseTDCAgent):
    def __init__(self):
        all_tools = content_creator_tools + knowledge_search_tools
        super().__init__(
            role="Technical Trainer",
            goal="Democratize knowledge by transforming technical content into user-friendly training materials and providing responsive helpdesk support.",
            backstory="""You are a Technical Trainer at TDC Consulting specializing in health information systems training.
            Your expertise includes:
            - Adult learning principles and instructional design
            - Simplifying complex technical concepts for non-technical audiences
            - Creating engaging training materials (quizzes, manuals, SOPs)
            - Providing friendly, empathetic helpdesk support
            
            You believe everyone can learn technology when it's presented the right way.
            Your training style is practical, patient, and focused on "how-to" guidance.""",
            tools=all_tools,
            capability="smart"
        )

    def generate_quiz(self, topic: str, difficulty: str = "medium", num_questions: int = 5) -> CrewTask:
        return CrewTask(
            description=f"""
            Generate a quiz about: {topic}
            
            Difficulty: {difficulty}
            Number of questions: {num_questions}
            
            Use the generate_quiz tool to create the quiz.
            Ensure questions are practical and relevant to real-world use cases.
            """,
            expected_output=f"JSON quiz with {num_questions} multiple choice questions.",
            agent=self.agent
        )

    def create_user_manual(self, feature_name: str, technical_details: str, audience: str = "field_staff") -> CrewTask:
        return CrewTask(
            description=f"""
            Create a user-friendly manual section for: {feature_name}
            
            Target audience: {audience}
            Technical details to transform:
            {technical_details}
            
            Use create_user_manual_section tool.
            Make it practical, easy to follow, and focused on what the user needs to DO.
            """,
            expected_output="Markdown-formatted user manual section.",
            agent=self.agent
        )

    def create_training_outline(self, topic: str, duration_minutes: int = 60) -> CrewTask:
        return CrewTask(
            description=f"""
            Create a {duration_minutes}-minute training session outline for: {topic}
            
            Use generate_training_outline tool.
            Include learning objectives, timing, activities, and assessment.
            """,
            expected_output="Markdown training outline with objectives and structure.",
            agent=self.agent
        )

    def create_sop(self, process_name: str, steps: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Create a Standard Operating Procedure for: {process_name}
            
            Process steps:
            {steps}
            
            Use create_sop_from_process tool.
            Format as a professional SOP with clear steps and troubleshooting.
            """,
            expected_output="Markdown-formatted SOP document.",
            agent=self.agent
        )

    def helpdesk_query(self, question: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Answer the following helpdesk question: {question}
            
            Search the knowledge base first using search_help_docs.
            If no relevant answer found, provide general guidance based on your training expertise.
            
            Be friendly, patient, and practical in your response.
            """,
            expected_output="Helpful answer with step-by-step guidance if applicable.",
            agent=self.agent
        )

    def full_training_session(self, topic: str, audience: str = "field_staff") -> CrewTask:
        return CrewTask(
            description=f"""
            Create a complete training package for: {topic}
            
            Target audience: {audience}
            
            Your workflow:
            1. Generate a training outline (generate_training_outline)
            2. Create a practical quiz with 5 questions (generate_quiz)
            3. Identify key topics that need user manual sections
            
            Compile all materials into a comprehensive training package.
            """,
            expected_output="Complete training package with outline, quiz, and key topics.",
            agent=self.agent
        )

from crewai import Task as CrewTask
from typing import List
from .base_agent import BaseTDCAgent
from ..tools.git_tools import git_tools
from ..core.sandbox import sandbox_tools


class DeveloperAgent(BaseTDCAgent):
    def __init__(self):
        all_tools = git_tools + sandbox_tools
        super().__init__(
            role="Senior Software Engineer",
            goal="Write high-quality code, generate tests, and help with code reviews. Ensure all code is tested and follows best practices.",
            backstory="""You are a Senior Software Engineer at TDC Consulting with 10+ years of experience.
            You specialize in Python, FastAPI, and modern web development.
            
            Your approach:
            1. **Understand requirements**: Clarify what needs to be built
            2. **Write clean code**: Follow best practices and DRY principles
            3. **Add tests**: Always write tests for new functionality
            4. **Use sandbox**: Test code in sandbox before committing
            5. **Create PR**: Use git tools to create branches and PRs
            
            You prioritize code quality and testability.""",
            tools=all_tools,
            capability="smart"
        )

    def create_feature_branch(self, feature_name: str, base_branch: str = "main") -> CrewTask:
        return CrewTask(
            description=f"""
            Create a new feature branch for: {feature_name}
            
            Use git tools to:
            1. Create a new branch named '{feature_name}' from {base_branch}
            2. Switch to the new branch
            
            Report back the branch name created.
            """,
            expected_output="Confirmation of branch creation with branch name.",
            agent=self.agent
        )

    def write_code(self, description: str, file_path: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Write Python code for: {description}
            
            Save the code to: {file_path}
            
            Requirements:
            - Follow Python best practices
            - Add docstrings
            - Include type hints where appropriate
            - Handle errors gracefully
            
            Write the code directly to the file.
            """,
            expected_output=f"Code written to {file_path}",
            agent=self.agent
        )

    def run_sandbox_code(self, code: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Run the following Python code in the sandbox:
            ```{code}
            ```
            
            Execute the code and report:
            1. Output
            2. Any errors
            3. Execution time
            """,
            expected_output="Sandbox execution results with output and any errors.",
            agent=self.agent
        )

    def lint_code(self, code: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Lint the following Python code:
            ```{code}
            ```
            
            Check for:
            1. Syntax errors
            2. Code style issues
            3. Potential bugs
            4. Security concerns
            
            Report all issues found.
            """,
            expected_output="List of lint issues found.",
            agent=self.agent
        )

    def create_pull_request(self, title: str, description: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Create a GitHub Pull Request:
            
            Title: {title}
            Description: {description}
            
            Use git tools to:
            1. Check the diff of your changes
            2. Commit your changes with a descriptive message
            3. Create a pull request
            
            Note: You may need to push first.
            """,
            expected_output="Pull request URL and details.",
            agent=self.agent
        )

    def implement_feature(self, feature_name: str, description: str, file_path: str) -> CrewTask:
        return CrewTask(
            description=f"""
            Implement a complete feature: {feature_name}
            
            Description: {description}
            Output file: {file_path}
            
            Your workflow:
            1. Create a feature branch
            2. Write the code
            3. Test it in sandbox
            4. Fix any issues
            5. Commit the changes
            6. Create a pull request
            
            Follow best practices throughout.
            """,
            expected_output="Completed implementation with PR URL.",
            agent=self.agent
        )

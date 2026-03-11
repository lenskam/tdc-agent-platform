import json
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from ..core.llm_router import llm_router


@tool
def generate_quiz(topic: str, difficulty: str = "medium", num_questions: int = 5) -> str:
    """
    Generate a quiz with multiple choice questions on a given topic.

    Args:
        topic: The topic for the quiz (e.g., "DHIS2 data entry", "HIV surveillance")
        difficulty: Difficulty level - "easy", "medium", or "hard"
        num_questions: Number of questions to generate (default 5)

    Returns:
        JSON string containing quiz questions with answers
    """
    difficulty_prompts = {
        "easy": "basic concepts and definitions",
        "medium": "practical applications and procedures",
        "advanced": "edge cases, troubleshooting, and optimization"
    }

    prompt = f"""Generate a {num_questions}-question multiple choice quiz about "{topic}" at {difficulty} difficulty.

Format the output as a JSON array with this structure:
[
  {{
    "question": "Question text here?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A) Option 1",
    "explanation": "Brief explanation of why this is correct"
  }}
]

Requirements:
- Questions should test {difficulty_prompts.get(difficulty, difficulty_prompts['medium'])}
- Each question must have exactly 4 options
- Include a brief explanation for the correct answer
- Make questions practical and relevant to real-world use cases"""

    llm = llm_router.get_model(capability="smart")
    response = llm.invoke(prompt)

    try:
        quiz_data = json.loads(response.content)
        return json.dumps(quiz_data, indent=2)
    except json.JSONDecodeError:
        return json.dumps([
            {"error": "Failed to parse quiz generation", "raw_response": response.content}
        ])


@tool
def create_user_manual_section(feature_name: str, technical_details: str, audience: str = "field_staff") -> str:
    """
    Transform technical specifications into user-friendly manual sections.

    Args:
        feature_name: Name of the feature or function
        technical_details: Technical specifications or documentation to simplify
        audience: Target audience - "field_staff", "supervisors", or "technical"

    Returns:
        Markdown-formatted user manual section
    """
    audience_styles = {
        "field_staff": "Use simple language, avoid jargon, focus on step-by-step instructions. Include warnings about common mistakes.",
        "supervisors": "Include both practical steps and rationale. Add tips for monitoring team performance.",
        "technical": "Include technical details, configuration options, and troubleshooting steps."
    }

    style_guide = audience_styles.get(audience, audience_styles["field_staff"])

    prompt = f"""Transform the following technical documentation for {feature_name} into a user-friendly manual section.

Target audience: {audience}
Style guide: {style_guide}

Technical Details:
{technical_details}

Output format should be Markdown with:
1. A clear title
2. A brief "What is this?" section (1-2 sentences)
3. Step-by-step instructions (numbered)
4. Important tips or warnings (if applicable)
5. A "Need help?" section with common issues

Make it practical, easy to follow, and focused on what the user needs to DO."""

    llm = llm_router.get_model(capability="smart")
    response = llm.invoke(prompt)

    return response.content


@tool
def generate_training_outline(topic: str, duration_minutes: int = 60) -> str:
    """
    Generate a training session outline with objectives and content.

    Args:
        topic: The training topic
        duration_minutes: Expected session duration in minutes

    Returns:
        Markdown-formatted training outline
    """
    prompt = f"""Create a {duration_minutes}-minute training session outline for: {topic}

Include:
1. Learning objectives (3-5 bullet points)
2. Session structure with timing
3. Key concepts to cover
4. Hands-on exercises or activities
5. Assessment method
6. Resources for further learning

Format as clean Markdown suitable for a trainer."""

    llm = llm_router.get_model(capability="smart")
    response = llm.invoke(prompt)

    return response.content


@tool
def create_sop_from_process(process_name: str, steps: str) -> str:
    """
    Create a Standard Operating Procedure (SOP) from process steps.

    Args:
        process_name: Name of the process
        steps: Raw process steps or description

    Returns:
        Markdown-formatted SOP document
    """
    prompt = f"""Create a Standard Operating Procedure (SOP) for: {process_name}

Process Steps:
{steps}

Format as a professional SOP with:
1. Purpose and scope
2. Roles and responsibilities
3. Prerequisites
4. Step-by-step procedure (numbered, with clear actions)
5. Expected outcomes
6. Troubleshooting common issues
7. Related documents

Use clear, action-oriented language."""

    llm = llm_router.get_model(capability="smart")
    response = llm.invoke(prompt)

    return response.content


content_creator_tools = [
    generate_quiz,
    create_user_manual_section,
    generate_training_outline,
    create_sop_from_process
]

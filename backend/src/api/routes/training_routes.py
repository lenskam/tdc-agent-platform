from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from ...agents.training_agent import TrainingAgent
from crewai import Crew

router = APIRouter()

class QuizRequest(BaseModel):
    topic: str
    difficulty: str = "medium"
    num_questions: int = 5

class HelpdeskRequest(BaseModel):
    question: str

class ManualRequest(BaseModel):
    feature_name: str
    technical_details: str
    audience: str = "field_staff"

class TrainingOutlineRequest(BaseModel):
    topic: str
    duration_minutes: int = 60


@router.post("/training/quiz")
async def generate_quiz(request: QuizRequest):
    """
    Generate a quiz on a given topic.
    """
    try:
        training_agent = TrainingAgent()
        task = training_agent.generate_quiz(
            topic=request.topic,
            difficulty=request.difficulty,
            num_questions=request.num_questions
        )
        
        crew = Crew(
            agents=[training_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"quiz": str(result), "topic": request.topic, "difficulty": request.difficulty}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/training/helpdesk")
async def helpdesk_query(request: HelpdeskRequest):
    """
    Answer a helpdesk question using the knowledge base.
    """
    try:
        training_agent = TrainingAgent()
        task = training_agent.helpdesk_query(request.question)
        
        crew = Crew(
            agents=[training_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"response": str(result), "question": request.question}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/training/manual")
async def create_manual(request: ManualRequest):
    """
    Create a user-friendly manual section from technical details.
    """
    try:
        training_agent = TrainingAgent()
        task = training_agent.create_user_manual(
            feature_name=request.feature_name,
            technical_details=request.technical_details,
            audience=request.audience
        )
        
        crew = Crew(
            agents=[training_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"manual": str(result), "feature": request.feature_name}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/training/outline")
async def create_outline(request: TrainingOutlineRequest):
    """
    Create a training session outline.
    """
    try:
        training_agent = TrainingAgent()
        task = training_agent.create_training_outline(
            topic=request.topic,
            duration_minutes=request.duration_minutes
        )
        
        crew = Crew(
            agents=[training_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"outline": str(result), "topic": request.topic}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ...agents.pm_agent import ProjectManagerAgent
from crewai import Crew

router = APIRouter()

class ProjectPlanRequest(BaseModel):
    description: str

@router.post("/pm/plan")
async def plan_project(request: ProjectPlanRequest):
    """
    Trigger the Project Manager Agent to create a project plan.
    """
    try:
        # Initialize Agent
        pm_agent = ProjectManagerAgent()
        
        # Create Task
        task = pm_agent.plan_project(request.description)
        
        # Create Crew (Single agent for now)
        crew = Crew(
            agents=[pm_agent.get_agent()],
            tasks=[task]
        )
        
        # Execute
        result = crew.kickoff()
        
        return {"result": result}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

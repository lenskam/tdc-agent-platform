from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ...agents.director_agent import DirectorAgent
from crewai import Crew

router = APIRouter()

class RiskSummaryRequest(BaseModel):
    time_period: str = "30_days"

class AuditRequest(BaseModel):
    time_window_hours: int = 24
    sensitivity: str = "medium"

class StrategicReportRequest(BaseModel):
    include_finance: bool = True
    include_operations: bool = True

class AgentCompareRequest(BaseModel):
    agent_list: List[str]


@router.post("/director/risks")
async def summarize_risks(request: RiskSummaryRequest):
    """
    Summarize key risks across the organization.
    """
    try:
        director_agent = DirectorAgent()
        task = director_agent.summarize_risks(request.time_period)
        
        crew = Crew(
            agents=[director_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"result": str(result), "time_period": request.time_period}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/director/audit")
async def audit_system(request: AuditRequest):
    """
    Audit system for anomalies and suspicious behavior.
    """
    try:
        director_agent = DirectorAgent()
        task = director_agent.audit_system_health(request.time_window_hours)
        
        crew = Crew(
            agents=[director_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"result": str(result), "time_window": request.time_window_hours}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/director/strategic")
async def generate_strategic_report(request: StrategicReportRequest):
    """
    Generate comprehensive strategic report.
    """
    try:
        director_agent = DirectorAgent()
        task = director_agent.generate_strategic_report(
            request.include_finance,
            request.include_operations
        )
        
        crew = Crew(
            agents=[director_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"result": str(result)}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

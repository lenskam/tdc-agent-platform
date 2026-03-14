from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from ...agents.finance_agent import FinanceAgent
from crewai import Crew

router = APIRouter()

class BudgetAnalysisRequest(BaseModel):
    budget_id: str

class DonorComplianceRequest(BaseModel):
    donor_name: str
    category: Optional[str] = "reporting"

class DonorReportRequest(BaseModel):
    budget_id: str
    donor_name: str


@router.post("/finance/analyze")
async def analyze_budget(request: BudgetAnalysisRequest):
    """
    Analyze budget variance for a given budget ID.
    """
    try:
        finance_agent = FinanceAgent()
        task = finance_agent.analyze_budget(request.budget_id)
        
        crew = Crew(
            agents=[finance_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"result": str(result), "budget_id": request.budget_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/finance/compliance")
async def check_compliance(request: DonorComplianceRequest):
    """
    Check donor compliance guidelines.
    """
    try:
        finance_agent = FinanceAgent()
        task = finance_agent.check_donor_compliance(request.donor_name, request.category)
        
        crew = Crew(
            agents=[finance_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"result": str(result), "donor": request.donor_name}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/finance/report")
async def generate_donor_report(request: DonorReportRequest):
    """
    Generate donor compliance report.
    """
    try:
        finance_agent = FinanceAgent()
        task = finance_agent.generate_donor_report(request.budget_id, request.donor_name)
        
        crew = Crew(
            agents=[finance_agent.get_agent()],
            tasks=[task]
        )
        
        result = crew.kickoff()
        
        return {"result": str(result), "budget_id": request.budget_id, "donor": request.donor_name}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

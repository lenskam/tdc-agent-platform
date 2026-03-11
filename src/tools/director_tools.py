import json
from typing import List, Dict, Any, Optional
from langchain_core.tools import tool
from ..tools.audit_tools import get_agent_activity_summary, scan_logs_for_anomalies
from ..tools.finance_tools import read_budget_sheet, analyze_budget_variance


@tool
def query_all_agent_logs(agent_filter: Optional[str] = None, action_filter: Optional[str] = None) -> str:
    """
    Query logs across all agents with optional filtering.

    Args:
        agent_filter: Filter by specific agent (e.g., "pm_agent", "data_agent")
        action_filter: Filter by action type (e.g., "plan_project", "fetch_dhis2")

    Returns:
        JSON string with filtered log entries
    """
    from ..tools.audit_tools import MOCK_LOGS
    
    logs = MOCK_LOGS
    
    if agent_filter:
        logs = [log for log in logs if log["agent"] == agent_filter]
    
    if action_filter:
        logs = [log for log in logs if log["action"] == action_filter]
    
    return json.dumps({
        "total_logs": len(logs),
        "filters": {
            "agent": agent_filter,
            "action": action_filter
        },
        "logs": logs
    }, indent=2)


@tool
def summarize_key_risks(time_period: str = "30_days") -> str:
    """
    Summarize key risks identified across all projects and agents.

    Args:
        time_period: Time period to analyze - "7_days", "30_days", "90_days"

    Returns:
        JSON string with risk summary
    """
    risk_data = {
        "project_risks": [
            {"project": "Health MIS", "risk": "Staff turnover", "severity": "high", "mitigation": "Cross-train team members"},
            {"project": "Health MIS", "risk": "DHIS2 API rate limits", "severity": "medium", "mitigation": "Implement caching"},
            {"project": "HIV Surveillance", "risk": "Data quality issues", "severity": "high", "mitigation": "Enhanced validation rules"},
            {"project": "TB Program", "risk": "Procurement delays", "severity": "medium", "mitigation": "Early ordering"},
        ],
        "budget_risks": [
            {"category": "Equipment", "risk": "Overspend Q1", "severity": "medium", "amount": 3000},
            {"category": "Personnel", "risk": "Underspend Q1", "severity": "low", "amount": 5000},
        ],
        "compliance_risks": [
            {"area": "USAID reporting", "risk": "Q1 report delayed", "severity": "high"},
            {"area": "Data privacy", "risk": "PII in logs", "severity": "medium"},
        ]
    }
    
    period_mapping = {
        "7_days": 7,
        "30_days": 30,
        "90_days": 90
    }
    
    days = period_mapping.get(time_period, 30)
    
    summary = {
        "time_period": time_period,
        "total_risks": len(risk_data["project_risks"]) + len(risk_data["budget_risks"]) + len(risk_data["compliance_risks"]),
        "high_severity_count": sum(1 for r in risk_data["project_risks"] + risk_data["budget_risks"] + risk_data["compliance_risks"] if r["severity"] == "high"),
        "by_category": {
            "project": len(risk_data["project_risks"]),
            "budget": len(risk_data["budget_risks"]),
            "compliance": len(risk_data["compliance_risks"])
        },
        "risks": risk_data,
        "recommendations": [
            "Address high-severity risks immediately",
            "Review budget variance in Equipment category",
            "Submit USAID Q1 report before deadline"
        ]
    }
    
    return json.dumps(summary, indent=2)


@tool
def generate_strategic_report(include_finance: bool = True, include_operations: bool = True) -> str:
    """
    Generate a comprehensive strategic report synthesizing data from multiple agents.

    Args:
        include_finance: Include financial data in the report
        include_operations: Include operational data in the report

    Returns:
        JSON string with strategic report
    """
    from ..tools.audit_tools import get_agent_activity_summary
    
    report = {
        "report_type": "Monthly Strategic Summary",
        "generated_at": "2026-03-11",
        "period": "February 2026",
        "executive_summary": "Overall organizational health is stable with some areas requiring attention.",
        "key_highlights": [
            "Successfully delivered 3 major proposals",
            "DHIS2 integration on track",
            "Training program expanded to 50 new users"
        ],
        "areas_of_concern": [
            "Budget overspend in Equipment category",
            "Staff capacity stretched thin",
            "USAID reporting timeline tight"
        ]
    }
    
    if include_finance:
        report["finance_summary"] = {
            "budget_status": "On track with minor variances",
            "utilization": "78%",
            "donor_compliance": "Compliant"
        }
    
    if include_operations:
        activity = json.loads(get_agent_activity_summary.invoke(days=30))
        report["operations_summary"] = {
            "total_agent_actions": activity["total_actions"],
            "most_active_agent": activity["most_active_agent"],
            "key_activities": activity["by_action_type"]
        }
    
    report["next_month_priorities"] = [
        "Submit USAID Q1 report",
        "Complete staff recruitment for TB program",
        "Implement DHIS2 caching layer",
        "Launch training program Phase 2"
    ]
    
    return json.dumps(report, indent=2)


@tool
def compare_agent_performance(agent_list: List[str]) -> str:
    """
    Compare performance metrics across multiple agents.

    Args:
        agent_list: List of agent names to compare

    Returns:
        JSON string with performance comparison
    """
    from ..tools.audit_tools import get_agent_activity_summary
    
    comparison = {
        "agents_compared": agent_list,
        "metrics": []
    }
    
    for agent in agent_list:
        activity = json.loads(get_agent_activity_summary.invoke(agent_name=agent, days=30))
        comparison["metrics"].append({
            "agent": agent,
            "total_actions": activity["total_actions"],
            "activity_breakdown": activity["by_action_type"]
        })
    
    return json.dumps(comparison, indent=2)


director_tools = [
    query_all_agent_logs,
    summarize_key_risks,
    generate_strategic_report,
    compare_agent_performance
]

import json
import re
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from langchain_core.tools import tool


MOCK_LOGS = []


def _add_log_entry(agent_name: str, action: str, details: str, status: str = "success"):
    MOCK_LOGS.append({
        "timestamp": datetime.now().isoformat(),
        "agent": agent_name,
        "action": action,
        "details": details,
        "status": status
    })


_sample_logs = [
    {"timestamp": "2026-03-11T08:00:00", "agent": "pm_agent", "action": "plan_project", "details": "Created project plan for Health MIS", "status": "success"},
    {"timestamp": "2026-03-11T08:15:00", "agent": "pm_agent", "action": "update_task", "details": "Updated task status to in_progress", "status": "success"},
    {"timestamp": "2026-03-11T08:30:00", "agent": "proposal_agent", "action": "generate_proposal", "details": "Generated proposal for USAID bid", "status": "success"},
    {"timestamp": "2026-03-11T09:00:00", "agent": "data_agent", "action": "fetch_dhis2", "details": "Fetched HIV indicators for Q4", "status": "success"},
    {"timestamp": "2026-03-11T09:30:00", "agent": "developer_agent", "action": "execute_code", "details": "Ran data processing script", "status": "success"},
    {"timestamp": "2026-03-11T10:00:00", "agent": "devops_agent", "action": "deploy_service", "details": "Deployed dashboard to staging", "status": "success"},
    {"timestamp": "2026-03-11T10:30:00", "agent": "training_agent", "action": "generate_quiz", "details": "Created quiz on DHIS2 basics", "status": "success"},
    {"timestamp": "2026-03-11T11:00:00", "agent": "pm_agent", "action": "analyze_risks", "details": "Identified 3 project risks", "status": "success"},
]

for log in _sample_logs:
    MOCK_LOGS.append(log)


@tool
def scan_logs_for_anomalies(time_window_hours: int = 24, sensitivity: str = "medium") -> str:
    """
    Scan agent logs for anomalies and suspicious behavior patterns.

    Args:
        time_window_hours: Number of hours to look back (default 24)
        sensitivity: Detection sensitivity - "low", "medium", or "high"

    Returns:
        JSON string with detected anomalies and alerts
    """
    sensitivity_thresholds = {
        "low": {"error_rate": 0.3, "action_count": 100},
        "medium": {"error_rate": 0.15, "action_count": 50},
        "high": {"error_rate": 0.05, "action_count": 20}
    }
    
    threshold = sensitivity_thresholds.get(sensitivity, sensitivity_thresholds["medium"])
    
    cutoff_time = datetime.now() - timedelta(hours=time_window_hours)
    recent_logs = [
        log for log in MOCK_LOGS
        if datetime.fromisoformat(log["timestamp"]) >= cutoff_time
    ]
    
    agent_stats = {}
    anomalies = []
    
    for log in recent_logs:
        agent = log["agent"]
        if agent not in agent_stats:
            agent_stats[agent] = {"total": 0, "errors": 0, "actions": set()}
        
        agent_stats[agent]["total"] += 1
        agent_stats[agent]["actions"].add(log["action"])
        
        if log["status"] == "error" or log["status"] == "failed":
            agent_stats[agent]["errors"] += 1
        
        if log["action"] in ["execute_code", "deploy_service", "write_file"]:
            if "sensitive" in log.get("details", "").lower():
                anomalies.append({
                    "type": "sensitive_operation",
                    "agent": agent,
                    "timestamp": log["timestamp"],
                    "details": log["details"],
                    "severity": "high"
                })
    
    alerts = []
    for agent, stats in agent_stats.items():
        error_rate = stats["errors"] / stats["total"] if stats["total"] > 0 else 0
        
        if error_rate > threshold["error_rate"]:
            alerts.append({
                "type": "high_error_rate",
                "agent": agent,
                "error_rate": round(error_rate * 100, 2),
                "total_actions": stats["total"],
                "severity": "high" if error_rate > 0.2 else "medium"
            })
        
        if stats["total"] > threshold["action_count"]:
            alerts.append({
                "type": "high_activity",
                "agent": agent,
                "action_count": stats["total"],
                "severity": "low"
            })
    
    result = {
        "scan_summary": {
            "time_window_hours": time_window_hours,
            "logs_analyzed": len(recent_logs),
            "agents_acting": len(agent_stats),
            "anomalies_found": len(anomalies),
            "alerts_generated": len(alerts)
        },
        "anomalies": anomalies,
        "alerts": alerts,
        "recommendation": "Review high severity alerts" if any(a.get("severity") == "high" for a in alerts) else "No critical issues found"
    }
    
    return json.dumps(result, indent=2)


@tool
def verify_compliance(text: str, donor_name: Optional[str] = None) -> str:
    """
    Verify if a proposal or report complies with donor guidelines and keywords.

    Args:
        text: The text to check for compliance
        donor_name: Optional donor to check specific guidelines

    Returns:
        JSON string with compliance analysis
    """
    donor_keywords = {
        "USAID": ["GMS", "ASSP", "PMP", "EBola", "financial", "procurement"],
        "PEPFAR": ["DATIM", "MER", "QAR", "COP", "POART", "HIV", "ART"],
        "WorldBank": ["PforR", "ESMF", "financing", "procurement"]
    }
    
    required_sections = {
        "USAID": ["budget", "timeline", "monitoring", "evaluation"],
        "PEPFAR": ["HIV", "ART", "testing", "treatment"],
        "WorldBank": ["environmental", "procurement", "financial"]
    }
    
    issues = []
    warnings = []
    passed = []
    
    text_lower = text.lower()
    
    if donor_name:
        keywords = donor_keywords.get(donor_name, [])
        required = required_sections.get(donor_name, [])
        
        for keyword in keywords:
            if keyword.lower() in text_lower:
                passed.append(f"Found required keyword: {keyword}")
            else:
                warnings.append(f"Missing recommended keyword: {keyword}")
        
        for section in required:
            if section in text_lower:
                passed.append(f"Found section: {section}")
            else:
                issues.append(f"Missing required section: {section}")
    else:
        general_keywords = ["budget", "timeline", "objectives", "monitoring", "evaluation"]
        for keyword in general_keywords:
            if keyword in text_lower:
                passed.append(f"Found: {keyword}")
    
    score = len(passed) / (len(passed) + len(issues) + len(warnings)) * 100 if (passed or issues or warnings) else 0
    
    result = {
        "compliance_score": round(score, 2),
        "status": "compliant" if score >= 70 and not issues else "needs_review",
        "passed_checks": passed,
        "warnings": warnings,
        "issues": issues,
        "recommendation": "Ready for submission" if score >= 70 else "Address issues before submission"
    }
    
    return json.dumps(result, indent=2)


@tool
def get_agent_activity_summary(agent_name: Optional[str] = None, days: int = 7) -> str:
    """
    Get a summary of agent activity for audit purposes.

    Args:
        agent_name: Optional specific agent to query (default: all agents)
        days: Number of days to look back

    Returns:
        JSON string with activity summary
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    
    if agent_name:
        logs = [
            log for log in MOCK_LOGS
            if log["agent"] == agent_name and datetime.fromisoformat(log["timestamp"]) >= cutoff_date
        ]
    else:
        logs = [
            log for log in MOCK_LOGS
            if datetime.fromisoformat(log["timestamp"]) >= cutoff_date
        ]
    
    agent_counts = {}
    action_counts = {}
    
    for log in logs:
        agent = log["agent"]
        action = log["action"]
        
        agent_counts[agent] = agent_counts.get(agent, 0) + 1
        action_counts[action] = action_counts.get(action, 0) + 1
    
    result = {
        "period_days": days,
        "total_actions": len(logs),
        "by_agent": agent_counts,
        "by_action_type": action_counts,
        "most_active_agent": max(agent_counts.items(), key=lambda x: x[1])[0] if agent_counts else None,
        "most_common_action": max(action_counts.items(), key=lambda x: x[1])[0] if action_counts else None
    }
    
    return json.dumps(result, indent=2)


@tool
def audit_tool_access(tool_name: str, agent_role: str) -> str:
    """
    Audit whether a specific agent role has access to a specific tool.

    Args:
        tool_name: Name of the tool to check
        agent_role: Role of the agent requesting access

    Returns:
        JSON string with access decision and reasoning
    """
    role_permissions = {
        "finance_agent": ["read_budget_sheet", "check_donor_guidelines", "analyze_budget_variance", "generate_donor_report"],
        "director_agent": ["query_all_agent_logs", "summarize_key_risks", "scan_logs_for_anomalies", "verify_compliance"],
        "pm_agent": ["create_project", "add_task", "update_task", "list_tasks", "generate_report"],
        "developer_agent": ["execute_code", "read_file", "write_file"],
        "devops_agent": ["get_docker_status", "get_system_metrics", "deploy_service"],
        "data_agent": ["fetch_dhis2", "clean_data", "generate_statistics"],
        "training_agent": ["generate_quiz", "search_help_docs", "create_user_manual"]
    }
    
    allowed_tools = role_permissions.get(agent_role, [])
    has_access = tool_name in allowed_tools
    
    result = {
        "tool_name": tool_name,
        "agent_role": agent_role,
        "has_access": has_access,
        "decision": "ALLOW" if has_access else "DENY",
        "reason": f"{agent_role} is authorized to use {tool_name}" if has_access else f"{agent_role} is not authorized to use {tool_name}"
    }
    
    return json.dumps(result, indent=2)


audit_tools = [
    scan_logs_for_anomalies,
    verify_compliance,
    get_agent_activity_summary,
    audit_tool_access
]

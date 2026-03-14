from enum import Enum
from typing import Dict, List, Set, Optional
from functools import wraps
import logging

logger = logging.getLogger(__name__)


class AgentRole(str, Enum):
    PM_AGENT = "pm_agent"
    PROPOSAL_AGENT = "proposal_agent"
    DATA_AGENT = "data_agent"
    DEVELOPER_AGENT = "developer_agent"
    DEVOPS_AGENT = "devops_agent"
    TRAINING_AGENT = "training_agent"
    FINANCE_AGENT = "finance_agent"
    DIRECTOR_AGENT = "director_agent"


class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"


ROLE_PERMISSIONS: Dict[AgentRole, Dict[str, Set[Permission]]] = {
    AgentRole.PM_AGENT: {
        "projects": {Permission.READ, Permission.WRITE},
        "tasks": {Permission.READ, Permission.WRITE, Permission.DELETE},
        "reports": {Permission.READ, Permission.WRITE},
        "risks": {Permission.READ, Permission.WRITE},
    },
    AgentRole.PROPOSAL_AGENT: {
        "proposals": {Permission.READ, Permission.WRITE},
        "documents": {Permission.READ, Permission.WRITE},
        "cv_database": {Permission.READ},
    },
    AgentRole.DATA_AGENT: {
        "data": {Permission.READ, Permission.WRITE},
        "dhis2": {Permission.READ, Permission.EXECUTE},
        "statistics": {Permission.READ, Permission.EXECUTE},
    },
    AgentRole.DEVELOPER_AGENT: {
        "code": {Permission.READ, Permission.WRITE, Permission.EXECUTE},
        "files": {Permission.READ, Permission.WRITE},
        "sandbox": {Permission.EXECUTE},
    },
    AgentRole.DEVOPS_AGENT: {
        "infrastructure": {Permission.READ, Permission.EXECUTE},
        "deployments": {Permission.READ, Permission.WRITE, Permission.EXECUTE},
        "logs": {Permission.READ},
    },
    AgentRole.TRAINING_AGENT: {
        "training_materials": {Permission.READ, Permission.WRITE},
        "knowledge_base": {Permission.READ, Permission.WRITE},
        "quizzes": {Permission.READ, Permission.WRITE},
    },
    AgentRole.FINANCE_AGENT: {
        "budgets": {Permission.READ},
        "financial_reports": {Permission.READ},
        "donor_guidelines": {Permission.READ},
    },
    AgentRole.DIRECTOR_AGENT: {
        "all_reports": {Permission.READ},
        "audit_logs": {Permission.READ},
        "strategic_data": {Permission.READ},
        "agent_metrics": {Permission.READ},
    },
}


TOOL_ACCESS: Dict[str, Set[AgentRole]] = {
    "create_project": {AgentRole.PM_AGENT},
    "add_task": {AgentRole.PM_AGENT},
    "update_task": {AgentRole.PM_AGENT},
    "list_tasks": {AgentRole.PM_AGENT},
    "generate_report": {AgentRole.PM_AGENT},
    "analyze_risks": {AgentRole.PM_AGENT},
    "search_proposals": {AgentRole.PROPOSAL_AGENT},
    "match_cv": {AgentRole.PROPOSAL_AGENT},
    "ingest_document": {AgentRole.PROPOSAL_AGENT},
    "fetch_dhis2": {AgentRole.DATA_AGENT},
    "clean_data": {AgentRole.DATA_AGENT},
    "generate_statistics": {AgentRole.DATA_AGENT},
    "detect_outliers": {AgentRole.DATA_AGENT},
    "execute_code": {AgentRole.DEVELOPER_AGENT},
    "read_file": {AgentRole.DEVELOPER_AGENT},
    "write_file": {AgentRole.DEVELOPER_AGENT},
    "get_docker_status": {AgentRole.DEVOPS_AGENT},
    "get_system_metrics": {AgentRole.DEVOPS_AGENT},
    "deploy_service": {AgentRole.DEVOPS_AGENT},
    "generate_quiz": {AgentRole.TRAINING_AGENT},
    "search_help_docs": {AgentRole.TRAINING_AGENT},
    "create_user_manual": {AgentRole.TRAINING_AGENT},
    "read_budget_sheet": {AgentRole.FINANCE_AGENT},
    "check_donor_guidelines": {AgentRole.FINANCE_AGENT},
    "analyze_budget_variance": {AgentRole.FINANCE_AGENT},
    "generate_donor_report": {AgentRole.FINANCE_AGENT},
    "query_all_agent_logs": {AgentRole.DIRECTOR_AGENT},
    "summarize_key_risks": {AgentRole.DIRECTOR_AGENT},
    "generate_strategic_report": {AgentRole.DIRECTOR_AGENT},
    "scan_logs_for_anomalies": {AgentRole.DIRECTOR_AGENT, AgentRole.DIRECTOR_AGENT},
    "verify_compliance": {AgentRole.DIRECTOR_AGENT, AgentRole.DIRECTOR_AGENT},
}


class AccessControlError(Exception):
    pass


class RBAC:
    def __init__(self):
        self.role_permissions = ROLE_PERMISSIONS
        self.tool_access = TOOL_ACCESS
        self._audit_log: List[Dict] = []

    def check_permission(
        self, role: AgentRole, resource: str, permission: Permission
    ) -> bool:
        if role not in self.role_permissions:
            return False
        
        resource_perms = self.role_permissions[role].get(resource, set())
        has_permission = permission in resource_perms
        
        self._log_access(role, resource, permission, has_permission)
        
        return has_permission

    def check_tool_access(self, tool_name: str, role: AgentRole) -> bool:
        allowed_roles = self.tool_access.get(tool_name, set())
        has_access = role in allowed_roles
        
        self._log_tool_access(tool_name, role, has_access)
        
        return has_access

    def _log_access(
        self, role: AgentRole, resource: str, permission: Permission, granted: bool
    ):
        log_entry = {
            "action": "permission_check",
            "role": role.value,
            "resource": resource,
            "permission": permission.value,
            "granted": granted,
        }
        self._audit_log.append(log_entry)
        logger.info(f"Access control: {log_entry}")

    def _log_tool_access(self, tool_name: str, role: AgentRole, granted: bool):
        log_entry = {
            "action": "tool_access",
            "tool": tool_name,
            "role": role.value,
            "granted": granted,
        }
        self._audit_log.append(log_entry)
        logger.info(f"Tool access: {log_entry}")

    def get_audit_log(self, limit: int = 100) -> List[Dict]:
        return self._audit_log[-limit:]

    def get_role_permissions(self, role: AgentRole) -> Dict[str, Set[Permission]]:
        return self.role_permissions.get(role, {})

    def get_allowed_tools(self, role: AgentRole) -> Set[str]:
        allowed = set()
        for tool, roles in self.tool_access.items():
            if role in roles:
                allowed.add(tool)
        return allowed


rbac = RBAC()


def require_permission(resource: str, permission: Permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = kwargs.get("role") or kwargs.get("agent_role")
            if role and isinstance(role, AgentRole):
                if not rbac.check_permission(role, resource, permission):
                    raise AccessControlError(
                        f"Role {role.value} does not have {permission.value} permission for {resource}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_tool_access(tool_name: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            role = kwargs.get("role") or kwargs.get("agent_role")
            if role and isinstance(role, AgentRole):
                if not rbac.check_tool_access(tool_name, role):
                    raise AccessControlError(
                        f"Role {role.value} is not authorized to use tool {tool_name}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

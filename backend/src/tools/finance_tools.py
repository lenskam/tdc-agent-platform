import json
import os
from typing import Dict, List, Any, Optional
from langchain_core.tools import tool


BUDGET_DATA_PATH = os.getenv("BUDGET_DATA_PATH", "./data/budgets")
DONOR_GUIDELINES_PATH = os.getenv("DONOR_GUIDELINES_PATH", "./data/donors")


@tool
def read_budget_sheet(budget_id: str, project_id: Optional[str] = None) -> str:
    """
    Read budget data from the budget sheet. This is READ-ONLY access.

    Args:
        budget_id: The budget identifier (e.g., "Q1_2024", "annual_2024")
        project_id: Optional project ID to filter budget details

    Returns:
        JSON string containing budget data with line items, allocated amounts, and spent amounts
    """
    budget_data = {
        "Q1_2024": {
            "total_budget": 150000,
            "currency": "USD",
            "line_items": [
                {"category": "Personnel", "allocated": 80000, "spent": 75000, "variance": -5000},
                {"category": "Equipment", "allocated": 25000, "spent": 28000, "variance": 3000},
                {"category": "Travel", "allocated": 15000, "spent": 12000, "variance": -3000},
                {"category": "Operations", "allocated": 30000, "spent": 28500, "variance": -1500}
            ],
            "variance_summary": {
                "under_budget": 2,
                "over_budget": 2,
                "total_variance": -2000
            }
        },
        "Q2_2024": {
            "total_budget": 175000,
            "currency": "USD",
            "line_items": [
                {"category": "Personnel", "allocated": 90000, "spent": 88000, "variance": -2000},
                {"category": "Equipment", "allocated": 30000, "spent": 32000, "variance": 2000},
                {"category": "Travel", "allocated": 20000, "spent": 18000, "variance": -2000},
                {"category": "Operations", "allocated": 35000, "spent": 34000, "variance": -1000}
            ],
            "variance_summary": {
                "under_budget": 3,
                "over_budget": 1,
                "total_variance": -3000
            }
        }
    }

    if budget_id in budget_data:
        data = budget_data[budget_id]
        if project_id:
            data["note"] = f"Filtering for project: {project_id}"
        return json.dumps(data, indent=2)
    
    return json.dumps({
        "error": f"Budget '{budget_id}' not found",
        "available_budgets": list(budget_data.keys())
    })


@tool
def check_donor_guidelines(donor_name: str, category: Optional[str] = None) -> str:
    """
    Check donor compliance guidelines and reporting requirements. READ-ONLY access.

    Args:
        donor_name: Name of the donor (e.g., "USAID", "PEPFAR", "WorldBank")
        category: Optional category filter (e.g., "reporting", "eligibility", "budget")

    Returns:
        JSON string with donor guidelines and compliance requirements
    """
    donor_guidelines = {
        "USAID": {
            "reporting_frequency": "Quarterly",
            "required_reports": [
                "Financial Status Report (FSR)",
                "Program Progress Report (PPR)",
                "Annual Audit"
            ],
            "eligibility_requirements": [
                "Non-profit registration",
                "Demonstrated technical capacity",
                "Financial management systems"
            ],
            "budget_restrictions": [
                "Administrative costs max 15%",
                "Equipment purchases require prior approval",
                "Travel must be economy class"
            ],
            "compliance_keywords": [
                "GMS", "ASSP", "PMP", "EBola", "F", "financial", "procurement"
            ]
        },
        "PEPFAR": {
            "reporting_frequency": "Semi-annually",
            "required_reports": [
                "Program Area Dashboard",
                "Financial Dashboard",
                "Site Inventory Report"
            ],
            "eligibility_requirements": [
                "Ministry of Health partnership",
                "HIV/AIDS focus",
                "Data quality requirements"
            ],
            "budget_restrictions": [
                "ARV procurement guidelines",
                "Staffing ratios",
                "Laboratory equipment standards"
            ],
            "compliance_keywords": [
                "DATIM", "MER", "QAR", "COP", "POART", "HIV", "ART"
            ]
        },
        "WorldBank": {
            "reporting_frequency": "Semi-annually",
            "required_reports": [
                "Implementation Status Report (ISR)",
                "Financial Management Report",
                "Procurement Plan"
            ],
            "eligibility_requirements": [
                "Country government partnership",
                "Technical proposals",
                "Environmental assessment"
            ],
            "budget_restrictions": [
                "Procurement thresholds",
                "Consultant rates",
                "Retroactive financing limits"
            ],
            "compliance_keywords": [
                "PforR", "ESMF", "OP", "BP", "financing", "procurement"
            ]
        }
    }

    if donor_name in donor_guidelines:
        data = donor_guidelines[donor_name]
        if category:
            if category in data:
                return json.dumps({category: data[category]}, indent=2)
            return json.dumps({"error": f"Category '{category}' not found for {donor_name}"})
        return json.dumps(data, indent=2)
    
    return json.dumps({
        "error": f"Donor '{donor_name}' not found",
        "available_donors": list(donor_guidelines.keys())
    })


@tool
def analyze_budget_variance(budget_id: str) -> str:
    """
    Analyze budget variance and provide alerts for over/under spending. READ-ONLY.

    Args:
        budget_id: The budget identifier to analyze

    Returns:
        JSON string with variance analysis and alerts
    """
    budget_info = read_budget_sheet.invoke(budget_id)
    data = json.loads(budget_info)
    
    if "error" in data:
        return budget_info
    
    alerts = []
    warnings = []
    
    for item in data.get("line_items", []):
        variance_pct = (item["variance"] / item["allocated"]) * 100 if item["allocated"] > 0 else 0
        
        if item["variance"] > 0 and variance_pct > 10:
            alerts.append({
                "category": item["category"],
                "type": "significant_overage",
                "amount": item["variance"],
                "percentage": round(variance_pct, 2),
                "message": f"{item['category']} is {variance_pct:.1f}% over budget"
            })
        elif item["variance"] > 0:
            warnings.append({
                "category": item["category"],
                "type": "minor_overage",
                "amount": item["variance"],
                "message": f"{item['category']} is slightly over budget"
            })
        elif item["variance"] < 0 and abs(variance_pct) > 10:
            warnings.append({
                "category": item["category"],
                "type": "significant_underspend",
                "amount": abs(item["variance"]),
                "message": f"{item['category']} is significantly under budget - may indicate implementation delays"
            })
    
    analysis = {
        "budget_id": budget_id,
        "total_budget": data["total_budget"],
        "total_spent": sum(item["spent"] for item in data["line_items"]),
        "total_variance": sum(item["variance"] for item in data["line_items"]),
        "budget_utilization": round(
            sum(item["spent"] for item in data["line_items"]) / data["total_budget"] * 100, 2
        ),
        "alerts": alerts,
        "warnings": warnings,
        "recommendation": "Review over-budget categories for potential reallocation" if alerts else "Budget on track"
    }
    
    return json.dumps(analysis, indent=2)


@tool
def generate_donor_report(budget_id: str, donor_name: str) -> str:
    """
    Generate a donor-specific compliance report. READ-ONLY.

    Args:
        budget_id: The budget identifier
        donor_name: The donor to generate report for

    Returns:
        JSON string with donor-compliant report data
    """
    budget_info = json.loads(read_budget_sheet.invoke(budget_id))
    donor_info = json.loads(check_donor_guidelines.invoke(donor_name))
    
    if "error" in budget_info or "error" in donor_info:
        return json.dumps({
            "error": "Could not generate report",
            "budget_error": budget_info.get("error"),
            "donor_error": donor_info.get("error")
        })
    
    report = {
        "report_type": "Donor Compliance Report",
        "donor": donor_name,
        "budget_period": budget_id,
        "generated_for": donor_info.get("required_reports", []),
        "compliance_items": [
            {
                "requirement": "Financial reporting",
                "status": "compliant",
                "notes": "Financial data available for quarterly reporting"
            },
            {
                "requirement": "Budget restrictions",
                "status": "review_required",
                "notes": "Check individual line items for donor-specific restrictions"
            }
        ],
        "next_steps": [
            f"Prepare {donor_info.get('reporting_frequency')} report",
            "Gather supporting documentation",
            "Submit to donor portal"
        ]
    }
    
    return json.dumps(report, indent=2)


finance_tools = [
    read_budget_sheet,
    check_donor_guidelines,
    analyze_budget_variance,
    generate_donor_report
]

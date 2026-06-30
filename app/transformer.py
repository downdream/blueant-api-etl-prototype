import re
from html import unescape
from app.config import TARGET_PORTFOLIO_ID


KPI_FIELD_IDS = {
    "project_budget_eur": "838167179",
    "planned_costs_eur": "838167339",
    "actual_costs_eur": "838167342",
    "planned_effort_until_today_pt": "832985580",
    "planned_effort_total_pt": "832985583",
    "actual_effort_pt": "838167426",
    "planned_completion_percent": "832985592",
    "actual_completion_percent": "832985595",
}

INDICATOR_FIELD_IDS = {
    "status_total": "832814142",
    "progress_percent": "832814146",
    "status_result": "832814169",
    "status_time": "832814171",
    "status_effort": "832814173",
    "status_explanation": "832814150",
    "classification": "532205505",
    "strategy_contribution": "358638926",
    "confidentiality": "358638949",
}

STATUS_OPTIONS = {
    1: "Rot",
    2: "Gelb",
    3: "Grün",
    "1": "Rot",
    "2": "Gelb",
    "3": "Grün",
}

CLASSIFICATION_OPTIONS = {
    "532205508": "initial project",
    "532205510": "follow-up-project",
}

STRATEGY_CONTRIBUTION_OPTIONS = {
    "358638943": "hoch",
    "358638945": "mittel",
    "358638947": "niedrig",
    "808993519": "sehr niedrig",
}

CONFIDENTIALITY_OPTIONS = {
    "358638952": "Vertraulich",
    "358638954": "Intern",
}

def clean_html_text(value):
    """
    Convert simple HTML content from Blueant API into a readable plain text.
    """

    if value is None:
        return None
    
    text = str(value)
    text = re.sub(r"<[^>]+>", " ", text)
    text = unescape(text)
    text = " ".join(text.split())

    return text

def clean_overall_risk(overall_risk):
    """
    Clean BlueAnt overall risk object for frontend/dashboard usage.
    """

    if not overall_risk:
        return None

    return {
        "overall_risk_id": overall_risk.get("overallRiskId"),
        "risk_assessment": clean_html_text(overall_risk.get("riskAssessment")),
    }

def extract_kpis(custom_fields):
    """
    Extract readable KPI values from BlueAnt custom fields.
    """

    return {
        kpi_name: custom_fields.get(field_id)
        for kpi_name, field_id in KPI_FIELD_IDS.items()
    }


def filter_ki_portfolio_projects(projects):
    """
    Filter projects that belong to the configured KI portfolio.
    """

    return [
        project
        for project in projects
        if TARGET_PORTFOLIO_ID in project.get("portfolioIds", [])
    ]


def clean_project_data(projects):
    """
    Create a simplified project structure for frontend and AI usage.
    """

    clean_projects = []

    for project in projects:
        custom_fields = project.get("customFields", {})

        clean_project = {
            "id": project.get("id"),
            "number": project.get("number"),
            "name": project.get("name"),
            "status_id": project.get("statusId"),
            "portfolio_ids": project.get("portfolioIds", []),
            "start": project.get("start"),
            "end": project.get("end"),
            "planning_type": project.get("planningType"),
            "billing_type": project.get("billingType"),
            "subject": clean_html_text(project.get("subjectMemo")),
            "problem": clean_html_text(project.get("problemMemo")),
            "objective": clean_html_text(project.get("objectiveMemo")),
            "status_text": clean_html_text(project.get("statusMemo")),
            "conclusion": clean_html_text(project.get("conclusionMemo")),
            "overall_risk": clean_overall_risk(project.get("overallRisk")),
            "indicators": extract_indicators(custom_fields),
            "kpis": extract_kpis(custom_fields),
        }

        clean_projects.append(clean_project)

    return clean_projects

def clean_planning_entries(entries):
    """
    Clean BlueAnt planning entries for frontend/dashboard usage.
    """
    
    cleaned_entries = []
    
    for entry in entries:
        cleaned_entry = {
            "id": entry.get("id"),
            "entry_type": entry.get("entryType"),
            "number": entry.get("number"),
            "name": clean_html_text(entry.get("name")),
            "description": clean_html_text(entry.get("description")),
            "start": entry.get("start"),
            "end": entry.get("end"),
            "parent_id": entry.get("parentId"),
            "is_collective_task": entry.get("isCollectiveTask", False),
            "work_planned_days": entry.get("workPlannedDays"),
            "work_actual_days": entry.get("workActualDays"),
            "work_estimated_days": entry.get("workEstimatedDays"),
            "duration_days": entry.get("durationDays"),
            "progress_actual": entry.get("progressActual"),
        }

        cleaned_entries.append(cleaned_entry)

    return cleaned_entries

def split_planning_entries(entries):
    """
    Split planning entries into tasks and milestones.
    """

    return {
        "tasks": [
            entry for entry in entries
            if entry.get("entry_type") == "task"
        ],
        "milestones": [
            entry for entry in entries
            if entry.get("entry_type") == "milestone"
        ],
    }
        
        
def map_option(value, options):
    """
    Translate BlueAnt option keys into readable labels.
    """
    
    if value is None:
        return None
    
    return options.get(value) or options.get(str(value)) or value 

def extract_indicators(custom_fields):
    """
    Extract readable status and metadata indicators from BlueAnt custom fields.
    """
    
    status_total_raw = custom_fields.get(INDICATOR_FIELD_IDS["status_total"])
    status_result_raw = custom_fields.get(INDICATOR_FIELD_IDS["status_result"])
    status_time_raw = custom_fields.get(INDICATOR_FIELD_IDS["status_time"])
    status_effort_raw = custom_fields.get(INDICATOR_FIELD_IDS["status_effort"])

    classification_raw = custom_fields.get(INDICATOR_FIELD_IDS["classification"])
    strategy_contribution_raw = custom_fields.get(INDICATOR_FIELD_IDS["strategy_contribution"])
    confidentiality_raw = custom_fields.get(INDICATOR_FIELD_IDS["confidentiality"])
    
    return {
        "status_total": {
            "raw": status_total_raw,
            "label": map_option(status_total_raw, STATUS_OPTIONS),
        },
        "status_result": {
            "raw": status_result_raw,
            "label": map_option(status_result_raw, STATUS_OPTIONS),
        },
        "status_time": {
            "raw": status_time_raw,
            "label": map_option(status_time_raw, STATUS_OPTIONS),
        },
        "status_effort": {
            "raw": status_effort_raw,
            "label": map_option(status_effort_raw, STATUS_OPTIONS),
        },
        "progress_percent": custom_fields.get(INDICATOR_FIELD_IDS["progress_percent"]),
        "status_explanation": clean_html_text(
            custom_fields.get(INDICATOR_FIELD_IDS["status_explanation"])
        ),
        "classification": {
            "raw": classification_raw,
            "label": map_option(classification_raw, CLASSIFICATION_OPTIONS),
        },
        "strategy_contribution": {
            "raw": strategy_contribution_raw,
            "label": map_option(strategy_contribution_raw, STRATEGY_CONTRIBUTION_OPTIONS),
        },
        "confidentiality": {
            "raw": confidentiality_raw,
            "label": map_option(confidentiality_raw, CONFIDENTIALITY_OPTIONS),
        },
    }
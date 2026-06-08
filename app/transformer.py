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
            "subject": project.get("subjectMemo"),
            "problem": project.get("problemMemo"),
            "objective": project.get("objectiveMemo"),
            "status_text": project.get("statusMemo"),
            "conclusion": project.get("conclusionMemo"),
            "overall_risk": project.get("overallRisk"),
            "custom_fields": custom_fields,
            "kpis": extract_kpis(custom_fields),
        }

        clean_projects.append(clean_project)

    return clean_projects
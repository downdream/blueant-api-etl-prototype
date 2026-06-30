from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.blueant_client import fetch_projects, fetch_portfolio, fetch_project_planning_entries
from app.transformer import filter_ki_portfolio_projects, clean_project_data, clean_planning_entries, split_planning_entries
from app.config import validate_config, TARGET_PORTFOLIO_ID


def get_clean_project_by_id(project_id: int):
    """
    Load AI portfolio projects, clean them, and return one project by ID for dashboard usage
    """
    
    all_projects = fetch_projects()
    ki_projects = filter_ki_portfolio_projects(all_projects)
    clean_project = clean_project_data(ki_projects)
    
    for project in clean_project:
        if project.get("id") == project_id:
            return project
        
    return None

app = FastAPI(
    title="BlueAnt API Backend",
    description="Backend prototype for extracting and preparing BlueAnt project data.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "message": "BlueAnt API Backend is running",
        "available_endpoints": [
            "/api/projects",
            "/api/portfolio",
            "/api/projects/{project_id}/planningentries",
            "/api/projects/{project_id}/dashboard",
        ],
    }


@app.get("/api/projects")
def get_projects():
    try:
        validate_config()
        
        portfolio_response = fetch_portfolio(TARGET_PORTFOLIO_ID)
        portfolio = portfolio_response.get("portfolio", {})

        all_projects = fetch_projects()
        ki_projects = filter_ki_portfolio_projects(all_projects)
        clean_projects = clean_project_data(ki_projects)

        return {
            "portfolio": {
                "id": portfolio.get("id"),
                "number": portfolio.get("number"),
                "name": portfolio.get("name"),
                "date_from": portfolio.get("dateFrom"),
                "date_to": portfolio.get("dateTo"),
                "active": portfolio.get("active"),
                "project_count": len(portfolio.get("projectIds", [])),
            },
            "total_projects": len(all_projects),
            "ki_portfolio_projects": len(ki_projects),
            "projects": clean_projects,
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    
@app.get("/api/portfolio")
def get_portfolio():
    try:
        validate_config()
        portfolio = fetch_portfolio(TARGET_PORTFOLIO_ID)
        return portfolio
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
    

@app.get("/api/projects/{project_id}/planningentries")
def get_project_planning_entries(project_id: int):
    try:
        validate_config()

        planning_response = fetch_project_planning_entries(project_id)
        raw_entries = planning_response.get("entries", [])

        cleaned_entries = clean_planning_entries(raw_entries)
        grouped_entries = split_planning_entries(cleaned_entries)

        return {
            "project_id": project_id,
            "total_entries": len(cleaned_entries),
            "total_tasks": len(grouped_entries["tasks"]),
            "total_milestones": len(grouped_entries["milestones"]),
            "entries": cleaned_entries,
            "tasks": grouped_entries["tasks"],
            "milestones": grouped_entries["milestones"],
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.get("/api/projects/{project_id}/dashboard")
def get_project_dashboard(project_id: int):
    try:
        validate_config()

        project = get_clean_project_by_id(project_id)

        if not project:
            raise HTTPException(
                status_code=404,
                detail="Project not found in AI Portfolio",
            )

        planning_response = fetch_project_planning_entries(project_id)
        raw_entries = planning_response.get("entries", [])

        cleaned_entries = clean_planning_entries(raw_entries)
        grouped_entries = split_planning_entries(cleaned_entries)

        return {
            "project": project,
            "planning": {
                "total_entries": len(cleaned_entries),
                "total_tasks": len(grouped_entries["tasks"]),
                "total_milestones": len(grouped_entries["milestones"]),
                "entries": cleaned_entries,
                "tasks": grouped_entries["tasks"],
                "milestones": grouped_entries["milestones"],
            },
        }

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
from fastapi import FastAPI, HTTPException

from app.config import validate_config
from app.blueant_client import fetch_projects
from app.transformer import filter_ki_portfolio_projects, clean_project_data


app = FastAPI(
    title="BlueAnt API Backend",
    description="Backend prototype for extracting and preparing BlueAnt project data.",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "BlueAnt API Backend is running",
        "available_endpoints": ["/api/projects"],
    }


@app.get("/api/projects")
def get_projects():
    try:
        validate_config()

        all_projects = fetch_projects()
        ki_projects = filter_ki_portfolio_projects(all_projects)
        clean_projects = clean_project_data(ki_projects)

        return {
            "total_projects": len(all_projects),
            "ki_portfolio_projects": len(ki_projects),
            "projects": clean_projects,
        }

    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))
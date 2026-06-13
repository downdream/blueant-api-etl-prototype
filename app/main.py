from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.blueant_client import fetch_projects, fetch_portfolio
from app.transformer import filter_ki_portfolio_projects, clean_project_data
from app.config import validate_config, TARGET_PORTFOLIO_ID


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
        "available_endpoints": ["/api/projects"],
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

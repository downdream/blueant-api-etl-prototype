import os
import json
import requests
from dotenv import load_dotenv


# ------------------------------------------------------------
# 1. Load environment variables
# ------------------------------------------------------------

load_dotenv()

base_url = os.getenv("BLUEANT_BASE_URL")
api_key = os.getenv("BLUEANT_API_KEY")


# ------------------------------------------------------------
# 2. Basic checks
# ------------------------------------------------------------

if not base_url:
    raise ValueError("BLUEANT_BASE_URL is missing in .env")

if not api_key:
    raise ValueError("BLUEANT_API_KEY is missing in .env")


# ------------------------------------------------------------
# 3. Define API endpoint and parameters
# ------------------------------------------------------------

endpoint = "/rest/v1/projects"
url = base_url + endpoint

params = {
    "fromDate": "2025-12-21",
    "toDate": "2026-09-21",
    "includeMemoFields": "true",
    "includeClients": "true",
    "includeOverallRisk": "true",
    "includeExternalSystemInformation": "true",
    "includeCustomFields": "true",
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Accept": "application/json",
}


# ------------------------------------------------------------
# 4. Call BlueAnt API
# ------------------------------------------------------------

response = requests.get(url, headers=headers, params=params, timeout=30)

print("Status code:", response.status_code)

response.raise_for_status()

data = response.json()


# ------------------------------------------------------------
# 5. Extract projects from response
# ------------------------------------------------------------

projects = data.get("projects", [])


# ------------------------------------------------------------
# 6. Filter only KI-Portfolio projects
# ------------------------------------------------------------

target_portfolio_id = 676698496

ki_portfolio_projects = [
    project
    for project in projects
    if target_portfolio_id in project.get("portfolioIds", [])
]


# ------------------------------------------------------------
# 7. Create clean project objects
# ------------------------------------------------------------

clean_projects = []

for project in ki_portfolio_projects:
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
        "custom_fields": project.get("customFields", {}),
    }

    clean_projects.append(clean_project)


# ------------------------------------------------------------
# 8. Print preview
# ------------------------------------------------------------

print("Number of all projects:", len(projects))
print("Number of KI-Portfolio projects:", len(ki_portfolio_projects))
print("Number of clean projects:", len(clean_projects))

print("\nClean project preview:")
for project in clean_projects:
    print(
        f"- {project['number']} | "
        f"{project['name']} | "
        f"status_id={project['status_id']} | "
        f"{project['start']} to {project['end']}"
    )


# ------------------------------------------------------------
# 9. Print custom field IDs for inspection
# ------------------------------------------------------------

print("\nCustom field IDs per KI project:")

for project in clean_projects:
    print(f"\n{project['number']} | {project['name']}")

    custom_fields = project.get("custom_fields", {})

    for field_id, value in custom_fields.items():
        print(f"  {field_id}: {value}")


# ------------------------------------------------------------
# 10. Save raw and clean JSON files
# ------------------------------------------------------------

with open("blueant_projects_raw.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=2)

with open("blueant_projects_clean.json", "w", encoding="utf-8") as file:
    json.dump(clean_projects, file, ensure_ascii=False, indent=2)


print("\nSaved file: blueant_projects_raw.json")
print("Saved file: blueant_projects_clean.json")
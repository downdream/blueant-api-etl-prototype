import requests

from app.config import (
    BLUEANT_BASE_URL,
    BLUEANT_API_KEY,
    BLUEANT_FROM_DATE,
    BLUEANT_TO_DATE,
)


def fetch_projects():
    """
    Fetch project data from the BlueAnt API.

    This function calls the /rest/v1/projects endpoint and returns
    the list of projects from the API response.
    """

    endpoint = "/rest/v1/projects"
    url = BLUEANT_BASE_URL + endpoint

    params = {
        "fromDate": BLUEANT_FROM_DATE,
        "toDate": BLUEANT_TO_DATE,
        "includeMemoFields": "true",
        "includeClients": "true",
        "includeOverallRisk": "true",
        "includeExternalSystemInformation": "true",
        "includeCustomFields": "true",
    }

    headers = {
        "Authorization": f"Bearer {BLUEANT_API_KEY}",
        "Accept": "application/json",
    }

    response = requests.get(url, headers=headers, params=params, timeout=30)

    print("BlueAnt API status code:", response.status_code)

    response.raise_for_status()

    data = response.json()

    return data.get("projects", [])
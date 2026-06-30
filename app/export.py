import json
import requests
from pathlib import Path
from datetime import datetime


API_URL = "http://127.0.0.1:8000/api/projects"
OUTPUT_DIR = Path("exports")


def main():
    OUTPUT_DIR.mkdir(exist_ok=True)

    print("Calling backend API...")
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    data = response.json()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"blueant_api_projects_export_{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    print(f"Export created successfully: {output_file}")


if __name__ == "__main__":
    main()
import json
import requests
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

BLUEANT_BASE_URL = os.getenv("BLUEANT_BASE_URL")
BLUEANT_API_KEY = os.getenv("BLUEANT_API_KEY")

OUTPUT_DIR = Path("exports")

def fetch_project_custom_field_definition():
    """
    Fetch all custom field definition for BlueAnt Project context.
    """
    
    endpoint = "/rest/v1/masterdata/customfield/definitions/Project"
    url = BLUEANT_BASE_URL + endpoint
    
    headers = {
        "Authorization": f"Bearer {BLUEANT_API_KEY}",
        "Accept": "application/json",
    }
    
    response = requests.get(url, headers=headers, timeout=30)
    print("BlueAnt custom field definitions status code:", response.status_code)
    response.raise_for_status()
    
    return response.json()

def create_readable_mapping(data):
    """
    Create a smaller mapping from BlueAnt custom field definitions.
    """
    
    definitions = data.get("customFields", [])
    mapping = {}
    
    for field in definitions:
        field_id = str(field.get("id"))
        
        mapping[field_id] = {
            "id": field.get("id"),
            "name": field.get("name"),
            "type": field.get("type"),
            "report_id": field.get("reportId"),
            "required": field.get("required"),
            "active": field.get("active"),
            "context_type": field.get("contextType"),
            "options": field.get("options", []),
        }
        
    return mapping

def main():
    if not BLUEANT_BASE_URL:
        raise ValueError("BLUEANT_BASE_URL is missing in .env")
    
    if not BLUEANT_API_KEY:
        raise ValueError("BLUEANT_API_KEY is missing in .env")
    
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    data = fetch_project_custom_field_definition()
    mapping = create_readable_mapping(data)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    full_output_file = OUTPUT_DIR / f"blueant_custom_field_definition_project_full_{timestamp}.json"
    mapping_output_file = OUTPUT_DIR / f"blueant_custom_field_mapping_project_{timestamp}.json"
    with open(full_output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

    with open(mapping_output_file, "w", encoding="utf-8") as file:
        json.dump(mapping, file, ensure_ascii=False, indent=2)

    print()
    print(f"Full export created: {full_output_file}")
    print(f"Readable mapping created: {mapping_output_file}")

    print()
    print("Important known fields:")
    important_ids = [
        "832814142",
        "832814146",
        "838167179",
        "838167339",
        "838167342",
        "832985580",
        "832985583",
        "838167426",
        "832985592",
        "832985595",
    ]

    for field_id in important_ids:
        field = mapping.get(field_id)

        if field:
            print(f"{field_id}: {field['name']} ({field['type']})")
        else:
            print(f"{field_id}: not found")


if __name__ == "__main__":
    main()
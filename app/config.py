import os
from dotenv import load_dotenv


load_dotenv()

BLUEANT_BASE_URL = os.getenv("BLUEANT_BASE_URL")
BLUEANT_API_KEY = os.getenv("BLUEANT_API_KEY")

BLUEANT_FROM_DATE = os.getenv("BLUEANT_FROM_DATE", "2025-01-01")
BLUEANT_TO_DATE = os.getenv("BLUEANT_TO_DATE", "2026-12-31")

TARGET_PORTFOLIO_ID = int(os.getenv("TARGET_PORTFOLIO_ID", "676698496"))


def validate_config():
    if not BLUEANT_BASE_URL:
        raise ValueError("BLUEANT_BASE_URL is missing in .env")

    if not BLUEANT_API_KEY:
        raise ValueError("BLUEANT_API_KEY is missing in .env")
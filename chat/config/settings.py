import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL")

API_KEY = os.getenv("OPENAI_KEY")

GOOGLE_SHEETS_CREDENTIALS_FILE = "config/google_sheets_credentials.json"
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
SHEET_NAME = "Página_1"


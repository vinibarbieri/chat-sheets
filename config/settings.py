import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=dotenv_path, override=True)

BACKEND_URL = os.getenv("BACKEND_URL")

OPENAI_API_KEY = os.getenv("OPENAI_KEY")

GOOGLE_SHEETS_CREDENTIALS_FILE = "config/google_sheets_credentials.json"
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID")
SHEET_NAME = os.getenv("SHEET_NAME")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

import gspread
from google.oauth2.service_account import Credentials
from config.settings import GOOGLE_SHEETS_CREDENTIALS_FILE, GOOGLE_SHEETS_ID

credentials = Credentials.from_service_account_file(
    GOOGLE_SHEETS_CREDENTIALS_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(credentials)

print(f"🔍 Acessando planilha {GOOGLE_SHEETS_ID}...")

spreadsheet = client.open_by_key(GOOGLE_SHEETS_ID)
abas = spreadsheet.worksheets()
print("✅ Abas encontradas na planilha:")

for aba in abas:
    print(f"- '{aba.title}'")

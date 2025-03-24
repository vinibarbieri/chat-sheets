import gspread
import pandas as pd
from typing import List, Dict
from google.oauth2.service_account import Credentials
from config.settings import GOOGLE_SHEETS_CREDENTIALS_FILE, SHEET_NAME
from chat.interfaces.spreadsheet_interface import SpreadsheetInterface

class GoogleSheetsManager(SpreadsheetInterface):
    def __init__(self, spreadsheet_id: str):
        self.credentials_file = GOOGLE_SHEETS_CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = SHEET_NAME

    def _authenticate(self):
        credentials = Credentials.from_service_account_file(
            self.credentials_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(credentials)
        return client.open_by_key(self.spreadsheet_id).worksheet(self.sheet_name)

    def load_data(self) -> pd.DataFrame:
        sheet = self._authenticate()
        data = sheet.get_all_values()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])

    def save_data(self, data: List[Dict[str, str]]) -> None:
        print("\n📤 Atualizando Google Sheets...")
        sheet = self._authenticate()
        existing_data = sheet.get_all_values()
        existing_columns = existing_data[0] if existing_data else []

        if not existing_columns:
            print("⚠️ Nenhuma coluna encontrada na planilha. Abortando operação.")
            return

        df = pd.DataFrame(existing_data[1:], columns=existing_columns) if existing_data else pd.DataFrame(columns=existing_columns)
        new_df = pd.DataFrame(data).reindex(columns=existing_columns, fill_value="")
        df = pd.concat([df, new_df], ignore_index=True)

        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("✅ Dados salvos com sucesso!")

import gspread
import pandas as pd
from typing import List, Dict
from google.oauth2.service_account import Credentials
from config.settings import GOOGLE_SHEETS_CREDENTIALS_FILE, SHEET_NAME, GOOGLE_SHEETS_ID
from chat.interfaces.spreadsheet_interface import SpreadsheetInterface

class GoogleSheetsManager(SpreadsheetInterface):
    def __init__(self, spreadsheet_id: str = GOOGLE_SHEETS_ID):
        self.credentials_file = GOOGLE_SHEETS_CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = SHEET_NAME

    def authenticate_google_sheets(self):
        print(f" Acessando planilha {self.spreadsheet_id}...")
        print(f"Acessando a aba {self.sheet_name}...")

        credentials = Credentials.from_service_account_file(
            self.credentials_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(credentials)
        return client.open_by_key(self.spreadsheet_id).worksheet(self.sheet_name)

    def load_data(self) -> pd.DataFrame:
        sheet = self.authenticate_google_sheets()
        data = sheet.get_all_values()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data[1:], columns=data[0])

    def save_data(self, data: List[Dict[str, str]]) -> None:
        print("\n📤 Atualizando Google Sheets...")
        sheet = self.authenticate_google_sheets()
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

    def upsert_lead(self, lead_id: str, new_data: dict):
        sheet = self.authenticate_google_sheets()
        data = sheet.get_all_records()

        # Tenta encontrar o índice da linha com esse ID
        row_index = None
        for i, row in enumerate(data):
            if str(row.get("ID", "")).strip() == lead_id:
                row_index = i + 2  # +2 por causa do cabeçalho e índice 0

        # Se a linha já existir, atualiza os campos
        if row_index:
            print(f"🔄 Atualizando linha existente para ID {lead_id}")
            existing_row = data[row_index - 2]
            updated_row = {**existing_row, **new_data}
            sheet.update(f"A{row_index}:{chr(65 + len(updated_row) - 1)}{row_index}", [list(updated_row.values())])
        else:
            print(f"➕ Criando nova linha para ID {lead_id}")
            headers = sheet.row_values(1)
            new_row = [""] * len(headers)
            for k, v in new_data.items():
                if k in headers:
                    idx = headers.index(k)
                    new_row[idx] = v
            sheet.append_row(new_row)


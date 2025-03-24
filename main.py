from chat import Chat, GoogleSheetsManager
from chat.utils.extract_sheets_id import extract_sheet_id

import sys
import os

# Garante que a raiz do projeto esteja no PYTHONPATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))


def main():
    print("🔗 Digite o link da planilha do Google Sheets:")
    sheet_url = input("> ").strip()
    lead_id = input("🆔 Digite o ID do lead: ").strip()

    sheet_id = extract_sheet_id(sheet_url)
    if not sheet_id:
        print("❌ Erro: ID inválido.")
        return

    sheets = GoogleSheetsManager(sheet_id)
    chat = Chat(sheets, lead_id)
    chat.start()

if __name__ == "__main__":
    main()

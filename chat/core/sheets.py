import gspread
import pandas as pd
import re
from google.oauth2.service_account import Credentials
from config.settings import GOOGLE_SHEETS_CREDENTIALS_FILE, SHEET_NAME

class GoogleSheetsManager:
    def __init__(self, spreadsheet_id):
        self.credentials_file = GOOGLE_SHEETS_CREDENTIALS_FILE
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = SHEET_NAME

    def authenticate_google_sheets(self):
        """Autentica no Google Sheets e retorna a planilha."""
        credentials = Credentials.from_service_account_file(
            self.credentials_file, scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        client = gspread.authorize(credentials)
        return client.open_by_key(self.spreadsheet_id)

    def load_posts(self):
        """Lê os dados do Google Sheets e retorna um DataFrame."""
        sheet = self.authenticate_google_sheets().worksheet(self.sheet_name)
        data = sheet.get_all_values()

        if not data:
            return pd.DataFrame()

        return pd.DataFrame(data[1:], columns=data[0])

    def save_posts(self, posts):
        """Escreve novos dados na planilha, garantindo compatibilidade com as colunas existentes."""
        print("\n📤 Atualizando Google Sheets...")

        sheet = self.authenticate_google_sheets().worksheet(self.sheet_name)
        data = sheet.get_all_values()

        existing_columns = data[0] if data else []

        if not existing_columns:
            print("⚠️ Nenhuma coluna encontrada na planilha. Abortando operação.")
            return

        df = pd.DataFrame(data[1:], columns=existing_columns) if data else pd.DataFrame(columns=existing_columns)

        new_df = pd.DataFrame(posts)
        new_df = new_df.reindex(columns=existing_columns, fill_value="")  

        df = pd.concat([df, new_df], ignore_index=True)

        sheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("✅ Dados salvos no Google Sheets com sucesso!")


def extract_sheet_id(sheet_url):
    """Extrai o ID da planilha a partir do link fornecido pelo usuário."""
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
    return match.group(1) if match else None


def print_dataframe(df):
    """Formata e imprime um DataFrame de forma legível."""
    if df.empty:
        print("⚠️ Nenhum dado encontrado na planilha.")
        return

    for index, row in df.iterrows():
        print(f"🔹 Linha {index + 1}:")
        for column in df.columns:
            print(f"   {column}: {row[column]}")
        print("-" * 40)  


def main():
    """Interface interativa para o usuário."""
    print("🔗 Digite o link da sua planilha do Google Sheets:")
    sheet_url = input("> ").strip()

    sheet_id = extract_sheet_id(sheet_url)
    if not sheet_id:
        print("❌ Erro: ID da planilha não encontrado. Verifique o link e tente novamente.")
        return

    sheets = GoogleSheetsManager(sheet_id)

    while True:
        print("\n📌 O que deseja fazer?")
        print("1️⃣ - Ler a planilha")
        print("2️⃣ - Escrever na planilha")
        print("3️⃣ - Sair")

        escolha = input("> ").strip()

        if escolha == "1":
            print("\n📄 Lendo a planilha...\n")
            df = sheets.load_posts()
            print_dataframe(df)

        elif escolha == "2":
            print("\n✍️ Escrevendo na planilha...")
            df = sheets.load_posts()

            if df.empty:
                print("⚠️ Nenhuma coluna encontrada na planilha. Abortando escrita.")
                continue

            existing_columns = df.columns.tolist()
            new_data = {}

            for col in existing_columns:
                value = input(f"Digite o valor para '{col}': ").strip()
                new_data[col] = value

            sheets.save_posts([new_data])

        elif escolha == "3":
            print("👋 Saindo... Até logo!")
            break

        else:
            print("❌ Opção inválida. Escolha 1, 2 ou 3.")

if __name__ == "__main__":
    main()

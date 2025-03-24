from chat.services.gsheets_manager import GoogleSheetsManager
from chat.utils.sheets import extract_sheet_id, print_dataframe

def main():
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
            df = sheets.load_data()
            print_dataframe(df)

        elif escolha == "2":
            df = sheets.load_data()
            if df.empty:
                print("⚠️ Nenhuma coluna encontrada na planilha.")

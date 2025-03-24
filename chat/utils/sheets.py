import re
import pandas as pd

def extract_sheet_id(sheet_url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", sheet_url)
    return match.group(1) if match else None

def print_dataframe(df: pd.DataFrame):
    if df.empty:
        print("⚠️ Nenhum dado encontrado na planilha.")
        return

    for index, row in df.iterrows():
        print(f"🔹 Linha {index + 1}:")
        for column in df.columns:
            print(f"   {column}: {row[column]}")
        print("-" * 40)

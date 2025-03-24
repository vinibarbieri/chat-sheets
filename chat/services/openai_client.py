from config.settings import OPENAI_API_KEY
from openai import OpenAI
import os

# Cria um cliente da OpenAI com sua chave de API
client = OpenAI(api_key=OPENAI_API_KEY)

def get_openai_response(messages: list) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"[Erro ao chamar a OpenAI: {e}]"

from flask import Flask, request
import os
from chat import Chat, GoogleSheetsManager
from chat.utils.extract_sheets_id import extract_sheet_id
from config.settings import GOOGLE_SHEETS_CREDENTIALS_FILE, SHEET_NAME, GOOGLE_SHEETS_ID, VERIFY_TOKEN, WHATSAPP_TOKEN, PHONE_NUMBER
from dotenv import load_dotenv

from config import settings
print(f"🧪 ID da planilha carregado: {settings.GOOGLE_SHEETS_ID}")


load_dotenv()
app = Flask(__name__)

sessions = {}


@app.route("/webhook", methods=["GET"])
def verify():
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if token == VERIFY_TOKEN:
        return challenge, 200
    return "Invalid token", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()
    
    try:
        value = data["entry"][0]["changes"][0]["value"]

        # Só processa se tiver mensagens novas
        if "messages" in value:
            message = value["messages"][0]
            sender = message["from"]
            text = message["text"]["body"]

            print(f"📩 Mensagem recebida de {sender}: {text}")

            if sender not in sessions:
                sheets = GoogleSheetsManager(GOOGLE_SHEETS_ID)
                sessions[sender] = Chat(sheets, lead_id=sender)

            # Monta e roda o chat (você pode persistir o histórico por sender futuramente)
            chat = sessions[sender]
            reply = chat.handle_message(text)

            # Enviar resposta
            send_reply(sender, reply)
        
        else:
            print("ℹ️ Nenhuma mensagem nova encontrada")

    except Exception as e:
        print(f"❌ Erro ao processar mensagem: {e}")

    return "OK", 200

def send_reply(phone_number, message_text):
    import requests
    import json

    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": phone_number,
        "type": "text",
        "text": {"body": message_text}
    }

    response = requests.post(
        f"https://graph.facebook.com/v19.0/{PHONE_NUMBER}/messages",
        headers=headers,
        data=json.dumps(payload)
    )

    print(f"📤 Resposta enviada ({response.status_code}): {message_text}")
    print("🔍 Resposta da Meta:", response.text)  # Adicione isso para ver o erro exato

if __name__ == "__main__":
    app.run(port=5000)

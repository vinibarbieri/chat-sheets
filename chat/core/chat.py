from chat.interfaces.chat_interface import BaseChatInterface
from chat.core.sheets import GoogleSheetsManager
import openai

class Chat:
    def __init__(self, interface: BaseChatInterface, sheets: GoogleSheetsManager):
        self.interface = interface
        self.sheets = sheets
        self.messages = []

    def process_user_message(self, message: str):
        self.interface.send_user_message(message)
        self.messages.append({"role": "user", "content": message})

        # OpenAI
        openai.api_key = "sua-api-key"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        reply = response["choices"][0]["message"]["content"]
        self.messages.append({"role": "assistant", "content": reply})
        self.interface.receive_bot_message(reply)

        # Exemplo: salvar dados se achar nome/email
        if "meu nome é" in message and "email" in message:
            nome = message.split("meu nome é")[-1].split(",")[0].strip()
            email = message.split("email")[-1].strip()
            self.sheets.save_posts([{"Nome": nome, "Email": email}])

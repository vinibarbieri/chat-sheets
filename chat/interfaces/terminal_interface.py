from chat.interfaces.chat_interface import BaseChatInterface

class TerminalChatInterface(BaseChatInterface):
    def send_user_message(self, message: str) -> None:
        print(f"🧑 Você: {message}")

    def receive_bot_message(self, message: str) -> None:
        print(f"🤖 Bot: {message}")

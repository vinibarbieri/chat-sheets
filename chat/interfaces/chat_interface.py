from abc import ABC, abstractmethod

class BaseChatInterface(ABC):
    @abstractmethod
    def send_user_message(self, message: str) -> None:
        pass

    @abstractmethod
    def receive_bot_message(self, message: str) -> None:
        pass

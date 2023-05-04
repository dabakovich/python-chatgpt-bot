from abc import ABC, abstractmethod
from models.chat import Chat


class Database(ABC):
    @abstractmethod
    def load_chat(self, chat_id: int) -> Chat:
        pass

    @abstractmethod
    def save_chat(self, chat_id: int, chat: Chat) -> None:
        pass

    @abstractmethod
    def clear_chat(self, chat_id: int, message_thread_id: int) -> None:
        pass

from abc import ABC, abstractmethod
from models.user import User


class Database(ABC):
    @abstractmethod
    def load_user(self, chat_id: int) -> User:
        pass

    @abstractmethod
    def save_user(self, chat_id: int, user: User) -> None:
        pass

    @abstractmethod
    def clear_user(self, chat_id: int) -> None:
        pass

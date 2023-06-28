from abc import ABC, abstractmethod

from models.chat import Chat


class Database(ABC):
    @abstractmethod
    def load_chat(self, chat_id: int) -> Chat:
        pass

    @abstractmethod
    def save_chat(self, chat_id: int, chat: Chat) -> None:
        pass

    def clear_messages(self, chat_id: int, message_thread_id: int | None) -> None:
        chat = self.load_chat(chat_id)

        if chat is None:
            return

        if message_thread_id is None:
            chat.messages = None
        else:
            message_thread_id_str = str(message_thread_id)
            if message_thread_id_str in chat.threads:
                chat.threads[message_thread_id_str]["messages"] = None

        self.save_chat(chat_id, chat)

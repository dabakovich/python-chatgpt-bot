import json
from typing import Dict

from telegram import User as TelegramUser, Update

from local_types import GPTMessage, ConversationBase
from models.chat_info import ChatInfo
from utils.gpt_helpers import generate_user_gpt_message, generate_system_gpt_message, get_default_system_message_text
from utils.helpers import get_message_thread_id


class Chat:
    def __init__(self,
                 chat_id: int,
                 info: ChatInfo = None,
                 users: Dict[str, TelegramUser] = None,
                 messages: list[GPTMessage] = None,
                 system_message_text: str = None,
                 threads: Dict[str, ConversationBase] = None):
        self.chat_id = chat_id

        # Chat info
        self.info = info

        # Chat users storing by id
        self.users = users

        # Chat messages
        # Will be "General" chat messages if it's a channel with forum topics
        self.messages = messages

        self.system_message_text = system_message_text

        # Chat threads storing by id
        # Is not None when it's a channel with topics
        self.threads = threads

    def process_telegram_update(self, update: Update):
        user = update.effective_user
        message = update.effective_message
        message_thread_id = get_message_thread_id(update)

        self.chat_id = update.effective_chat.id
        self.info = update.effective_chat
        self.save_user(update.effective_user)

        if message_thread_id is not None:
            thread = self.get_thread(message_thread_id)
            thread_info = message.reply_to_message.forum_topic_created.to_dict()
            thread["info"] = thread_info

        self.ensure_system_message_text_present(message_thread_id)
        self.append_message(generate_user_gpt_message(message.text, user), message_thread_id)

    def process_gpt_response(self, gpt_response: dict, message_thread_id: int = None):
        self.append_message(gpt_response, message_thread_id)

    def append_message(self, message: GPTMessage, message_thread_id: int | None = None):
        messages = self.get_messages(message_thread_id)

        messages.append(message)

    def ensure_system_message_text_present(self, message_thread_id: int | None = None):
        if message_thread_id is not None:
            thread = self.get_thread(message_thread_id)

            if "system_message_text" not in thread or thread["system_message_text"] is None:
                thread["system_message_text"] = get_default_system_message_text(chat_type=self.info.type)

        else:
            if self.system_message_text is None:
                self.system_message_text = get_default_system_message_text(chat_type=self.info.type)

    def get_system_message(self, message_thread_id: int | None = None):
        if message_thread_id is not None:
            thread = self.get_thread(message_thread_id)

            return generate_system_gpt_message(thread["system_message_text"])
        else:
            return generate_system_gpt_message(self.system_message_text)

    def get_messages(self, message_thread_id: int | None = None) -> list[GPTMessage]:
        if message_thread_id is not None:
            thread = self.get_thread(message_thread_id)

            if "messages" not in thread or not thread["messages"]:
                thread["messages"] = []

            return thread["messages"]
        else:
            if self.messages is None:
                self.messages = []

            return self.messages

    def get_thread(self, message_thread_id: int):
        message_thread_id_str = str(message_thread_id)

        threads = self.get_threads()

        if message_thread_id_str not in threads:
            self.threads[message_thread_id_str] = ConversationBase()

        return self.threads[message_thread_id_str]

    def get_threads(self) -> Dict[str, ConversationBase]:
        if self.threads is None:
            self.threads = {}

        return self.threads

    def save_user(self, user: TelegramUser):
        if self.users is None:
            self.users = {}

        self.users[str(user.id)] = user

    def to_dict(self):
        users_dict = None

        if self.users is not None:
            users_dict = {}
            for user_id, user in self.users.items():
                users_dict[user_id] = user.to_dict()

        return {
            "chat_id": self.chat_id,
            "info": self.info.to_dict() if self.info is not None else None,
            "users": users_dict,
            "messages": self.messages,
            "system_message_text": self.system_message_text,
            "threads": self.threads,
        }

    @classmethod
    def from_dict(cls, chat_dict: dict) -> 'Chat':
        chat_id = chat_dict.get('chat_id')
        info = ChatInfo.from_dict(chat_dict.get('info'))

        users_dict = chat_dict.get('users')
        users = None
        if users_dict is not None:
            users = {}
            for user_id, user_data in users_dict.items():
                users[user_id] = TelegramUser(**user_data)

        messages = chat_dict.get('messages')
        system_message_text = chat_dict.get('system_message_text')
        threads = chat_dict.get('threads')
        return cls(chat_id=chat_id,
                   info=info,
                   users=users,
                   messages=messages,
                   system_message_text=system_message_text,
                   threads=threads)

    def to_json(self) -> str:
        chat_dict = self.to_dict()
        return json.dumps(chat_dict, indent=4, ensure_ascii=False)

    @classmethod
    def from_json(cls, chat_id: int, chat_json: str) -> 'Chat':
        if not chat_json:
            return cls(chat_id)

        chat_dict = json.loads(chat_json)
        return cls.from_dict(chat_dict)

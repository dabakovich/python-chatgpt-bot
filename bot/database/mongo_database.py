from pymongo import MongoClient

from config import MONGO_URI, MONGO_DB_NAME
from constants import CHATS_MONGO_COLLECTION_NAME
from database import database
from models.chat import Chat


class MongoDatabase(database.Database):
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.chats_collection = self.db[CHATS_MONGO_COLLECTION_NAME]

    def load_chat(self, chat_id) -> Chat:
        chat_dict = self.chats_collection.find_one({"chat_id": chat_id})
        if chat_dict is None:
            return Chat()

        chat = Chat()
        chat.__dict__.update(chat_dict)
        return chat

    def save_chat(self, chat_id, chat) -> None:
        chat_dict = chat.__dict__
        chat_dict["chat_id"] = chat_id
        self.chats_collection.replace_one({"chat_id": chat_id}, chat_dict, upsert=True)

    def clear_chat(self, chat_id, message_thread_id) -> None:
        if message_thread_id is None:
            self.chats_collection.delete_one({"chat_id": chat_id})
        else:
            chat = self.load_chat(chat_id)
            if chat is not None:
                del chat.threads[message_thread_id]
                self.save_chat(chat_id, chat)

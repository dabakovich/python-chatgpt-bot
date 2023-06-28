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
        chat_mapping = self.chats_collection.find_one({"chat_id": chat_id})
        if chat_mapping is None:
            return Chat()

        chat = Chat.from_dict(dict(chat_mapping))
        return chat

    def save_chat(self, chat_id, chat) -> None:
        chat_dict = chat.to_dict()
        chat_dict["chat_id"] = chat_id
        self.chats_collection.replace_one({"chat_id": chat_id}, chat_dict, upsert=True)

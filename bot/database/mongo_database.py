from pymongo import MongoClient

from config import MONGO_URI, MONGO_DB_NAME
from constants import USERS_MONGO_COLLECTION_NAME
from database import database
from models.user import User


class MongoDatabase(database.Database):
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.users_collection = self.db[USERS_MONGO_COLLECTION_NAME]

    def load_user(self, chat_id: int) -> User:
        user_dict = self.users_collection.find_one({"chat_id": chat_id})
        if user_dict is None:
            return User()

        user = User()
        user.__dict__.update(user_dict)
        return user

    def save_user(self, chat_id: int, user: User) -> None:
        user_dict = user.__dict__
        user_dict["chat_id"] = chat_id
        self.users_collection.replace_one({"chat_id": chat_id}, user_dict, upsert=True)

    def clear_user(self, chat_id: int) -> None:
        self.users_collection.delete_one({"chat_id": chat_id})

from pymongo import MongoClient

from config import MONGO_URI, MONGO_DB_NAME
from models.user import User

USERS_COLLECTION_NAME = 'users'  # replace with your collection name

client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
users_collection = db[USERS_COLLECTION_NAME]


def load_user(chat_id: int):
    user_dict = users_collection.find_one({"chat_id": chat_id})
    if user_dict is None:
        return User()

    user = User()
    user.__dict__.update(user_dict)
    return user


def save_user(chat_id: int, user: User):
    user_dict = user.__dict__
    user_dict['chat_id'] = chat_id
    users_collection.replace_one({"chat_id": chat_id}, user_dict, upsert=True)


def clear_user(chat_id: int):
    users_collection.delete_one({"chat_id": chat_id})

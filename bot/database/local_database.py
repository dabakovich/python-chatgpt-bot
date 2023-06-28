import os

from database import database
from models.chat import Chat


class LocalDatabase(database.Database):
    def __init__(self, database_dir: str = "db"):
        self.database_dir = database_dir

    def load_chat(self, chat_id) -> Chat:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        if not os.path.exists(path):
            return Chat(chat_id)

        with open(path, "r") as f:
            json_str = f.read()

            chat = Chat.from_json(chat_id, json_str)

            return chat

    def save_chat(self, chat_id, chat) -> None:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        with open(path, "w") as f:
            # converting it into JSON
            json_str = chat.to_json()

            # writing to the file
            f.write(json_str)

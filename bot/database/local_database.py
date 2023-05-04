import json
import os

from database import database
from models.chat import Chat


class LocalDatabase(database.Database):
    def __init__(self, database_dir: str = "db"):
        self.database_dir = database_dir

    def load_chat(self, chat_id) -> Chat:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        if not os.path.exists(path):
            return Chat()

        with open(path, "r") as f:
            json_str = f.read()

            # reading json
            data = json.loads(json_str)

            # creating new chat object
            chat = Chat()

            # adding dict data to the created chat object
            chat.__dict__.update(data)
            return chat

    def save_chat(self, chat_id, chat) -> None:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        with open(path, "w") as f:
            # getting dict from the chat object
            data = chat.__dict__

            # converting it into JSON
            json_str = json.dumps(data, indent=4, ensure_ascii=False)

            # writing to the file
            f.write(json_str)

    def clear_chat(self, chat_id, message_thread_id) -> None:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        if os.path.exists(path):
            if message_thread_id is None:
                os.remove(path)
            else:
                message_thread_id_str = str(message_thread_id)
                chat = self.load_chat(chat_id)
                if message_thread_id_str in chat.threads:
                    del chat.threads[message_thread_id_str]
                    self.save_chat(chat_id, chat)

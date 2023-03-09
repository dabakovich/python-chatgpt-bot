import json
import os

from database import database
from models.user import User


class LocalDatabase(database.Database):
    def __init__(self, database_dir: str = "db"):
        self.database_dir = database_dir

    def load_user(self, chat_id: int) -> User:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        if not os.path.exists(path):
            return User()

        with open(path, "r") as f:
            json_str = f.read()

            # reading json
            data = json.loads(json_str)

            # creating new user object
            user = User()

            # adding dict data to the created user object
            user.__dict__.update(data)
            return user

    def save_user(self, chat_id: int, user: User) -> None:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        with open(path, "w") as f:
            # getting dict from the user object
            data = user.__dict__

            # converting it into JSON
            json_str = json.dumps(data, indent=4, ensure_ascii=False)

            # writing to the file
            f.write(json_str)

    def clear_user(self, chat_id: int) -> None:
        path = os.path.join(self.database_dir, f"{chat_id}.json")

        if os.path.exists(path):
            os.remove(path)

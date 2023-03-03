import json
import os

from models.user import User

database_dir = 'db'


def load_user(chat_id: int):
    path = os.path.join(database_dir, f'{chat_id}.json')

    if not os.path.exists(path):
        return User()

    with open(path, 'r') as f:
        json_str = f.read()

        # reading json
        data = json.loads(json_str)

        # creating new user object
        user = User()

        # adding dict data to the created user object
        user.__dict__.update(data)
        return user


def save_user(chat_id: int, user: User):
    path = os.path.join(database_dir, f'{chat_id}.json')

    with open(path, 'w') as f:
        # getting dict from the user object
        data = user.__dict__

        # converting it into JSON
        json_str = json.dumps(data, indent=4, ensure_ascii=False)

        # writing to the file
        f.write(json_str)


def clear_user(chat_id: int):
    path = os.path.join(database_dir, f'{chat_id}.json')

    if os.path.exists(path):
        os.remove(path)

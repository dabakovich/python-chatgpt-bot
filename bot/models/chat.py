class Chat:
    def __init__(self):
        self.chat_id = None
        self.chat_type = None
        self.chat_title = None
        self.user = None
        # ToDo: add logic for saving multiple users in chat group
        # self.users = []
        self.messages = []
        self.threads = {}

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "chat_type": self.chat_type,
            "chat_title": self.chat_title,
            "user": self.user,
            # "users": self.users,
            "messages": self.messages,
            "threads": self.threads,
        }

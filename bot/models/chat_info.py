from telegram import Chat as TelegramChat


class ChatInfo(TelegramChat):
    def __init__(self, **chat_data):
        super().__init__(**chat_data)

    @classmethod
    def from_dict(cls, info_dict: dict | None) -> 'ChatInfo' or None:
        if info_dict is None:
            return None

        return cls(**info_dict)

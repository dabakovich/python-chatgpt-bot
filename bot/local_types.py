from typing import Dict, TypedDict, NotRequired


class GPTMessage(TypedDict):
    role: str
    content: str
    name: NotRequired[str]


class ConversationBase(Dict):
    messages: list[GPTMessage] | None
    info: dict | None
    system_message_text: str | None

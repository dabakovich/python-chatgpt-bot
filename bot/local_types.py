from typing import TypedDict, NotRequired


class GPTMessage(TypedDict):
    role: str
    content: str
    name: NotRequired[str]


class ConversationBase(TypedDict):
    messages: list[GPTMessage] | None
    info: NotRequired[dict]

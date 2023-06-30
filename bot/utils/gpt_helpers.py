import re

from telegram import User
from transliterate import translit, detect_language
from transliterate.exceptions import LanguageDetectionError

from constants import default_initial_context
from local_types import GPTMessage


def generate_system_gpt_message(text=default_initial_context) -> GPTMessage:
    return {
        "role": "system",
        "content": text,
    }


# We need to generate unique name for user's message that matches ^[a-zA-Z0-9_-]{1,64}$ regex
def generate_user_gpt_message(text: str, user: User) -> GPTMessage:
    name = user.first_name
    if user.last_name:
        name += f"-{user.last_name}"

    try:
        detected_language = detect_language(name)
    except LanguageDetectionError:
        detected_language = None

    if detected_language:
        name = translit(name, reversed=True, language_code=detected_language)

    # Remove disallowed symbols
    name = re.sub(r'[^a-zA-Z0-9_-]', '', name)

    # Limit the name length to 64 characters
    name = name[:64]

    name_and_id = name.strip()
    # name_and_id = f"{name.strip()}_{user.id}"

    return {
        "role": "user",
        "content": text,
        "name": name_and_id
    }


def generate_assistant_gpt_message(text: str) -> GPTMessage:
    return {
        "role": "assistant",
        "content": text,
    }

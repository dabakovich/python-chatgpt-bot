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


# We need to generate unique name for user's message in latin characters
def generate_user_gpt_message(text: str, user: User) -> GPTMessage:
    if user.first_name or user.last_name:
        if user.first_name:
            name = user.first_name
            if user.last_name:
                name += f"-{user.last_name}"
        else:
            name = user.last_name

        try:
            detected_language = detect_language(name)
        except LanguageDetectionError:
            detected_language = None

        if detected_language:
            name = translit(name, reversed=True, language_code=detected_language)
    else:
        name = user.username

    name_and_id = name.strip()
    # name_and_id = f"{name.strip()}_{user.id}"

    return {
        "role": "user",
        "content": text,
        "name": name_and_id
    }

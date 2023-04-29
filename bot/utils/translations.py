import json
import os


def load_translation(lang_code, key, default_lang_code="en"):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    upper_directory = os.path.dirname(current_directory)

    path = os.path.join(upper_directory, "i18n", f"{lang_code}.json")

    try:
        with open(path, "r", encoding="utf-8") as f:
            translations = json.load(f)
        return translations.get(key)
    except (FileNotFoundError, KeyError):
        if lang_code != default_lang_code:
            return load_translation(default_lang_code, key)
        else:
            return key  # Return the key itself if the translation is not found in the default language

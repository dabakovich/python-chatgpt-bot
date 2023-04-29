import logging
import openai

from config import OPENAI_API_KEY, GPT_MODEL_NAME, GPT_PREMIUM_MODEL_NAME

openai.api_key = OPENAI_API_KEY


def get_gpt_response(messages, is_premium=False):
    response = openai.ChatCompletion.create(
        model=GPT_PREMIUM_MODEL_NAME if is_premium else GPT_MODEL_NAME,
        messages=messages,
    )

    logging.info(f"gpt tokens usage: {response.usage}")

    return response.choices[0].message

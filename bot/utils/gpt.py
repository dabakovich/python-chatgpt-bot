import time
from typing import Callable, Awaitable

import openai

from config import OPENAI_API_KEY, GPT_MODEL_NAME, GPT_PREMIUM_MODEL_NAME
from constants import MESSAGE_UPDATE_INTERVAL
from utils.gpt_helpers import generate_assistant_gpt_message

openai.api_key = OPENAI_API_KEY


# Get streamed GPT response
async def get_gpt_response(messages, on_new_partial_text: Callable[[str, bool], Awaitable[None]],
                           is_premium=False):
    # Create a new GPT message that will collect streamed response
    gpt_message = generate_assistant_gpt_message("")

    last_message_update_time = None

    async def handle_chunk(next_chunk):
        nonlocal last_message_update_time
        content = extract_content_from_chunk(next_chunk)

        # Collect new partial text from the chunk into the GPT message
        if content:
            gpt_message["content"] += content

        now_time = time.time()

        # We will start tracking time after the first chunk is received
        if last_message_update_time is None:
            last_message_update_time = now_time

        # Update the message every MESSAGE_UPDATE_INTERVAL seconds
        if now_time - last_message_update_time > MESSAGE_UPDATE_INTERVAL:
            last_message_update_time = now_time

            # Call the callback function with the new partial text
            await on_new_partial_text(gpt_message["content"], False)

    response = await openai.ChatCompletion.acreate(
        model=GPT_PREMIUM_MODEL_NAME if is_premium else GPT_MODEL_NAME,
        messages=messages,
        stream=True,
    )

    # Iterate over the streamed response
    async for chunk in response:
        await handle_chunk(chunk)

    # Call the callback function with the last partial text
    await on_new_partial_text(gpt_message["content"], True)

    return gpt_message


# Helper function to extract content from a GPT partial chunk
def extract_content_from_chunk(chunk):
    if 'choices' in chunk and chunk['choices'] and 'delta' in chunk['choices'][0]:
        return chunk['choices'][0]['delta'].get('content', '')
    return ''

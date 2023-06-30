import logging

from openai import InvalidRequestError
from telegram import Update
from telegram.ext import ContextTypes

from config import PREMIUM_USER_IDS
from models.chat import Chat
from utils.gpt import get_gpt_response
from utils.helpers import get_message_thread_id
from utils.translations import load_translation


async def send_updatable_gpt_response(update: Update, context: ContextTypes.DEFAULT_TYPE, chat: Chat):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    language_code = update.effective_user.language_code
    message_thread_id = get_message_thread_id(update)

    try:
        message_id = None

        async def on_new_partial_text(new_text, is_last_part=False):
            nonlocal message_id

            if not new_text:
                return

            text = new_text + " ..." if not is_last_part else new_text

            try:
                if message_id is None:
                    response = await context.bot.send_message(chat_id=chat_id,
                                                              message_thread_id=message_thread_id,
                                                              text=text)
                    message_id = response.message_id
                else:
                    await context.bot.edit_message_text(chat_id=chat_id,
                                                        message_id=message_id,
                                                        text=text)

            except Exception as e:
                logging.error(f"Error editing message text: {e}")

        # Check if the chat is in premium list
        is_premium = user_id in PREMIUM_USER_IDS
        logging.info(f"user_id={user_id}, is_premium={is_premium}")

        messages = chat.get_messages(message_thread_id)
        system_message = chat.get_system_message(message_thread_id)

        messages_with_system_message = [system_message] + messages

        gpt_response = await get_gpt_response(messages_with_system_message, on_new_partial_text, is_premium)
    except InvalidRequestError as e:
        logging.error(e.code)

        if e.code == "context_length_exceeded":
            await context.bot.send_message(chat_id=chat_id,
                                           message_thread_id=message_thread_id,
                                           text=load_translation(language_code, 'context_length_exceeded_error'))
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           message_thread_id=message_thread_id,
                                           text=load_translation(language_code, 'other_error'))

        return

    return gpt_response

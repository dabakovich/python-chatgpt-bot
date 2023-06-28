import logging

from openai import InvalidRequestError
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import PREMIUM_USER_IDS
from database.database_manager import database
from utils.gpt import get_gpt_response
from utils.translations import load_translation


async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"update.effective_chat: {update.effective_chat}")
    logging.info(f"update.effective_user: {update.effective_user}")

    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    message_thread_id = update.effective_message.message_thread_id
    language_code = update.effective_user.language_code

    await context.bot.send_chat_action(chat_id=chat_id, message_thread_id=message_thread_id, action='typing')

    # Load the conversation history from DB
    chat = database.load_chat(chat_id)

    chat.process_telegram_update(update)

    # Save the updated history with user's new message to DB
    database.save_chat(chat_id, chat)

    try:
        # Check if the chat is in premium list
        is_premium = user_id in PREMIUM_USER_IDS
        logging.info(f"user_id={user_id}, is_premium={is_premium}")

        gpt_response = await get_gpt_response(chat.get_messages(message_thread_id), is_premium)
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

    if gpt_response is not None:
        # Load the conversation history from DB
        chat = database.load_chat(chat_id)

        chat.process_gpt_response(gpt_response, message_thread_id)

        # Save the updated history with GPT response to DB
        database.save_chat(chat_id, chat)

    await context.bot.send_message(chat_id=chat_id, message_thread_id=message_thread_id, text=gpt_response.content)


text_message_handler = MessageHandler(
    filters.TEXT & (~ filters.UpdateType.EDITED_MESSAGE),
    on_text_message,
    block=False)

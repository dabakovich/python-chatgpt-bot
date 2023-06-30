import logging

from telegram import Update
from telegram.constants import ChatAction, ChatType
from telegram.ext import ContextTypes, MessageHandler, filters

from database.database_manager import database
from utils.handler_helpers import send_updatable_gpt_response


async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"update.effective_chat: {update.effective_chat}")
    logging.info(f"update.effective_user: {update.effective_user}")
    logging.info(f"message text: {update.effective_message.text}")

    chat_id = update.effective_chat.id
    message_thread_id = update.effective_message.message_thread_id

    # Send typing action only in private chat
    if update.effective_chat.type == ChatType.PRIVATE:
        await context.bot.send_chat_action(chat_id=chat_id, message_thread_id=message_thread_id,
                                           action=ChatAction.TYPING)

    # Load the conversation history from DB
    chat = database.load_chat(chat_id)

    chat.process_telegram_update(update)

    # Save the updated history with user's new message to DB
    database.save_chat(chat_id, chat)

    gpt_response = await send_updatable_gpt_response(update, context, chat)

    if gpt_response is not None:
        # Load the conversation history from DB
        chat = database.load_chat(chat_id)

        chat.process_gpt_response(gpt_response, message_thread_id)

        # Save the updated history with GPT response to DB
        database.save_chat(chat_id, chat)


text_message_handler = MessageHandler(
    filters.TEXT & (~ filters.UpdateType.EDITED_MESSAGE),
    on_text_message,
    block=False)

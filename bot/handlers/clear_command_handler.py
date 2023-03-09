import logging

from telegram import Update
from telegram.ext import CallbackContext

from database.database_manager import database


async def clear_command_handler(update: Update, context: CallbackContext):
    """Handle the /start command."""
    chat_id = update.effective_chat.id

    logging.info(f"chat_id={chat_id}")

    database.clear_user(chat_id)

    await context.bot.send_message(chat_id=chat_id, text="Your conversation was successfully cleared")

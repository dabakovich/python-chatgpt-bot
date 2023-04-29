import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from database.database_manager import database
from enums import Commands
from utils.translations import load_translation


async def clear_command(update: Update, context: CallbackContext):
    """Handle the /start command."""
    chat_id = update.effective_chat.id
    language_code = update.effective_user.language_code

    logging.info(f"clear_command -> chat_id={chat_id}")

    database.clear_user(chat_id)

    await context.bot.send_message(chat_id=chat_id, text=load_translation(language_code, 'clear_message'))


clear_command_handler = CommandHandler(Commands.CLEAR.value, clear_command)

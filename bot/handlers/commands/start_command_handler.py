import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from enums import Commands
from utils.helpers import get_message_thread_id
from utils.translations import load_translation


# ToDo: add check for openai api key existence for a user
async def start_command(update: Update, context: CallbackContext):
    """Handle the /start command."""
    chat_id = update.effective_chat.id
    message_thread_id = get_message_thread_id(update)
    language_code = update.effective_user.language_code

    logging.info(f"start_command -> chat_id={chat_id}")

    await context.bot.send_message(chat_id=chat_id, message_thread_id=message_thread_id,
                                   text=load_translation(language_code, 'welcome_message'))


start_command_handler = CommandHandler(Commands.START.value, start_command)

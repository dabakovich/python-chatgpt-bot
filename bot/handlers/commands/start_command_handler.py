import logging

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from constants import welcome_message
from enums import Commands


# ToDo: add check for openai api key existence for a user
async def start_command(update: Update, context: CallbackContext):
    """Handle the /start command."""
    chat_id = update.effective_chat.id

    logging.info(f"start_command -> chat_id={chat_id}")

    await context.bot.send_message(chat_id=chat_id, text=welcome_message)


start_command_handler = CommandHandler(Commands.START.value, start_command)

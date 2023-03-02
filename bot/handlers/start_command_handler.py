import logging

from telegram import Update
from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# ToDo: add check for openai api key existence for a user
async def start_command_handler(update: Update, context: CallbackContext):
    """Handle the /start command."""
    chat_id = update.effective_chat.id

    logging.info(f"chat_id={chat_id}")

    await context.bot.send_message(chat_id=chat_id, text="Hello, it's your bot")

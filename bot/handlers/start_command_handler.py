import logging

from telegram import Update
from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

welcome_message = "Hello, it's your ChatGPT bot. Ask me anything you want. Type /clear to clear you context an start " \
                  "new conversation."


# ToDo: add check for openai api key existence for a user
async def start_command_handler(update: Update, context: CallbackContext):
    """Handle the /start command."""
    chat_id = update.effective_chat.id

    logging.info(f"chat_id={chat_id}")

    await context.bot.send_message(chat_id=chat_id, text=welcome_message)

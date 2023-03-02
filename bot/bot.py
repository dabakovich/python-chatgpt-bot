import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers.clear_command_handler import clear_command_handler
from handlers.start_command_handler import start_command_handler
from handlers.text_message_handler import text_message_handler

from config import TELEGRAM_BOT_TOKEN

# ToDo: add to shared util
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Set up the start command handler
    application.add_handler(CommandHandler("clear", clear_command_handler))
    application.add_handler(CommandHandler("start", start_command_handler))
    application.add_handler(MessageHandler(filters.TEXT, text_message_handler))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()

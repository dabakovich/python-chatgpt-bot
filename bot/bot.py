import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from handlers.clear_command_handler import clear_command_handler
from handlers.error_handler import error_handler
from handlers.start_command_handler import start_command_handler
from handlers.text_message_handler import text_message_handler

from config import TELEGRAM_BOT_TOKEN, PORT, IS_USE_WEBHOOK_BOT

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Set up the start command handler
    application.add_handler(CommandHandler("clear", clear_command_handler))
    application.add_handler(CommandHandler("start", start_command_handler))
    application.add_handler(MessageHandler(filters.TEXT, text_message_handler))

    application.add_error_handler(error_handler)

    if IS_USE_WEBHOOK_BOT:
        # Start the bot
        application.run_webhook(listen="0.0.0.0",
                                port=PORT,
                                url_path=TELEGRAM_BOT_TOKEN,
                                webhook_url='https://python-chatgpt-bot.herokuapp.com/' + TELEGRAM_BOT_TOKEN)
    else:
        application.run_polling()


if __name__ == '__main__':
    main()

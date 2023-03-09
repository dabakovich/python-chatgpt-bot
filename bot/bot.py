import logging

from telegram.ext import ApplicationBuilder

from config import TELEGRAM_BOT_TOKEN, PORT, IS_USE_WEBHOOK_BOT
from handlers.commands import clear_command_handler, start_command_handler
from handlers.conversations import set_context_conversation_handler
from handlers.error_handler import error_handler
from handlers.messages import text_message_handler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Set up command handlers
    application.add_handler(clear_command_handler)
    application.add_handler(set_context_conversation_handler)
    application.add_handler(start_command_handler)

    # Set up message handler. We're not handling edited message update yet
    application.add_handler(text_message_handler)

    # Set up unhandled error handler
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

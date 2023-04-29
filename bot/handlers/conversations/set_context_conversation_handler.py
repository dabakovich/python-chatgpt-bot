import logging

from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters

from database.database_manager import database
from enums import Commands
from models.user import User
from utils.translations import load_translation

WAITING_FOR_CONTEXT_TEXT = "WAITING_FOR_CONTEXT_TEXT"


async def set_context_command(update: Update, context: CallbackContext):
    """Handle the /set_context command."""
    chat_id = update.effective_chat.id
    language_code = update.effective_user.language_code

    logging.info(f"chat_id={chat_id}")

    await context.bot.send_message(chat_id=chat_id, text=load_translation(language_code, 'send_system_message'))

    return WAITING_FOR_CONTEXT_TEXT


async def context_text(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    text = update.message.text
    language_code = update.effective_user.language_code

    logging.info(f"chat_id={chat_id}")

    user = User(text)

    database.save_user(chat_id, user)

    await context.bot.send_message(chat_id=chat_id, text=load_translation(language_code, 'system_message_applied'))

    return ConversationHandler.END


async def cancel_command(update: Update, _context: CallbackContext) -> int:
    language_code = update.effective_user.language_code

    """Cancels and ends the conversation."""
    await update.message.reply_text(load_translation(language_code, 'system_message_cancel'))

    return ConversationHandler.END


set_context_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler(Commands.SET_CONTEXT.value, set_context_command)],
    states={
        WAITING_FOR_CONTEXT_TEXT: [MessageHandler(filters.TEXT & (~ filters.COMMAND), context_text)],
    },
    fallbacks=[CommandHandler(Commands.CANCEL.value, cancel_command)],
)

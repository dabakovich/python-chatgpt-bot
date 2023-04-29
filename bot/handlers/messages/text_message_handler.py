import logging

from openai import InvalidRequestError
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import PREMIUM_CHAT_IDS
from constants import error_texts
from database.database_manager import database
from utils.gpt import get_gpt_response


async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    logging.info(f"New message from {update.effective_chat.first_name} with '{text}' text")

    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    # Load the conversation history from file
    user = database.load_user(chat_id)

    # Save JSON serialized of update.effective_user into user.user key
    user.user = update.effective_user.to_dict()

    # Save JSON serialized of update.effective_chat into user.chat key
    user.chat = update.effective_chat.to_dict()

    # Add the current message to the history
    user.messages.append({"role": 'user', "content": text})

    # Check if the user is in premium list
    is_premium = chat_id in PREMIUM_CHAT_IDS

    logging.info(f"chat_id={chat_id}, is_premium={is_premium}")

    try:
        chatgpt_response = get_gpt_response(user.messages, is_premium)
    except InvalidRequestError as e:
        logging.error(e.code)

        if e.code == "context_length_exceeded":
            await context.bot.send_message(chat_id=chat_id, text=error_texts.get('context_length_exceeded'))
        else:
            await context.bot.send_message(chat_id=chat_id, text=error_texts.get('other_error'))

        return

    # Add the response to the history
    user.messages.append(chatgpt_response)

    # Save the updated history to file
    database.save_user(chat_id, user)

    await context.bot.send_message(chat_id=chat_id, text=chatgpt_response.content)


text_message_handler = MessageHandler(filters.TEXT & (~ filters.UpdateType.EDITED_MESSAGE), on_text_message)

import logging

from openai import InvalidRequestError
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from constants import error_texts
from database.database_manager import database
from utils.gpt import get_gpt_response


async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # exit if it's edited message update, we're not handling it yet
    # if update.edited_message is not None:
    #     return

    chat_id = update.effective_chat.id
    text = update.message.text

    logging.info(f"New message from {update.effective_chat.first_name} with '{text}' text")

    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    # Load the conversation history from file
    user = database.load_user(chat_id)

    # Add the current message to the history
    user.messages.append({"role": 'user', "content": text})

    try:
        chatgpt_response = get_gpt_response(user.messages)
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

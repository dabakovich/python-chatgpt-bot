import logging

from telegram import Update
from telegram.ext import ContextTypes

from utils.database import load_user, save_user
from utils.gpt import get_gpt_response


async def text_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    logging.info(f"New message from {update.effective_chat.first_name} with '{text}' text")

    await context.bot.send_chat_action(chat_id=chat_id, action='typing')

    # Load the conversation history from file
    user = load_user(chat_id)

    # Add the current message to the history
    user.messages.append({"role": 'user', "content": text})

    chatgpt_response = get_gpt_response(user.messages)

    # Add the response to the history
    user.messages.append(chatgpt_response)

    # Save the updated history to file
    save_user(chat_id, user)

    await context.bot.send_message(chat_id=chat_id, text=chatgpt_response.content)

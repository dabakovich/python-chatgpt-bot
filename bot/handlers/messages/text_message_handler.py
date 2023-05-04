import logging

from openai import InvalidRequestError
from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from config import PREMIUM_CHAT_IDS
from database.database_manager import database
from utils.gpt import get_gpt_response
from utils.translations import load_translation


async def on_text_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.info(f"update.effective_chat: {update.effective_chat}")
    logging.info(f"update.effective_user: {update.effective_user}")
    logging.info(f"update.effective_message: {update.effective_message}")

    chat_id = update.effective_chat.id
    message_thread_id = update.effective_message.message_thread_id
    text = update.effective_message.text
    language_code = update.effective_user.language_code

    logging.info(f"New message from {update.effective_chat.first_name} with '{text}' text")

    await context.bot.send_chat_action(chat_id=chat_id, message_thread_id=message_thread_id, action='typing')

    # Load the conversation history from file
    chat = database.load_chat(chat_id)

    # Save JSON serialized of update.effective_chat into chat.chat key
    chat.chat = update.effective_chat.to_dict()

    # Save JSON serialized of update.effective_user into chat.user key
    chat.user = update.effective_user.to_dict()

    if message_thread_id is not None:
        message_thread_id_str = str(message_thread_id)

        # ToDo: think about replacing type of threads from dict to array
        if message_thread_id_str not in chat.threads:
            chat.threads[message_thread_id_str] = {"messages": []}

        messages = chat.threads[message_thread_id_str]["messages"]

        thread_info = update.effective_message.reply_to_message.forum_topic_created.to_dict()
        chat.threads[message_thread_id_str]["info"] = thread_info
    else:
        messages = chat.messages

    # Add the current message to the history
    messages.append({"role": 'user', "content": text})

    try:
        # Check if the chat is in premium list
        is_premium = chat_id in PREMIUM_CHAT_IDS
        logging.info(f"chat_id={chat_id}, is_premium={is_premium}")

        chatgpt_response = await get_gpt_response(messages, is_premium)
    except InvalidRequestError as e:
        logging.error(e.code)

        if e.code == "context_length_exceeded":
            await context.bot.send_message(chat_id=chat_id,
                                           message_thread_id=message_thread_id,
                                           text=load_translation(language_code, 'context_length_exceeded_error'))
        else:
            await context.bot.send_message(chat_id=chat_id,
                                           message_thread_id=message_thread_id,
                                           text=load_translation(language_code, 'other_error'))

        return

    # Add the response to the history
    messages.append(chatgpt_response)

    # Save the updated history to file
    database.save_chat(chat_id, chat)

    await context.bot.send_message(chat_id=chat_id, message_thread_id=message_thread_id, text=chatgpt_response.content)


text_message_handler = MessageHandler(
    filters.TEXT & (~ filters.UpdateType.EDITED_MESSAGE),
    on_text_message,
    block=False)

import html
import json
import logging
import traceback

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

from config import ERRORS_CHAT_ID
from utils.helpers import get_message_thread_id
from utils.translations import load_translation


async def error_handler(update: object, context: CallbackContext):
    logging.error(update)

    logging.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)

    if isinstance(update, Update):
        chat_id = update.effective_chat.id
        message_thread_id = get_message_thread_id(update)
        language_code = update.effective_user.language_code

        await context.bot.send_message(chat_id=chat_id, message_thread_id=message_thread_id,
                                       text=load_translation(language_code, 'other_error'))

    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f"An exception was raised while handling an update\n"
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}"
        "</pre>\n\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )

    await context.bot.send_message(
        chat_id=ERRORS_CHAT_ID, text=message, parse_mode=ParseMode.HTML
    )

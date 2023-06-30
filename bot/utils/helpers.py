from telegram import Update


# We can message_thread_id not only from topics, but also from replies, so we need to check if the message is from topic
def get_message_thread_id(update: Update):
    message = update.effective_message
    message_thread_id = message.message_thread_id

    if message_thread_id is not None and message.reply_to_message is not None and message.reply_to_message.forum_topic_created is not None:
        return message_thread_id

    return None

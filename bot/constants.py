default_initial_context = "You are a helpful assistant."

welcome_message = "Hello, it's your ChatGPT bot. Ask me anything you want. Type /clear to clear you context an start " \
                  "new conversation."
error_texts = {
    "context_length_exceeded": "Unfortunately, you reached the maximum conversation length, please start new using "
                               "/clear command",
    "other_error": "Unfortunately, an error occurred, please try again"
}

USERS_MONGO_COLLECTION_NAME = 'users'

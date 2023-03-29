from constants import default_initial_context


class User:
    def __init__(self, initial_context=default_initial_context):
        self.messages = [
            {"role": "system", "content": initial_context},
        ]

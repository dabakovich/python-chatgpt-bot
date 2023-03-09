class User:
    def __init__(self, initial_context="You are a helpful assistant."):
        self.messages = [
            {"role": "system", "content": initial_context},
        ]

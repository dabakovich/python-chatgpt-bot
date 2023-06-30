import unittest

from telegram import User as TelegramUser

from utils.gpt_helpers import generate_user_gpt_message


class TestUser(TelegramUser):
    def __init__(self, **kwargs):
        super().__init__(id=1, is_bot=False, **kwargs)


text = "Hello, how are you?"


class TestHelper(unittest.TestCase):
    def test_generate_user_gpt_message_with_first_and_last_name(self):
        user = TestUser(first_name="John", last_name="Doe")
        expected_result = {
            "role": "user",
            "content": text,
            "name": "John-Doe"
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)

    def test_generate_user_gpt_message_with_first_name_only(self):
        user = TestUser(first_name="John", last_name=None)
        expected_result = {
            "role": "user",
            "content": text,
            "name": "John"
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)

    def test_generate_user_gpt_message_with_correct_transliteration(self):
        user = TestUser(first_name="Олександр", last_name="Петренко")
        expected_result = {
            "role": "user",
            "content": text,
            "name": "Oleksandr-Petrenko"
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)

    def test_generate_user_gpt_message_with_disallowed_symbols(self):
        user = TestUser(first_name="John", last_name="Doe&")
        expected_result = {
            "role": "user",
            "content": text,
            "name": "John-Doe"
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)

    def test_generate_user_gpt_message_disallowed_symbols_2(self):
        user = TestUser(first_name="•|Anya|•", last_name=None)
        expected_result = {
            "role": "user",
            "content": text,
            "name": "Anya"
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)

    def test_generate_user_gpt_message_with_correct_transliteration_and_disallowed_symbols(self):
        user = TestUser(first_name="🍭Марта🍭", last_name=None)
        expected_result = {
            "role": "user",
            "content": text,
            "name": "Marta"
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)

    def test_generate_user_gpt_message_with_long_name(self):
        user = TestUser(first_name="a" * 70, last_name=None)
        expected_result = {
            "role": "user",
            "content": text,
            "name": "a" * 64
        }
        self.assertEqual(generate_user_gpt_message(text, user), expected_result)


if __name__ == '__main__':
    unittest.main()

import ast
import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

GPT_MODEL_NAME = os.getenv("GPT_MODEL_NAME")
GPT_PREMIUM_MODEL_NAME = os.getenv("GPT_PREMIUM_MODEL_NAME")

DEVELOPER_CHAT_ID = os.getenv("DEVELOPER_CHAT_ID")
ERRORS_CHAT_ID = os.getenv("ERRORS_CHAT_ID")

PREMIUM_CHAT_IDS = list(map(int, os.getenv("PREMIUM_CHAT_IDS", "").split(",")))

IS_USE_MONGO_DB = ast.literal_eval(os.getenv("IS_USE_MONGO_DB", "True"))
IS_USE_WEBHOOK_BOT = ast.literal_eval(os.getenv("IS_USE_WEBHOOK_BOT", "True"))

PORT = int(os.getenv('PORT', 5000))

import ast
import os

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
DEVELOPER_CHAT_ID = os.getenv("DEVELOPER_CHAT_ID")

IS_USE_MONGO_DB = ast.literal_eval(os.getenv("IS_USE_MONGO", "True"))
IS_USE_WEBHOOK_BOT = ast.literal_eval(os.getenv("IS_USE_WEBHOOK_BOT", "True"))

PORT = int(os.getenv('PORT', 5000))

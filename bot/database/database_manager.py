from config import IS_USE_MONGO_DB
from database.local_database import LocalDatabase
from database.mongo_database import MongoDatabase

if IS_USE_MONGO_DB:
    database = MongoDatabase()
else:
    database = LocalDatabase()

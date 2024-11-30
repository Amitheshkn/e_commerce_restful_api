from pymongo import MongoClient

from e_commerce_app.config import settings


class MongoDBClient:
    """
    Singleton class to manage the MongoDB client and database connection.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = MongoClient(settings.MONGO_URI)
            cls._instance.db = cls._instance.client[settings.DATABASE_NAME]
        return cls._instance

    @property
    def get_db(self):
        return self.db


mongodb_client = MongoDBClient()

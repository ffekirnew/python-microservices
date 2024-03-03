from pymongo import MongoClient
from pymongo.collection import Collection

from src.config import config


class DbClient:
    def __init__(self):
        self.client = MongoClient(config["MONGO"]["CONNECTION_STRING"])
        self.db = self.client[config["MONGO"]["DB_NAME"]]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    def on_close(self):
        self.client.close()

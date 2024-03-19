from gridfs import GridFS
from pymongo import MongoClient
from pymongo.collection import Collection


class DbClient:
    def __init__(self, connection_string: str, db_name: str):
        self.client = MongoClient(connection_string)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str) -> Collection:
        return self.db[collection_name]

    def get_fs(self) -> GridFS:
        return GridFS(self.db)

    def on_close(self) -> None:
        self.client.close()

from typing import Annotated

from fastapi import Depends
from pymongo import MongoClient

from app.config import Settings, get_settings


class OrdersSystemRepository:
    def __init__(self, settings: Annotated[Settings, Depends(get_settings)]):
        uri = f"mongodb+srv://{settings.db_user}:{settings.db_password}@{settings.db_host}/?retryWrites=true&w=majority"
        self.__client = MongoClient(uri)
        self.__db = self.client.get_database(settings.db_name)

    def get_collection(self, collection_name):
        return self.db[collection_name]

    @property
    def db(self):
        return self.__db

    @property
    def client(self):
        return self.__client

    def close(self):
        self.client.close()

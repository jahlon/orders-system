import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')


class OrdersSystemRepository:
    def __init__(self):
        uri = f"mongodb+srv://{user}:{password}@{host}/?retryWrites=true&w=majority"
        self.__client = MongoClient(uri)
        self.__db = self.client.get_database(db_name)
        print("Successfully connected to MongoDB!")

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

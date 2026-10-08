from pymongo import MongoClient 
from dotenv import load_dotenv
import os
load_dotenv(override=True)

def connect() :
    port = int(os.getenv('MONGO_PORT'))
    user = os.getenv('MONGO_ROOT_USER')
    password = os.getenv('MONGO_ROOT_PASSWORD')

    client = MongoClient(f"mongodb://{user}:{password}@127.0.0.1:{port}/?directConnection=true&serverSelectionTimeoutMS=2000")
    return client

client = connect()
db = client.youcode_02_03
movies = db.movies
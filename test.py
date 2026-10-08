# print(data.columns)
from pymongo import MongoClient 
from dotenv import load_dotenv
import os
load_dotenv(override=True)

port = int(os.getenv('MONGO_PORT'))
user = os.getenv('MONGO_ROOT_USER')
password = os.getenv('MONGO_ROOT_PASSWORD')

client = MongoClient(f"mongodb://{user}:{password}@127.0.0.1:{port}/?directConnection=true&serverSelectionTimeoutMS=2000")
db = client.youcode_02_03
movies = db.movies

# loading data
import pandas as pd
mongodb_data = list(movies.find())
data = pd.DataFrame(mongodb_data)

import matplotlib.pyplot as ptl
ptl.figure(figsize=(10 , 6))

# distribution des notes et popularités ;
# print(data['overview'].head())
# print(data['popularity'].head())
ptl.scatter(data['overview'] , data['popularity'])
ptl.xlabel("overview")
ptl.ylabel("popularity")
ptl.show()
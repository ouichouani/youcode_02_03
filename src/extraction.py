
import requests as rq
import json
import os
from dotenv import dotenv_values , load_dotenv
import time

load_dotenv(override=True) 
token = os.getenv("TMDB_API_KEY_TOKEN")

params = {
    "language" : "en-US"
}
headers = {
    'accept': 'application/json' ,
    'Authorization' : f"Bearer {token}"
}

def fetch_movies_id() :
    data = []
    for page in range(1 , 151) : 
        try : 
            raw = rq.get(f'https://api.themoviedb.org/3/discover/movie?page={page}' , params=params , headers=headers ,timeout=10)
            if(raw.status_code == 200) : 
                raw = raw.json()
                data += [item.get("id") for item in raw['results']]
            else : 
                print("status code : " , raw.status_code)
                print("reason : " , raw.reason)
                return
        except Exception as e : 
            print(f"extract error : fetching all data  : {e}")
    return data

def fetch_movie_details() :
    data = []
    ids = fetch_movies_id()
    for movie_id in ids : 
        try : 
            raw = rq.get(f'https://api.themoviedb.org/3/movie/{movie_id}?append_to_response=keywords' , params=params , headers=headers ,timeout=10)
            if(raw.status_code == 200) : 
                raw = raw.json()
                data.append(raw)
                
            elif(raw.status_code == 429): 
                print("Rate limit reached. Waiting...")
                time.sleep(5)

            elif(raw.status_code == 429): 
                print("status code : " , raw.status_code)
                print("reason : " , raw.reason)
                return
        except rq.exceptions.ConnectionError as e : 
            print(f"extract error : fetching movies details : {e}")
            time.sleep(2)

        time.sleep(0.1)
    return data

def save_data() :
    data = fetch_movie_details() 
    if(len(data) <= 0 ) :
        print("somthing is wrong with data , check fetch_data in extraction file")
        return
    
    with open('data/raw/raw.json' , "w") as f :
        json.dump(data , f , indent=4)

save_data()


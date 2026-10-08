import pandas as pd
data = pd.read_json("data/raw/raw.json")

# missing and duplicate values
data = data.drop_duplicates('id')
data["belongs_to_collection"] = data["belongs_to_collection"].apply(lambda x: {"name" : "none"} if pd.isna(x) else x)
data = data.drop(columns=["imdb_id","homepage","poster_path","video","adult","backdrop_path", "softcore" , "status" , "original_title"])

# change datatype
data["release_date"] = pd.to_datetime(data["release_date"] , errors="coerce")
data["genres"] = data['genres'].apply(lambda x : [item.get("name") for item in x ])
data["belongs_to_collection"] = data['belongs_to_collection'].apply(lambda x : x.get("name") )
data["production_companies"] = data['production_companies'].apply(lambda x : [item.get("name") for item in x ])
data["keywords"] = data['keywords'].apply(lambda x : [item.get("name") for item in x.get("keywords") ])
data["production_countries"] = data["production_countries"].apply(lambda x : [item.get("iso_3166_1") for item in x ])
data["spoken_languages"] = data["spoken_languages"].apply(lambda x : [item.get("iso_639_1") for item in x ])

# Detection of inconsistencies
# categorical futures

data["original_language"] = data["original_language"].fillna("unknown")
data['overview'] = data['overview'].fillna("")
data['tagline'] = data['tagline'].fillna("")
data["title"] = data["title"].fillna('none')

# numerical futures

# vote_count
data['vote_count'] = data['vote_count'].fillna(0)
data.loc[data['vote_count'] < 0 , 'vote_count'] = 0

# popularity
data['popularity'] = data['popularity'].fillna(0)
data.loc[data['popularity'] < 0 , 'popularity'] = 0

# revenue
data['revenue'] = data['revenue'].fillna(0)
data.loc[data['revenue'] < 0 , 'revenue'] = 0

# release_date
now = pd.Timestamp.now()
data["release_date"] = data["release_date"].fillna(data["release_date"].median())
data.loc[data["release_date"]  < "1933-07-13" , "release_date" ] = "1933-07-13"
data.loc[data["release_date"]  > now , "release_date" ] = now

# budget
data.loc[ data['budget'] < 0  , "budget"] = 0

# runtime
data = data[data['runtime'] > 0]

# vote_average
data['vote_average'] = data['vote_average'].fillna(0)
data.loc[data["vote_average"] < 0 , "vote_average"] = 0 
data.loc[data["vote_average"] > 10 , "vote_average"] = 10 
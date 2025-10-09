import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# params = {
#     "language": "en-AU",
#     "region": "AU"
# }

# headers = { 
#     "accept": "application/json",
#     "Authorization": f"Bearer {os.environ.get('API_TOKEN')}"
# }

# now_playing_resp = requests.get(
#     url="https://api.themoviedb.org/3/movie/now_playing", 
#     headers=headers, 
#     params=params
#     )

# upcoming_resp = requests.get(
#     url="https://api.themoviedb.org/3/movie/upcoming", 
#     headers=headers, 
#     params=params
#     )

# if now_playing_resp.status_code == 200:
#     now_playing_json = now_playing_resp.json()
# else:
#     raise Exception(
#         f"""
#         Failed to extract now playing movie data from The Movies Database API. 
#         Status Code {now_playing_resp.status_code}. 
#         Response: {now_playing_resp.text}
#         """
#     )

# if upcoming_resp.status_code == 200:
#     upcoming_json = upcoming_resp.json()
# else:
#     raise Exception(
#         f"""
#         Failed to extract upcoming movie data from The Movies Database API. 
#         Status Code {upcoming_resp.status_code}. 
#         Response: {upcoming_resp.text}
#         """
#     )

# now_playing_total_pages = now_playing_json.get("total_pages")
# upcoming_total_pages = upcoming_json.get("total_pages")

# now_playing_data = now_playing_json.get("results")
# upcoming_data = upcoming_json.get("results")

# if now_playing_total_pages > 1:
#     for page_num in range(2, now_playing_total_pages + 1):
#         params.update({"page":page_num})
#         response = requests.get(url="https://api.themoviedb.org/3/movie/now_playing", headers=headers, params=params)
#         if response.status_code == 200:
#             response_data = response.json()
#             now_playing_data.extend(response_data.get("results"))
#         else:
#             raise Exception(
#                 f"""
#                 Failed to extract now playing movie data from The Movies Database API. 
#                 Status Code {now_playing_resp.status_code}. 
#                 Response: {now_playing_resp.text}
#                 """
#             )
# else:
#     pass

# if upcoming_total_pages > 1:
#     for page_num in range(2, upcoming_total_pages + 1):
#         params.update({"page":page_num})
#         response = requests.get(url="https://api.themoviedb.org/3/movie/upcoming", headers=headers, params=params)
#         if response.status_code == 200:
#             response_data = response.json()
#             upcoming_data.extend(response_data.get("results"))
#         else:
#             raise Exception(
#                 f"""
#                 Failed to extract upcoming movie data from The Movies Database API. 
#                 Status Code {upcoming_resp.status_code}. 
#                 Response: {upcoming_resp.text}
#                 """
#             )
# else:
#     pass

# with open("data/now_playing.json", "w") as outfile:
#     json.dump(obj=now_playing_data, fp=outfile, indent=4)

# with open("data/upcoming.json", "w") as outfile:
#     json.dump(obj=upcoming_data, fp=outfile, indent=4)

with open("data/now_playing.json", "r") as infile:
    now_playing_data = json.load(fp=infile)

with open("data/upcoming.json", "r") as infile:
    upcoming_data = json.load(fp=infile)

# convert to df
genres_df = pd.read_csv("data/genres.csv")
language_codes_df = pd.read_csv("data/language_codes.csv")
now_playing_df = pd.DataFrame(data=pd.json_normalize(now_playing_data))
upcoming_df = pd.DataFrame(data=pd.json_normalize(upcoming_data))

# drop columns
now_playing_df = now_playing_df.drop(
    columns=[
        "backdrop_path",
        "original_title",
        "overview",
        "poster_path",
        "video"
    ]
)

upcoming_df = upcoming_df.drop(
    columns=[
        "backdrop_path",
        "original_title",
        "overview",
        "poster_path",
        "video",
        "vote_average",
        "vote_count"
    ]
)

# rename columns
genres_df = genres_df.rename(
    columns={
        "id":"genre_id",
        "name":"genre"
        }
)

now_playing_df = now_playing_df.rename(
    columns={
        "adult":"is_adult",
        "genre_ids":"genre",
        "id": "movie_id",
        "original_language": "language",
        "popularity":"popularity_score",
        "vote_average": "rating_average",
        "vote_count":"rating_count"
    }
)

upcoming_df = upcoming_df.rename(
    columns={
        "adult":"is_adult",
        "genre_ids":"genre",
        "id": "movie_id",
        "original_language": "language",
        "popularity":"popularity_score",
        "vote_average": "rating_average",
        "vote_count":"rating_count"
    }
)

# reorder columns
now_playing_column_order = ['movie_id', 'title', 'release_date', 'genre', 'language', 'is_adult', 'popularity_score', 'rating_count', 'rating_average']
now_playing_df = now_playing_df[now_playing_column_order]

upcoming_column_order = ['movie_id', 'title', 'release_date', 'genre', 'language', 'is_adult', 'popularity_score']
upcoming_df = upcoming_df[upcoming_column_order]

# rearrange date
now_playing_df['release_date'] = pd.to_datetime(now_playing_df['release_date']).dt.strftime("%d-%m-%Y")
upcoming_df['release_date'] = pd.to_datetime(upcoming_df['release_date']).dt.strftime("%d-%m-%Y")

# join with genre
now_playing_df_exploded = now_playing_df.explode("genre")
now_playing_df_exploded["genre"] = pd.to_numeric(now_playing_df_exploded["genre"]).astype(dtype="Int64")

genres_df["genre_id"] = genres_df["genre_id"].astype(dtype="Int64")

now_playing_df_merged = pd.merge(left=now_playing_df_exploded, right=genres_df, left_on="genre", right_on="genre_id", how="left")
now_playing_grouped = now_playing_df_merged.groupby(by="movie_id").agg(
    {
        "title": "first",
        "release_date":"first",
        "genre_y": lambda genre: ", ".join(genre.astype(str)),
        "language":"first",
        "is_adult":"first",
        "popularity_score":"first",
        "rating_count":"first",
        "rating_average":"first"
    }
)

now_playing_grouped = now_playing_grouped.rename(columns={"genre_y":"genre"})

now_playing_merged_2 = pd.merge(left=now_playing_grouped, right=language_codes_df, left_on="language", right_on="iso_639_1", how="left")
now_playing_merged_2 = now_playing_merged_2.drop(columns=["language","iso_639_1", "name"])
now_playing_merged_2 = now_playing_merged_2.rename(columns={"english_name":"language"})

now_playing_merged_2[["popularity_score", "rating_average"]] = now_playing_merged_2[["popularity_score", "rating_average"]].round(2)

now_playing_transformed = now_playing_merged_2


pd.set_option('display.max_columns', None)  
#pd.set_option('display.width', None)      

#print(genres_df.head())
#print(now_playing_df.head())
#print(upcoming_df.head())
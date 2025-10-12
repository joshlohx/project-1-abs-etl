import pandas as pd
from app.etl_movie.connectors.movie_database import MovieDatabaseApiClient
from app.etl_movie.assets.movie_database import extract_genres, extract_language_codes, extract_movie_database, transform
import os 
from dotenv import load_dotenv

load_dotenv()

df = transform(
    df=extract_movie_database(
        movie_database_client=MovieDatabaseApiClient(
            api_token=os.getenv("API_TOKEN")
        )
    ),
    df_genres=extract_genres(filepath="app/etl_movie/data/genres.csv"),
    df_language_codes=extract_language_codes(filepath="app/etl_movie/data/language_codes.csv"),
)

pd.set_option('display.max_columns', None)  
print(df.head(5))
from app.etl_movie.connectors.movie_database import MovieDatabaseApiClient
import os 
from dotenv import load_dotenv

load_dotenv()

movie_database_client = MovieDatabaseApiClient(
    api_token=os.getenv("API_TOKEN")
)

print(movie_database_client.get_now_playing())
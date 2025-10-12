import pandas as pd
from app.etl_movie.connectors.movie_database import MovieDatabaseApiClient

def extract_movie_database(movie_database_client: MovieDatabaseApiClient) -> pd.DataFrame:

    data = movie_database_client.get_now_playing()
    df = pd.DataFrame(data=pd.json_normalize(data))
    return df

def extract_genres(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def extract_language_codes(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    return df

def transform(df: pd.DataFrame, df_genres: pd.DataFrame, df_language_codes: pd.DataFrame) -> pd.DataFrame:
    df_explode = df.explode("genre_ids")
    
    df_explode["genre_ids"] = pd.to_numeric(df_explode["genre_ids"]).astype(dtype="Int64")
    df_genres["id"] = df_genres["id"].astype(dtype="Int64")

    df_merged = pd.merge(left=df_explode, right=df_genres, left_on="genre_ids", right_on="id", how="left")
    df_grouped = df_merged.groupby(by="id_x").agg(
        {
            "id_x": "first",
            "title": "first",
            "release_date":"first",
            "name": lambda genre: ", ".join(genre.astype(str)),
            "original_language":"first",
            "adult":"first",
            "popularity":"first",
            "vote_count":"first",
            "vote_average":"first"
        }
    )

    df_merged_2 = pd.merge(left=df_grouped, right=df_language_codes, left_on="original_language", right_on="iso_639_1", how="left")
    
    df_renamed = df_merged_2.rename(
        columns={
            "id_x":"movie_id",
            "name_x":"genre",
            "adult":"is_adult",
            "popularity":"popularity_score",
            "vote_count":"rating_count",
            "vote_average":"rating_score",
            "english_name":"language"
        }
    )

    df_selected = df_renamed[
        ["movie_id", "title", "release_date", "genre", "language", "is_adult", "popularity_score", "rating_score", "rating_count"]
    ]

    df_selected[["popularity_score", "rating_score"]] = df_selected[["popularity_score", "rating_score"]].round(2)

    df_movie_now_playing = df_selected
    return df_movie_now_playing

def load():
    pass
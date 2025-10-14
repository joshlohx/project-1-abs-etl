from dotenv import load_dotenv
from pathlib import Path
from loguru import logger
import os
import yaml
import schedule
import time
from sqlalchemy import Column, Float, Integer, MetaData, String, Table, Date, create_engine
from app.etl_movie.connectors.movie_database import MovieDatabaseApiClient
from app.etl_movie.connectors.postgresql import PostgreSqlClient
from app.etl_movie.assets.movie_database import (
    extract_movie_database,
    extract_genres,
    extract_language_codes,
    transform,
    load
)

def pipeline():
    logger.info("Pipeline run commencing")

    logger.info("Fetching environment variables")
    api_token = os.getenv("api_token")
    db_database_name = os.getenv("db_database_name")
    db_password = os.getenv("db_password")
    db_server_name = os.getenv("db_server_name")
    db_user = os.getenv("db_user")

    movie_database_client = MovieDatabaseApiClient(
        api_token=api_token
    )

    # extract
    logger.info("Extracting data from movies database API and CSV files")

    df_movie_list = extract_movie_database(movie_database_client=movie_database_client)
    df_genres = extract_genres(filepath=pipeline_config.get("config").get("genres_filepath"))
    df_language_codes = extract_language_codes(filepath=pipeline_config.get("config").get("language_codes_filepath"))

    # transform
    logger.info("Transforming data")

    df_transformed = transform(
        df = df_movie_list,
        df_genres=df_genres,
        df_language_codes=df_language_codes
    )

    # load
    logger.info(f"Loading data to Postgres with load method: {pipeline_config.get('config').get('load_method')}")

    postgresql_client = PostgreSqlClient(
        username=db_user,
        password=db_password,
        host=db_server_name,
        database_name=db_database_name,
    )

    meta = MetaData()

    movie_list_table = Table(
    "movie_list",
    meta,
    Column("movie_id", Integer, primary_key=True),
    Column("title", String),
    Column("release_date", Date),
    Column("genre", String),
    Column("language", String),
    Column("is_adult", String),
    Column("popularity_score", Float),
    Column("rating_score", Float),
    Column("rating_count", Integer),
    )

    load(
        df=df_transformed,
        postgresql_client=postgresql_client,
        table=movie_list_table,
        metadata=meta,
        load_method=pipeline_config.get("config").get("load_method")
    )

    logger.info("Pipeline run completed")

if __name__ == "__main__":

    # get config 
    yaml_file_path = __file__.replace(".py", ".yaml")
    if Path(yaml_file_path).exists:
        with open(yaml_file_path) as yaml_file:
            pipeline_config = yaml.safe_load(yaml_file)
    else:
        raise Exception(
            "A correctly configued .yaml file does not exists. Please create one ensuring the name variable exists."
        )

    load_dotenv()

    schedule.every(pipeline_config.get("schedule").get("run_hours")).seconds.do(pipeline)

    while True:
        schedule.run_pending()
        time.sleep(1)
        
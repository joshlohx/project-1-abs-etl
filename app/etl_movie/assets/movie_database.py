import pandas as pd

def extract_movie_database() -> dict:
    pass

def extract_genres(filepath: str) -> pd.DataFrame:
    dataframe = pd.read_csv(filepath)
    return dataframe

def extract_language_codes(filepath: str) -> pd.DataFrame:
    dataframe = pd.read_csv(filepath)
    return dataframe

def transform() -> pd.DataFrame:
    pass

def load():
    pass
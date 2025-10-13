import pandas as pd
from app.etl_movie.assets.movie_database import transform

#assemble

def test_transform():
    df = pd.DataFrame(data=
        [
            {
                "adult": False,
                "genre_ids": [27, 28],
                "id":1,
                "original_language":"en",
                "title":"test",
                "popularity":1.036,
                "release_date":"2025-10-13",
                "vote_average":1.027,
                "vote_count":1
            }
        ]
    )

    df_genres = pd.DataFrame(data=
        [
            {
                "id": 27,
                "name":"genre1"
            },
            {
                "id": 28,
                "name":"genre2"
            }
        ]
    )

    df_language_codes = pd.DataFrame(data=
        [
            {
                "iso_639_1": "en",
                "english_name":"English",
                "name":None
            }
        ]
    )

    df_expected = pd.DataFrame(data=
        [
            {
                "movie_id":1, 
                "title":"test", 
                "release_date":"2025-10-13", 
                "genre":"genre1, genre2", 
                "language":"English", 
                "is_adult":False, 
                "popularity_score":1.04, 
                "rating_score":1.03, 
                "rating_count":1
            }
        ]
    )

    #act

    df_output = transform(df=df,
                        df_genres=df_genres,
                        df_language_codes=df_language_codes)

    #assert

    pd.testing.assert_frame_equal(left=df_output, right=df_expected, check_exact=True)
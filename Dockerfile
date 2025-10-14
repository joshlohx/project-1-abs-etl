FROM python:3.10

WORKDIR /

COPY / .

RUN pip install -r requirements.txt

CMD ["python", "-m", "app.etl_movie.pipelines.movie_database"]
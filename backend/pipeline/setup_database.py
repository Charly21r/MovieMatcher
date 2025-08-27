import os
import pandas as pd
from sqlalchemy import create_engine

MOVIE_DATA_PATH = "./backend/raw_data/movies.csv"
RATING_DATA_PATH = "./backend/raw_data/ratings.csv"
TAGS_DATA_PATH = "./backend/raw_data/ratings.csv"
DB_PATH = "./backend/moviematch.db"


def run_pipeline():
    """ 
        Runs the pipeline: reads, cleans, validates, and loads the data into the DB.
    """
    print("Starting pipeline...")
    print(f"Reading data from {MOVIE_DATA_PATH}, {RATING_DATA_PATH}, y {TAGS_DATA_PATH}")

    # Read csv files
    try:
        df_movies = pd.read_csv(MOVIE_DATA_PATH)
        df_ratings = pd.read_csv(RATING_DATA_PATH)
        df_tags = pd.read_csv(TAGS_DATA_PATH)
    except Exception as e:
        print(f"Error while reading the csv data: {e}")
        return

    print("Cleaning and Validating data")
    # Ensure ratings are between 0 and 5
    df_ratings = df_ratings[df_ratings["rating"].between(0, 5)]
    # Drop timestamp column
    df_ratings = df_ratings.drop(columns=["timestamp"])

    # Create Sqlite database
    print(f"Creating and connecting to the database at: {DB_PATH}")
    engine = create_engine(f'sqlite:///{DB_PATH}')

    try:
        df_movies.to_sql("movies", engine, if_exists='replace', index=False)
        df_ratings.to_sql("ratings", engine, if_exists='replace', index=False)
    except Exception as e:
        print(f"Error while loading the data to the database: {e}")
        return
    
    print(f"Pipeline finished succesfuly")

run_pipeline()
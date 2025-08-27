import os
import sys
import pandas as pd

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from app.models import Movie, Rating
from app.database import engine, Base, SessionLocal

RAW_DATA_DIR = 'raw_data'
MOVIES_CSV_PATH = os.path.join(project_root, RAW_DATA_DIR, 'movies.csv')
RATING_CSV_PATH = os.path.join(project_root, RAW_DATA_DIR, 'ratings.csv')


def run_pipeline():
    """ 
        Runs the pipeline: reads, cleans, validates, and loads the data into the DB.
    """
    print("Starting pipeline...")
    print("Creating Tables in the Database (if they didn't exist)")
    # Create tables in database (if they didn't exist)
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error while creating the tables: {e}")
        return
    
    # Read csv files
    print(f"Reading data from {MOVIES_CSV_PATH}, {RATING_CSV_PATH}")
    try:
        df_movies = pd.read_csv(MOVIES_CSV_PATH)
        df_ratings = pd.read_csv(RATING_CSV_PATH)
        # df_tags = pd.read_csv(TAGS_DATA_PATH)
    except Exception as e:
        print(f"Error while reading the csv data: {e}")
        return

    print("Cleaning and Validating data")
    # Ensure ratings are between 0 and 5
    df_ratings = df_ratings[df_ratings["rating"].between(0, 5)]
    # Drop timestamp column
    df_ratings = df_ratings.drop(columns=["timestamp"])
    
    session = SessionLocal()
    try:
        # Empty tables for a clean load
        session.execute(Rating.__table__.delete())
        session.execute(Movie.__table__.delete())

        movies_to_load = df_movies.to_dict(orient='records')
        ratings_to_load = df_ratings.to_dict(orient='records')

        # Insert into database
        print(f"Loading {len(movies_to_load)} movies to the database")
        session.bulk_insert_mappings(Movie, movies_to_load)
        
        print(f"Loading {len(ratings_to_load)} ratings to the database")
        session.bulk_insert_mappings(Rating, ratings_to_load)

        session.commit()
    
    except Exception as e:
        print(f"Error while loading the data to the database: {e}")
        session.rollback()
        return
    finally:
        session.close()
   

    print(f"Pipeline finished succesfuly")


if __name__ == "__main__":
    run_pipeline()
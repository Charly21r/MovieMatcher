from sqlalchemy import create_engine

DB_PATH = "./backend/moviematch.db"

print(f"Creating and connecting to the database at: {DB_PATH}")
engine = create_engine(f'sqlite:///{DB_PATH}')
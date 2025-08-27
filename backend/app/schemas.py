from pydantic import BaseModel
from typing import List

class MovieBase(BaseModel):
    title: str
    genres: str

class Movie(MovieBase):
    movieId: int

    class Config:
        from_attributes = True  # Allows pydantic to work with SQLAlchemy models

class RatingBase(BaseModel):
    userId: int
    movieId: int
    rating: float

class Rating(RatingBase):
    ratingId: int

    class Config:
        from_attributes = True

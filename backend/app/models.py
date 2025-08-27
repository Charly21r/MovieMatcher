from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Movie(Base):
    __tablename__ = "movies"
    
    movieId = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genres = Column(String)

    ratings = relationship("Rating", back_populates="movie")

class Rating(Base):
    __tablename__ = "ratings"

    ratingId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    userId = Column(Integer, index=True)
    movieId = Column(Integer, ForeignKey("movies.movieId"))
    rating = Column(Float)

    movie = relationship("Movie", back_populates="ratings")
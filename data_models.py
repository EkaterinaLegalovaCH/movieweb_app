from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime


db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'

    movie_id = Column(Integer, primary_key=True, autoincrement=True)
    movie_title = Column(String, nullable=False)
    movie_rating = Column(Float, nullable=False)
    movie_director = Column(String, nullable=False)
    movie_released = Column(Integer, nullable=False)
    movie_img = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f"Movie(movie_id = {self.movie_id}, title {self.movie_title})."


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)


    def __repr__(self):
        return f"User(user_id = {self.user_id}, user's name is {self.user_name})."


class Review(db.Model):
    __tablename__ = 'reviews'

    review_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.movie_id'), nullable=False)
    review_text = Column(String, nullable=False)
    review_rating = Column(Float, nullable=False)

    def __repr__(self):
        return f"Review(review_id = {self.review_id})."

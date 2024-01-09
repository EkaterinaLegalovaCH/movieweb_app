from flask_sqlalchemy import SQLAlchemy
from .data_manager_interface import DataManagerInterface
from movieweb_app.data_models import db, Movie, User, Review
import os
import requests
import json


API_KEY = "40ec12d2"
URL = "http://www.omdbapi.com/?"


class SQLiteDataManager(DataManagerInterface):
    def init_app(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath("data/moviewebapp.sqlite")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        """with app.app_context():
            db.create_all()"""   # using only for creating tables

    def get_all_users(self):
        users = db.session.query(User.user_id, User.user_name).all()
        users_info = [{'id': user.user_id, 'name': user.user_name} for user in users]

        return users_info

    def add_user(self, name):
        new_user = User(user_name=name)
        db.session.add(new_user)
        db.session.commit()
        users = db.session.query(User.user_id, User.user_name).all()
        users_info = [{'id': user.user_id, 'name': user.user_name} for user in users]

        return users_info

    def delete_user(self, user_id):
        user_to_delete = User.query.get(int(user_id))
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return f"User {user_id} was successfully deleted!"
        return f"User was not found!"

    def get_user_movies(self, user_id):
        user_movies = db.session.query(
            Movie.movie_id,
            Movie.movie_title,
            Movie.movie_rating,
            Movie.movie_director,
            Movie.movie_released,
            Movie.movie_img,
            Movie.user_id
        ).filter(Movie.user_id == user_id).all()
        movies_info = {f"{movie.movie_id}":
            {
                "name": movie.movie_title,
                "director": movie.movie_director,
                "year": movie.movie_released,
                "rating": movie.movie_rating,
                "poster": movie.movie_img
            }
            for movie in user_movies}
        return movies_info

    def add_user_movie(self, user_id, title):
        title = title
        url = f"{URL}apikey={API_KEY}&t={title}"
        response = requests.get(url)
        movie_data = response.json()
        new_movie_title = movie_data["Title"]
        new_rating = movie_data["imdbRating"]
        new_director = movie_data["Director"]
        new_year = movie_data["Year"]
        new_img_url = movie_data["Poster"]
        new_movie = Movie(
            movie_title=new_movie_title,
            movie_rating = new_rating,
            movie_director = new_director,
            movie_released = new_year,
            movie_img = new_img_url,
            user_id = user_id
        )
        db.session.add(new_movie)
        db.session.commit()
        print(f"Movie {new_movie_title} for user {user_id} was successfully added!")
        return

    def update_user_movie(self, user_id, movie_id, title, director, year, rating):
        movie_to_update = Movie.query.filter_by(user_id=user_id, movie_id=movie_id).first()
        if movie_to_update:
            movie_to_update.movie_title = title
            movie_to_update.movie_director = director
            movie_to_update.movie_released = year
            movie_to_update.movie_rating = rating

            db.session.commit()
            return f"Movie {movie_id} for user {user_id} was successfully updated!"
        return f"Movie {movie_id} not found for user {user_id}. Update failed."

    def delete_user_movie(self, user_id, movie_id):
        movie_to_delete = Movie.query.get(int(movie_id))
        if movie_to_delete:
            db.session.delete(movie_to_delete)
            db.session.commit()
            return
        return

    def add_review(self, user_id, movie_id, review_text, review_rating):
        new_review = Review(
            user_id=user_id,
            movie_id=movie_id,
            review_text=review_text,
            review_rating=review_rating
        )
        db.session.add(new_review)
        db.session.commit()
        return

    def get_reviews(self):
        reviews = db.session.query(
            Review.review_id,
            Review.user_id,
            Review.movie_id,
            Review.review_text,
            Review.review_rating
        ).all()
        reviews_info = {
            f"{review.movie_id}": {
                "id": review.review_id,
                "user-id": review.user_id,
                "review": review.review_text,
                "rating": review.review_rating

            } for review in reviews
        }
        return reviews_info

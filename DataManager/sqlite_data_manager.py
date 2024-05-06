from flask_sqlalchemy import SQLAlchemy
from .data_manager_interface import DataManagerInterface
from .data_models import db, Movie, User, Review, user_movie_association
import os
import requests
import json
from sqlalchemy.orm import joinedload

API_KEY = "40ec12d2"
URL = "http://www.omdbapi.com/?"


class SQLiteDataManager(DataManagerInterface):
    def init_app(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath("data/moviewebapp.sqlite")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)
        """
        with app.app_context():
          db.create_all()   # using only for creating tables
        """

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
        user = User.query.get(user_id)

        if user:
            movies_info = {
                f"{movie.movie_id}": {
                    "name": movie.movie_title,
                    "director": movie.movie_director,
                    "year": movie.movie_released,
                    "rating": movie.movie_rating,
                    "poster": movie.movie_img
                }
                for movie in user.movies
            }
            return movies_info
        else:
            return f"No user found with ID {user_id}"

    def add_user_movie(self, user_id, title, director):
        title = title
        director = director
        url = f"{URL}apikey={API_KEY}&t={title}&director={director}"
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code != 200:
            print(f"Error: Failed to retrieve movie data for '{title}' directed by '{director}'")
            return

        # Try to parse the JSON response
        try:
            movie_data = response.json()
        except Exception as e:
            print(f"Error parsing JSON data: {e}")
            return

        # Check if 'Title' and 'Director' keys exist in the response
        if 'Title' not in movie_data or 'Director' not in movie_data:
            print(f"Error: Movie data for '{title}' directed by '{director}' not found in the response")
            return

        # Access movie attributes safely
        new_movie_title = movie_data.get("Title")
        new_director = movie_data.get("Director")

        # Verify that the retrieved movie matches the provided title and director
        if new_movie_title.lower() != title.lower() or new_director.lower() != director.lower():
            print(
                f"Error: Retrieved movie '{new_movie_title}' directed by '{new_director}' does not match the provided title and director")
            return

        # Access other movie attributes
        new_rating = movie_data.get("imdbRating")
        new_year = movie_data.get("Year")
        new_img_url = movie_data.get("Poster")

        user = User.query.get(user_id)
        if not user:
            print(f"Error: User with ID {user_id} not found.")
            return
        # Create the movie object
        new_movie = Movie(
            movie_title=new_movie_title,
            movie_rating=new_rating,
            movie_director=new_director,
            movie_released=new_year,
            movie_img=new_img_url
        )
        # Add the movie to the user's movies
        user.movies.append(new_movie)

        db.session.commit()
        print(f"Movie '{new_movie_title}' directed by '{new_director}' for user {user_id} was successfully added!")

    def update_user_movie(self, user_id, movie_id, title, director, year, rating):
        user = User.query.get(user_id)

        if user:
            # Iterate through user's movies to find the association object
            for movie_association in user.movies:
                if str(movie_association.movie_id) == movie_id:
                    # Get the associated movie using movie_id
                    movie = Movie.query.get(movie_association.movie_id)
                    # Update movie details
                    movie.movie_title = title
                    movie.movie_director = director
                    movie.movie_released = year
                    movie.movie_rating = rating

                    db.session.commit()

                    return f"Movie {movie_id} for user {user_id} was successfully updated!"

            return f"Movie {movie_id} not found for user {user_id}. Update failed."

        return f"User {user_id} not found. Update failed."

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

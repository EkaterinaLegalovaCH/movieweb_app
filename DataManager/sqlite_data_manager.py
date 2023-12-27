from flask_sqlalchemy import SQLAlchemy
from .data_manager_interface import DataManagerInterface
from movieweb_app.data_models import db, Movie, User
import os

db = SQLAlchemy()


class SQLiteDataManager(DataManagerInterface):
    def init_app(self, app):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath("data/moviewebapp.sqlite")
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.init_app(app)

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
        user_to_delete = User.query.get(user_id)
        print(user_to_delete)
        if user_to_delete:
            db.session.delete(user_to_delete)
            db.session.commit()
            return f"User {user_id} was successfully deleted!"
        return f"User was not found!"


    def get_user_movies(self, user_id):
        pass


    def add_user_movie(self, user_id, title):
        pass


    def update_user_movie(self, user_id, movie_id, title, director, year, rating):
        pass

    def delete_user_movie(self, user_id, movie_id):
        pass











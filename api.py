from flask import Blueprint, render_template
from DataManager.sqlite_data_manager import SQLiteDataManager

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/users', methods=['GET'])
def get_users():
    data_manager = SQLiteDataManager()
    users = data_manager.get_all_users()
    return render_template('users.html', users_info=users)


@user_blueprint.route('/users/<string:user_id>', methods=['GET'])
def user_movies(user_id):
    """
    After clicking on user's name(link), implement function,
    getting list of user's movies, and create an HTML page with those movies
    :param user_id:
    :return: HTML page movies.html
    """
    data_manager = SQLiteDataManager()
    movies = data_manager.get_user_movies(user_id=user_id)
    reviews = data_manager.get_reviews()
    return render_template('movies.html', user_movies=movies, reviews=reviews, user_id=user_id)


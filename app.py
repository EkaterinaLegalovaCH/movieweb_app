from flask import Flask, render_template, redirect, url_for, request
from DataManager.json_data_manager import JSONDataManager
from DataManager.sqlite_data_manager import SQLiteDataManager
from data_models import db, Movie, User
from sqlalchemy import or_
import os

app = Flask(__name__, instance_path=os.path.abspath('data'))
"""data_manager = JSONDataManager("data/data.json")
"""

data_manager = SQLiteDataManager()
data_manager.init_app(app)


app.static_folder = 'static'


@app.route('/')
def home():
    """
    endpoint for a home page
    :return: greeting on a home page
    """
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    """
    endpoint for a list of users
    :return: HTML page with a list of users
    """
    users = data_manager.get_all_users()
    return render_template('users.html', users_info=users)


@app.route('/users/add_user', methods=['GET', 'POST'])
def add_user():
    """
    Check if request method is POST, implement function to add user, then redirect
    to HTML page with list of users
    """
    if request.method == 'POST':
        name = request.form.get('name')
        data_manager.add_user(name=name)
    return redirect(url_for('list_users'))


@app.route('/users/add_user_form', methods=["GET", "POST"])
def add_user_form():
    return render_template('add_user.html')


@app.route('/users/delete_user/<string:user_id>', methods=["GET", "POST"])
def delete_user(user_id):
    data_manager.delete_user(user_id=user_id)
    return redirect(url_for('list_users'))


@app.route('/users/<string:user_id>')
def user_movies(user_id):
    """
    After clicking on user's name(link), implement function,
    getting list of user's movies, and create an HTML page with those movies
    :param user_id:
    :return: HTML page movies.html
    """
    movies = data_manager.get_user_movies(user_id=user_id)
    return render_template('movies.html', user_movies=movies, user_id=user_id)


@app.route('/users/<string:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    """
    Check if request method is POST, implement function to add movie ,
    then create HTML page with list of movies
    """
    if request.method == "POST":
        name = request.form.get('name')
        try:                      # if title of movie doesn't exist in data OMDb API, raise exception
            data_manager.add_user_movie(user_id=user_id, title=name)
        except KeyError as e:
            print("A KeyError occurred", str(e))
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<string:user_id>/add_movie_form', methods=["GET", "POST"])
def add_movie_form(user_id):
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<string:user_id>/update_movie/<string:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    if request.method == "POST":
        print(f"user_id: {user_id}, movie_id: {movie_id}")
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        data_manager.update_user_movie(
            user_id=user_id,
            movie_id=movie_id,
            title=name,
            director=director,
            year=year,
            rating=rating
        )

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<string:user_id>/update_movie_form/<string:movie_id>', methods=["GET", "POST"])
def update_movie_form(user_id, movie_id):
    movies_details = data_manager.get_user_movies(user_id=user_id)
    movie_details = movies_details[movie_id]
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie_details=movie_details)


@app.route('/users/<string:user_id>/delete_movie/<string:movie_id>', methods=["GET", "POST"])
def delete_movie(user_id, movie_id):
    data_manager.delete_user_movie(user_id=user_id, movie_id=movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404




"""
with app.app_context():
    db.create_all()
"""

if __name__ == '__main__':
    app.run(debug=True)

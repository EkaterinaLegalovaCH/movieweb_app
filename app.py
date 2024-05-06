from flask import Flask, flash, render_template, redirect, url_for, request
from DataManager.json_data_manager import JSONDataManager
from DataManager.sqlite_data_manager import SQLiteDataManager
import os
import secrets
from api import create_api_endpoints

print("Current working directory:", os.getcwd())

app = Flask(__name__, instance_path=os.path.abspath('data'))
app.config['SECRET_KEY'] = secrets.token_hex(16)

"""
data_manager = JSONDataManager("data/data.json")
"""

data_manager = SQLiteDataManager()
data_manager.init_app(app)

app.static_folder = 'static'

create_api_endpoints(app, data_manager)


@app.route('/')
def home():
    """
    endpoint for a home page
    :return: home.html page
    """
    print("Wellcome to the Home Page!")
    return render_template('home.html')


@app.route('/users')
def list_users():
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
    """
    route for deleting user
    """
    data_manager.delete_user(user_id=user_id)
    return redirect(url_for('list_users'))


@app.route('/users/<string:user_id>', methods=["GET", "POST"])
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id=user_id)
    reviews = data_manager.get_reviews()
    return render_template('movies.html', user_movies=movies, reviews=reviews, user_id=user_id)


@app.route('/users/<string:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    """
    Check if request method is POST, implement function to add movie ,
    then create HTML page with list of movies
    """
    if request.method == "POST":
        name = request.form.get('name')
        director = request.form.get('director')
        try:  # if title of movie doesn't exist in data OMDb API, raise exception
            data_manager.add_user_movie(user_id=user_id, title=name, director=director)
        except KeyError as e:
            print("A KeyError occurred", str(e))
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<string:user_id>/add_movie_form', methods=["GET", "POST"])
def add_movie_form(user_id):
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<string:user_id>/update_movie/<string:movie_id>', methods=["GET", "POST"])
def update_movie(user_id, movie_id):
    """
    Get parameters about movie from update_movie.html form,
    then update information in the database using function update_user_movie in
    sqlite_data_manager.py
    """
    print("Received POST request to update movie details")
    print(user_id, type(user_id))
    if request.method == "POST":
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

        # Redirect to the page displaying user's movies after updating
        try:
            flash('Movie updated successfully!', 'success')
            return redirect(url_for('user_movies', user_id=user_id))
        except Exception as e:
            print(f"Error updating movie: {e}")
            flash('Error updating movie.', 'danger')
            return redirect(url_for('user_movies', user_id=user_id))
    else:
        # Render the form to update the movie
        movies_details = data_manager.get_user_movies(user_id=user_id)
        movie_details = movies_details[movie_id]
        return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie_details=movie_details)


@app.route('/users/<string:user_id>/update_movie_form/<string:movie_id>', methods=["GET", "POST"])
def update_movie_form(user_id, movie_id):
    movies_details = data_manager.get_user_movies(user_id=user_id)
    movie_details = movies_details[movie_id]
    return render_template('update_movie.html', user_id=user_id, movie_id=movie_id, movie_details=movie_details)


@app.route('/users/<string:user_id>/delete_movie/<string:movie_id>', methods=["GET", "POST"])
def delete_movie(user_id, movie_id):
    data_manager.delete_user_movie(user_id=user_id, movie_id=movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<string:user_id>/add_review/<string:movie_id>', methods=["GET", "POST"])
def add_review(user_id, movie_id):
    """
    for chosen movie of choosen user get review text and rating from reviews.html form,
    then add them in table reviews using function add_review in sqlite_data_manager.py
    """
    if request.method == "POST":
        user_id = int(user_id)
        movie_id = int(movie_id)
        review_text = request.form.get('review_text')
        review_rating = request.form.get('review_rating')
        data_manager.add_review(
            user_id=user_id,
            movie_id=movie_id,
            review_text=review_text,
            review_rating=review_rating
        )

        return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<string:user_id>/add_review_form/<string:movie_id>', methods=["GET", "POST"])
def add_review_form(user_id, movie_id):
    return render_template('reviews.html', user_id=user_id, movie_id=movie_id)


@app.route('/test_redirect')
def test_redirect():
    print('trying to redirect')
    return redirect(url_for('home'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

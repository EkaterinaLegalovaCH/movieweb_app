from flask import Flask, render_template, redirect, url_for, request
from DataManager.json_data_manager import JSONDataManager


app = Flask(__name__)
data_manager = JSONDataManager("data/data.json")
@app.route('/')
def home():
    return "Welcome to MovieWeb App!"


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    print(users)
    return render_template('users.html', users_info=users)


@app.route('/users/<string:user_id>')
def user_movies(user_id):
    movies = data_manager.get_user_movies(user_id=user_id)
    return render_template('movies.html', user_movies=movies, user_id=user_id)


@app.route('/users/<string:user_id>/add_movie', methods=["GET", "POST"])
def add_movie(user_id):
    if request.method == "POST":  # Check if the request method is POST
        name = request.form.get('name')
        data_manager.add_user_movie(user_id=user_id, title=name)

    return redirect(url_for('user_movies', user_id=user_id))


@app.route('/users/<string:user_id>/add_movie_form', methods=["GET", "POST"])
def add_movie_form(user_id):
    return render_template('add_movie.html', user_id=user_id)


@app.route('/users/<user_id>/update_movie/<movie_id>')
def update_movie(user_id, movie_id):
    pass


@app.route('/users/<user_id>/delete_movie/<movie_id>')
def delete_movie(user_id, movie_id):
    pass



if __name__ == '__main__':
    app.run(debug=True)
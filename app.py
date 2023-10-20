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


@app.route('/users/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form.get('name')
        data_manager.add_user(name=name)
    return redirect(url_for('list_users'))


@app.route('/users/add_user_form', methods=["GET", "POST"])
def add_user_form():
    return render_template('add_user.html')


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


@app.route('/users/<string:user_id>/delete_movie/<string:movie_id>')
def delete_movie(user_id, movie_id):
    data_manager.delete_user_movie(user_id=user_id, movie_id=movie_id)
    return redirect(url_for('user_movies', user_id=user_id))


if __name__ == '__main__':
    app.run(debug=True)

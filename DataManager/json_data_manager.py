import json
import requests
from .data_manager_interface import DataManagerInterface


API_KEY = "40ec12d2"
URL = "http://www.omdbapi.com/?"
DATA_FILE = "data/data.json"


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        users_info = []
        for key, value in users_dict.items():
            user_info = {}
            user_info['id'] = str(key)
            user_info['name'] = value['name']
            users_info.append(user_info)

        return users_info


    def add_user(self, name):
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        new_name = name
        new_user_id = max([int(item) for item in list(users_dict.keys())]) + 1
        new_user_movies = {}
        users_dict[new_user_id] = {'name': new_name, 'movies': new_user_movies}
        new_data = json.dumps(users_dict)
        with open(self.filename, "w") as handle:
            handle.write(new_data)
            print(f"User {name} was successfully added!")
            return

    def delete_user(self, user_id):
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        if str(user_id) in users_dict.keys():
            del users_dict[user_id]
            new_data = json.dumps(users_dict)
            with open(self.filename, "w") as handle:
                handle.write(new_data)
                print(f"user{user_id} was successfully deleted!")
                return

    def get_user_movies(self, user_id):
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        user_movies = users_dict[user_id]['movies']
        return user_movies

    def add_user_movie(self, user_id, title):
        title = title
        url = f"{URL}apikey={API_KEY}&t={title}"
        response = requests.get(url)
        movie_data = response.json()
        movie_title = movie_data["Title"]
        rating = movie_data["imdbRating"]
        director = movie_data["Director"]
        year = movie_data["Year"]
        img_url = movie_data["Poster"]
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        user_movies = users_dict[user_id]['movies']
        if not user_movies:
            new_id = 1
        else:
            new_id = max([int(item) for item in list(user_movies.keys())]) + 1
        new_title = movie_title
        new_director = director
        new_year = year
        new_rating = rating
        new_poster = img_url
        new_movie = {
            'name': new_title,
            'director': new_director,
            'year': new_year,
            'rating': new_rating,
            "poster": new_poster
        }
        user_movies[new_id] = new_movie
        users_dict[user_id]['movies'] = user_movies
        new_data = json.dumps(users_dict)
        with open(self.filename, "w") as handle:
            handle.write(new_data)
            print(f"New movie was successfully added!")
            return

    def update_user_movie(self, user_id, movie_id, title, director, year, rating):
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        user_movies = users_dict[user_id]['movies']
        new_title = title
        new_director = director
        new_year = year
        new_rating = rating
        user_movies[movie_id] = {
            'name': new_title,
            'director': new_director,
            'year': new_year,
            'rating': new_rating,
            'poster': user_movies[movie_id]['poster']
        }
        users_dict[user_id]['movies'] = user_movies
        new_data = json.dumps(users_dict)
        with open(self.filename, "w") as handle:
            handle.write(new_data)
            print(f"information of movie id {movie_id} was successfully updated!")
            return

    def delete_user_movie(self, user_id, movie_id):
        with open(self.filename, "r") as handle:
            users_data = handle.read()
            users_dict = json.loads(users_data)
        if str(movie_id) in users_dict[user_id]['movies'].keys():
            del users_dict[user_id]['movies'][movie_id]
            new_data = json.dumps(users_dict)
            with open(self.filename, "w") as handle:
                handle.write(new_data)
                print(f"movie{movie_id} of user {user_id} was successfully deleted!")
                return

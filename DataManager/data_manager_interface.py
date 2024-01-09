from abc import ABC, abstractmethod


class DataManagerInterface(ABC):
    @abstractmethod
    def init_app(self, app):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def add_user(self, name):
        pass

    @abstractmethod
    def delete_user(self, user_id):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def update_user_movie(self, user_id, movie_id, title, director, year, rating):
        pass

    @abstractmethod
    def add_user_movie(self, user_id, title):
        pass

    @abstractmethod
    def delete_user_movie(self, user_id, movie_id):
        pass



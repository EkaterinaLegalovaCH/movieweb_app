import pytest
from app import app

client = app.test_client()

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert b"Welcome to MovieWeb App!" in response.data


def test_list_users():
    response = client.get('/users')
    assert response.status_code == 200


def test_add_user():
    response = client.post('/users/add_user', data={'name': 'Test User'})
    assert response.status_code == 302


def test_add_user_form():
    response = client.get('/users/add_user_form')
    assert response.status_code == 200
    assert b"<title>Add User Form</title>" in response.data


def test_user_movies():
    response = client.get('/users/1')
    assert response.status_code == 200
    assert b"<title>My Movie App</title>" in response.data


def test_add_movie():
    response = client.post('/users/1/add_movie', data={'name': 'Test Movie'})
    assert response.status_code == 302


def test_add_movie_form():
    response = client.get('/users/1/add_movie_form')
    assert response.status_code == 200
    assert b"<title>Add Movie Form</title>" in response.data

def test_update_movie():
    response = client.post('/users/1/update_movie/1', data={"name": "Test Movie", "director": "Director", "year": "Year", "rating": "10", "poster": "Some"})
    assert response.status_code == 302


def test_update_movie_form():
    response = client.get('/users/1/update_movie_form/1')
    assert response.status_code == 200
    assert b"<title>Update Movie Form</title>" in response.data




pytest.main()

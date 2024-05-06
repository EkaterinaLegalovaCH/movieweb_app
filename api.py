from flask import jsonify, request

def create_api_endpoints(app, data_manager):
    @app.route('/api/users', methods=['GET'])
    def api_list_users():
        users = data_manager.get_all_users()
        return jsonify(users)

    @app.route('/api/users/<int:user_id>/movies', methods=['GET'])
    def api_list_user_movies(user_id):
        movies = data_manager.get_user_movies(user_id=user_id)
        return jsonify(movies)

    @app.route('/api/users/<int:user_id>/movies', methods=['POST'])
    def api_add_user_movie(user_id):
        data = request.get_json()
        print(data)
        name = data.get('title')
        director = data.get('director')
        try:
            data_manager.add_user_movie(user_id=user_id, title=name, director=director)
            return jsonify({"message": "Movie added successfully."}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 400

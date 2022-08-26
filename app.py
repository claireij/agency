import os
from flask import Flask, abort, jsonify, request
from models import setup_db, Actor, Movie
from flask_cors import CORS

from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        actors = Actor.query.all()
        
        if len(actors) == 0:
            abort(404)

        formatted_actors = [actor.format() for actor in actors]
        
        return jsonify({
            'success': True,
            'actors': formatted_actors
        })

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        movies = Movie.query.all()
        formatted_movies = [movie.format() for movie in movies]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': formatted_movies
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if actor is None:
            abort(404)
        
        actor_id = actor.format()['id']
        actor.delete()

        return jsonify({
            'success': True,
            'deleted': actor_id
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()

        if movie is None:
            abort(404)

        movie_id = movie.format()['id']
        movie.delete()

        return jsonify({
            'success': True,
            'deleted': movie_id
        })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_new_actor(jwt):
        data = request.get_json()

        if 'name' not in data or 'gender' not in data or 'age' not in data:
            abort(422)

        actor = Actor(name=data['name'], gender=data['gender'], age=data['age'])
        actor.insert()
        formatted_actor = actor.format()

        return jsonify({
            'success': True,
            'actor': formatted_actor
        })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_new_movie(jwt):
        data = request.get_json()

        if 'title' not in data or 'release_date' not in data:
            abort(422)

        movie = Movie(title=data['title'], release_date=data['release_date'])
        movie.insert()
        formatted_movie = movie.format()

        return jsonify({
            'success': True,
            'movie': formatted_movie
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, actor_id):
        data = request.get_json()
    
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
        
        if 'name' and 'age' and 'gender' not in data:
            abort(422)

        if 'name' in data:
            actor.name = data['name']

        if 'age' in data:
            actor.age = data['age']

        if 'gender' in data:
            actor.gender = data['gender']

        actor.update()
        formatted_actor = actor.format()
        
        return jsonify({
            'success': True,
            'actor': formatted_actor
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, movie_id):
        data = request.get_json()

        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if 'title' and 'release_date' not in data:
            abort(422)

        if 'title' in data:
            movie.title = data['title']

        if 'release_date' in data:
            movie.release_date = data['release_date']

        movie.update()
        formatted_movie = movie.format()

        return jsonify({
            'success': True,
            'movie': formatted_movie
        })

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422
    
    @app.errorhandler(404)
    def not_found(error):
        jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(AuthError)
    def process_AuthError(error):
        response = jsonify(error.error)
        response.status_code = error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run()

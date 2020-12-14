import os
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth
import json


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # General GET end point
    @app.route('/', methods=['GET'])
    def print_hello():
        return "hello"

    # GET movies end point
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()  #get list of movies
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies]
        }), 200

    # GET actors end point
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()  #get list of actors
        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    # POST movies end point
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        try:
            data = request.get_json()
            title = data['title']
            release_date = data['release_date']
            new_movie = Movie(title=title, release_date=release_date)
            new_movie.insert()
        except Exception as e:
            # print(e)
            abort(400)
        return jsonify({'success': True, 'movies': [new_movie.format()]}), 200

    # POST actors end point
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):

        try:
            data = request.get_json()
            name = data['name']
            age = data['age']
            gender = data['gender']
            new_actor = Actor(name=name, age=age, gender=gender)
            new_actor.insert()
        except Exception as e:
            # print(e)
            abort(400)
        return jsonify({'success': True, 'actors': [new_actor.format()]}), 200

    # DELETE movies end point
    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        # def delete_movie(id):
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        try:
            movie.delete()
        except:
            abort(400)
        return jsonify({'success': True, 'delete': id}), 200

    # DELETE actors end point
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        # def delete_actor(id):
        # behavior of abort inside try is different
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        try:
            actor.delete()
        except Exception as e:
            # print(e)
            print('error2')
            abort(400)
        return jsonify({'success': True, 'delete': id}), 200

    # PATCH movies end point
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        # def update_movie(id):
        movie = Movie.query.get(id)
        if not movie:
            abort(404)
        try:
            data = request.get_json()
            title = data.get('title')
            release_date = data.get('release_date')
            if title:
                movie.title = data['title']
            else:
                abort(400)
            if release_date:
                movie.releae_date = data['release_date']
            else:
                abort(400)
            movie.update()
        except:
            abort(400)
        return jsonify({'success': True, 'movies': [movie.format()]}), 200

    # PATCH actors end point
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        # def update_actor(id):
        actor = Actor.query.get(id)
        if not actor:
            abort(404)
        try:
            data = request.get_json()
            name = data.get('name')
            gender = data.get('gender')
            age = data.get('age')
            if name:
                actor.name = data['name']
            else:
                abort(400)
            if age:
                actor.age = data['age']
            else:
                abort(400)
            if gender:
                actor.gender = data['gender']
            else:
                abort(400)
            actor.update()
        except:
            abort(400)
        return jsonify({'success': True, 'actors': [actor.format()]}), 200

    ## Error Handling
    '''
    error handling for unprocessable entity
    '''

    # 422 - could not be processed
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    error handler for 404
    '''

    # 404 - resource not found
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # 400 - bad request
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    # 405 - method not allowed
    @app.errorhandler(405)
    def not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    '''
    error handler for AuthError 
    '''

    # 401 - Authentication/Authorization error
    @app.errorhandler(AuthError)
    def auth_error(e):
        return jsonify(e.error), e.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
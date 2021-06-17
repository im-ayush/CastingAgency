#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import os
import json
import dateutil.parser
import babel
from flask import (
            Flask,
            render_template,
            request,
            Response,
            flash,
            redirect,
            url_for,
            jsonify,
            abort
            )
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import FlaskForm
# from forms import *
from models import *
from datetime import datetime

from auth import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import or_
import sys

RESULTS_PER_PAGE = 10
def paginate(request, results):
    page = request.args.get('page', 1, type=int)
    start = (page - 1)*RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE

    results = [result.format() for result in results]
    current_results = results[start:end]
    if page>1 and not current_results:
        abort(404)

    return current_results

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    migrate = Migrate(app, db)
    CORS(app)


    @app.after_request
    def after_request(response):
        response.headers.add(
                            'Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true'
        )
        response.headers.add(
                            'Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS'
        )
        return response
    # ========================================================================
    # Index route just to check that API is running or not
    # ========================================================================
    @app.route('/')
    def index():
        return jsonify({
                    'success':True
                    })

    # ========================================================================
    #  ACTOR Routes
    # ========================================================================
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.all()
        current_actors = paginate(request, actors)

        return jsonify({
                    'success' : True,
                    'actors' : current_actors,
                    'total_actors' : len(actors)
                    })

    @app.route('/actors/<int:actor_id>')
    @requires_auth('get:actors')
    def get_actor(payload, actor_id):
        actor = None
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        return jsonify({
                    'success' : True,
                    'actor' : actor.format(),
                    'movies' : [movie.format() for movie in actor.movies],
                    'total_movies' : len(actor.movies),
                    })

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actor(payload):
        actor = None
        body = request.get_json()

        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movies = body.get('movies', None)

        try:
            actor = Actor(
                        name = name,
                        age = age,
                        gender = gender,
                        )

            if movies and len(movies):
                related_movies = []
                for movie_id in movies.split(','):
                    if movie_id:
                        t_movie = Movie.query.filter_by(
                                                        id=int(movie_id)
                                                        ).one_or_none()
                        if t_movie:
                            related_movies.append(t_movie)
                actor.movies = related_movies
        except Exception as e:
            print(sys.exc_info())
            abort(400)

        try:
            actor.insert()
        except Exception as e:
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

        return jsonify({
                    'success':True,
                    'total_actors':len(Actor.query.all()),
        })

    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(payload, actor_id):
        actor = None
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)

        body = request.get_json()
        name = body.get('name', None)
        age = body.get('age', None)
        gender = body.get('gender', None)
        movies = body.get('movies', None)

        try:
            if name:
                actor.name = name
            if age:
                actor.age = age
            if gender:
                actor.gender = gender
            if movies and len(movies):
                related_movies = []
                for movie_id in movies.split(','):
                    if movie_id:
                        movie = Movie.query.filter_by(
                                                    id=movie_id
                                                    ).one_or_none()
                        if movie:
                            related_movies.append(movie)
                actor.movies = related_movies
        except Exception as e:
            print(sys.exc_info())
            abort(400)

        try:
            actor.update()
        except Exception as e:
            print(sys.exc_info())
            abort(422)

        return jsonify({
                    'success':True,
                    'updated':actor_id,
        })

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, actor_id):
        actor = Actor.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except Exception as e:
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

        return jsonify({
                    'success':True,
                    'deleted':actor_id,
                    'total_actors':len(Actor.query.all()),
        })
    # ========================================================================
    # MOVIE Routes
    # ========================================================================
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        movies = Movie.query.all()
        current_movies = paginate(request, movies)

        return jsonify({
                    'success' : True,
                    'movies' : current_movies,
                    'total_movies' : len(movies)
                    })

    @app.route('/movies/<int:movie_id>')
    @requires_auth('get:movies')
    def get_movie(payload, movie_id):
        movie = None
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        
        return jsonify({
                    'success' : True,
                    'movie' : movie.format(),
                    'actors' : [actor.format() for actor in movie.actors],
                    'total_actors' : len(movie.actors),
                    })

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        movie = None
        body = request.get_json()

        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)

        try:
            movie = Movie(
                            title = title,
                            release_date = release_date,
                            )
            if actors and len(actors):
                related_actors = []
                for actor_id in actors.split(','):
                    if actor_id:
                        actor = Actor.query.filter_by(
                                                    id=actor_id
                                                    ).one_or_none()
                        if actor:
                            related_actors.append(actor)
                movie.actors = related_actors
        except Exception as e:
            print(sys.exc_info())
            abort(400)

        try:
            movie.insert()
        except Exception as e:
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

        return jsonify({
                    'success':True,
                    'total_movies':len(Movie.query.all()),
        })

    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(payload, movie_id):
        movie = None
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)

        body = request.get_json()
        title = body.get('title', None)
        release_date = body.get('release_date', None)
        actors = body.get('actors', None)

        try:
            if title:
                movie.title = title
            if release_date:
                movie.release_date = release_date
            if actors and len(actors):
                related_actors = []
                for actor_id in actors.split(','):
                    if actor_id:
                        actor = Actor.query.filter_by(
                                                    id=actor_id
                                                    ).one_or_none()
                        if actor:
                            related_actors.append(actor)
                movie.actors = related_actors

        except Exception as e:
            print(sys.exc_info())
            abort(400)

        try:
            movie.update()
        except Exception as e:
            print(sys.exc_info())
            abort(422)

        return jsonify({
                    'success':True,
                    'updated':movie_id,
        })

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, movie_id):
        movie = Movie.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except Exception as e:
            db.session.rollback()
            print(sys.exc_info())
            abort(422)
        finally:
            db.session.close()

        return jsonify({
                    'success':True,
                    'deleted':movie_id,
                    'total_movies':len(Movie.query.all()),
        })

    # ========================================================================
    # Error Handling
    # ========================================================================
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
                    'success':False,
                    'error': 400,
                    'message': 'bad request',
        }), 400

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
                    'success':False,
                    'error': 401,
                    'message': 'unauthorized',
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
                    'success':False,
                    'error': 404,
                    'message': 'resource not found',
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                    'success':False,
                    'error': 422,
                    'message': 'unprocessable',
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
                    'success':False,
                    'error': 500,
                    'message': 'internal server error',
        }), 500
    # =======================================================================
    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)

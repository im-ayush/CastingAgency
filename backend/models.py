import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_moment import Moment
from sqlalchemy import Column, String, Integer, create_engine
import json
from sqlalchemy.ext.declarative import declarative_base

SECRET_KEY = os.urandom(32)
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True

database_path = os.environ['DATABASE_URL']
# database_name = "casting_agency"
# database_path = "postgresql://{user}:{password}@{host}/{database}".format(
#                                                         user='postgres',
#                                                         password='ayush882',
#                                                         host='localhost:5432',
#                                                         database=database_name,
#                                                         )

# WTF_CSRF_ENABLED = False

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
projects = db.Table('projects', db.Model.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'))
)
class Movie(db.Model):
    __tablename__ = 'movies'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Title
    title = db.Column(db.String(120), nullable=False)
    # Date
    release_date = db.Column(db.Date, nullable=True)

    # Foreign Key to actors table
    # Establishes a two way relationship with Actor
    actors = db.relationship(
                            "Actor",
                            lazy = True,
                            secondary = projects,
                            backref = 'movies',
                            )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    '''
    insert()
        inserts a new model into a database
        the model must have a not null title
        the model can have a release date (optional)
        the model can have actors object list(optional)
        EXAMPLE
            movie = Movie(title=movie_title, release_date=movie_release_date)
            drink.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a model in the database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.title = 'XYZ'
            movie.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a model from database
        the model must exist in the database
        EXAMPLE
            drink = Movie(title=movie_title, release_date=movie_release_date)
            drink.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    format()
        formats python object into JSON format
    '''
    def format(self):
        return {
            'id' : self.id,
            'title' : self.title,
            'release_date' : self.release_date.strftime("%d %B, %Y"),
        }



class Actor(db.Model):
    __tablename__ = 'actors'
    # Autoincrementing, unique primary key
    id = db.Column(db.Integer, primary_key=True)
    # String Name
    name = db.Column(db.String(120), nullable=False)
    # String Gender
    gender = db.Column(db.String(20), nullable=False)
    # String Age
    age = db.Column(db.String(3), nullable=False)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    '''
    insert()
        inserts a new model into a database
        the model must have a not null name, gender, age
        the model can have movie object list(optional)
        EXAMPLE
            actor = Actor(name=actor_name, gender=actor_gender, age=actor_age)
            actor.insert()
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    update()
        updates a model in the database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.name = 'XYZ'
            actor.update()
    '''
    def update(self):
        db.session.commit()

    '''
    delete()
        deletes a model from database
        the model must exist in the database
        EXAMPLE
            actor = Actor(name=actor_name, gender=actor_gender, age=actor_age)
            actor.delete()
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    format()
        formats python object into JSON format
    '''
    def format(self):
        return {
            'id' : self.id,
            'name' : self.name,
            'age' : self.age,
            'gender' : self.gender,
        }

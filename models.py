from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

# database_name = "capstone"
# database_path = "postgres://{}/{}".format('localhost:5432', database_name)

database_path = os.environ['DATABASE_URL']

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


'''
Movie
Have title and release date
'''


class Movie(db.Model):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)  #movie id
    title = Column(String)  #movie title
    release_date = db.Column(db.Date)  #movie release date

    # actors = db.relationship('Actor', backref='movies')

    # def __init__(self, title, release_date):

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date  #,
            # 'actors': self.actors
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())


'''
Actor
Have name, age, and gender
'''


class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)  #actor id
    name = Column(String)  #actor name
    age = db.Column(db.Integer)  #actor age
    gender = db.Column(db.String)  #actor gender

    # movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender  #,
            # 'movie_id': self.movie_id
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.format())

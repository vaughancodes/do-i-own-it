import logging

from flask_sqlalchemy import SQLAlchemy
from app import app, db

class Movies(db.Model):
    __tablename__ = 'movies'

    title = db.Column('title', db.String(100))
    year = db.Column('year', db.Integer)
    poster_image_url = db.Column('poster_image_url', db.String(512), nullable=True)
    imdb_id = db.Column('imdb_id', db.String(32), primary_key=True)

    def __init__(self, data):
        self.title = data.get("title")
        self.year = data.get("year")
        self.poster_image_url = data.get("poster_image_url")
        self.imdb_id = data.get("imdb_id")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class OwnedMovieFormats(db.Model):
    __tablename__ = 'owned_movie_formats'

    imdb_id = db.Column('imdb_id', db.String(32), db.ForeignKey('movies.imdb_id'), primary_key=True)
    uhd_bluray = db.Column('uhd_bluray', db.Boolean, unique=False, default=False)
    bluray = db.Column('bluray', db.Boolean, unique=False, default=False)
    dvd = db.Column('dvd', db.Boolean, unique=False, default=False)

    movie = db.relationship("Movies", backref=db.backref("movies", uselist=False))

    def __init__(self, data):
        self.imdb_id = data.get("imdb_id")
        self.uhd_bluray = data.get("uhd_bluray")
        self.bluray = data.get("bluray")
        self.dvd = data.get("dvd")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



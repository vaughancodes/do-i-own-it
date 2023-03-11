# Python built-in
import os
import json
import urllib
import logging

# External packages
from flask import Flask, request, jsonify, Response
from sqlalchemy import exc
import requests

# Internal modules
from models import Movies, OwnedMovieFormats
from app import app, db
from config import *

def default_response():
    return {
        "status": 400,
        "message": "Default message.",
        "data": {}
    }

params_mapping = {
    "title": "s", 
    "year": "y",
    "imdb_id": "i"
}

@app.route('/search/movies', methods=['GET'])
def search_for_movies():
        response_dict = default_response()
        first_param = True
        query_url = OMDB_API_ENDPOINT

        for param_key in params_mapping.keys():
            if request.args.get(param_key):
                param = request.args.get(param_key)
                if first_param:
                    query_url += f"?{params_mapping[param_key]}={urllib.parse.quote(param)}"
                    first_param = False
                else:
                    query_url += f"&{params_mapping[param_key]}={urllib.parse.quote(movie_title)}"

        if first_param:
            response_dict["message"] = "No movie title and/or year provided for search!"
            return Response(json.dumps(response_dict), status=400, mimetype='application/json')
        else:
            query_url += f"&apikey={OMDB_API_KEY}" 
            rq = requests.get(query_url)
            if rq.status_code != 200:
                response_dict["status"] = 400
                response_dict["message"] = "Failed to search movie via OMDb!"
                response_dict["data"] = rq.json()
                return Response(json.dumps(response_dict), status=400, mimetype='application/json')
            response_dict["status"] = 200
            response_dict["message"] = "Searched for movies successfully!"
            logging.error(rq.text)
            response_dict["data"] = rq.json()
            return Response(json.dumps(response_dict), status=200, mimetype='application/json')


@app.route('/library/movies', methods=['GET', 'POST'])
def register_movie_in_library():
    response_dict = default_response()
    if request.method == "POST":
        if not request.args.get("imdb_id"):
            response_dict["status"] = 400
            response_dict["message"] = "No IMDb ID was provided for movie registration!"
            return Response(json.dumps(response_dict), status=400, mimetype='application/json')

        imdb_id = request.args.get("imdb_id")
        rq = requests.get(f"{OMDB_API_ENDPOINT}?i={urllib.parse.quote(imdb_id)}&apikey={OMDB_API_KEY}")
        movie_dict = {
            "title": rq.json()["Title"],
            "year": rq.json()["Year"],
            "poster_image_url": rq.json()["Poster"],
            "imdb_id": imdb_id
        }
        movie = Movies(movie_dict)
        try:
            db.session.add(movie)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            response_dict["status"] = 400
            response_dict["message"] = f"Failed to insert! - {str(e)}"
            return Response(json.dumps(response_dict), status=400, mimetype='application/json')

        response_dict["status"] = 200
        response_dict["message"] = "Inserted successfully!"
        response_dict["data"] = rq.json()
        return Response(json.dumps(response_dict), status=200, mimetype='application/json')
    if request.method == "GET":
        movies = []
        for movie in Movies.query.all():
            movies.append(movie.to_dict())
        response_dict["status"] = 200
        response_dict["message"] = "Retrieved movies in library!"
        response_dict["data"] = movies
        logging.error(response_dict)
        return Response(json.dumps(response_dict), status=200, mimetype='application/json')

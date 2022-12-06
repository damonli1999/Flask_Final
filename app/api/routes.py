# Location and rules of the server
# Allows two machines to talk to each other

# jsonify will reformat our data into json so we can use it with Python and JS
from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Movie, movie_schema, movies_schema

# url_prefix means we need api in front of our end slug.
api = Blueprint('api',__name__, url_prefix='/api')

# allows us to pull data into insomnia
@api.route('/getdata')
def getdata():
    return {'cat': 'dog'}

# This will post Movie data to the database (on insomnia) -- mimics another back end app requesting data with our flask app
# token is required to send the data
@api.route('/movies', methods = ['POST'])
@token_required
def create_movie(current_user_token):
    title = request.json['title']
    director = request.json['director']
    writer = request.json['writer']
    release_year = request.json['release_year']
    stars = request.json['stars']
    genre = request.json['genre']
    user_token = current_user_token.token

# Tells us in the terminal if everything up to this point has worked.
    print(f'BIG TESTER: {current_user_token.token}')

# Instantiates the Movie class with the data we just pulled from the json
    movie = Movie(title, director, writer, release_year, stars, genre, user_token = user_token )

# puts all the info into the database
    db.session.add(movie)
    db.session.commit()

    response = movie_schema.dump(movie)
    return jsonify(response)


# Gets all the movie data from our database and displays it in Insomnia in json format
@api.route('/movies', methods = ['GET'])
@token_required
def get_movie(current_user_token):
    a_user = current_user_token.token
    movies = Movie.query.filter_by(user_token = a_user).all()
    response = movies_schema.dump(movies)
    return jsonify(response)

# If we want a specific movie we can call it with an id number
# We're querying by id number, then returning the data that query grabs
@api.route('/movies/<id>', methods = ['GET'])
@token_required
def get_single_movie(current_user_token, id):
    movie = Movie.query.get(id)
    response = movie_schema.dump(movie)
    return jsonify(response)

# Get all the data from our query by the passed in ID
# save them all to a movie, and then individually rewrite them
# We have to manually update the JSON piece
@api.route('/movies/<id>', methods = ['POST','PUT'])
@token_required
def update_movie(current_user_token,id):
    movie = Movie.query.get(id) 
    movie.title = request.json['title']
    movie.director = request.json['director']
    movie.writer = request.json['writer']
    movie.release_year = request.json['release_year']
    movie.stars = request.json['stars']
    movie.genre = request.json['genre']
    movie.user_token = current_user_token.token

    db.session.commit()
    response = movie_schema.dump(movie)
    return jsonify(response)

# Delete books by id
# If we didn't do it by id we'd delete the whole database
@api.route('/movies/<id>', methods = ['DELETE'])
@token_required
def delete_movie(current_user_token, id):
    movie = Movie.query.get(id)
    db.session.delete(movie)
    db.session.commit()
    response = movie_schema.dump(movie)
    return jsonify(response)
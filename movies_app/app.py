import boto3
from flask import Flask, request, jsonify

from movies_app.service_layer.get_movie import get_movie
from movies_app.service_layer.insert_movie import insert_movie
from movies_app.service_layer.delete_movie import delete_movie
from movies_app.service_layer.MoviesCreateTable import create_movie_table


dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:8000")

app = Flask(__name__)

def _sanitize_title(title):
    # To avoid spaces in URLs, use underscores and then replace '_' with ' '
    return title.replace('_', ' ')


@app.route('/movies', methods=['GET'])
def get_movies():
    return jsonify(dynamodb.scan(TableName='Movies'))



@app.route('/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    required_fields = {'title', 'year', 'plot', 'rating'}
    if not required_fields.issubset(data):
        return jsonify({'error': 'Missing required fields'}), 400

    response = insert_movie(
        title=data['title'],  # no need to sanitize this
        year=int(data['year']),
        plot=data['plot'],
        rating=float(data['rating'])
    )
    return jsonify({'message': 'Movie inserted successfully', 'response': response}), 201


@app.route('/movies/<int:year>/<string:title>', methods=['GET'])
def retrieve_movie(year, title):
    title = _sanitize_title(title)
    try:
        movie = get_movie(title=title, year=year)
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404
        return jsonify(movie), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/movies/<int:year>/<string:title>', methods=['DELETE'])
def delete_movie(year, title):
    title = _sanitize_title(title)
    try:
        response = delete_movie(title=title, year=year)
        return jsonify({'message': 'Movie deleted successfully', 'response': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':

    # create the 'Movies' table and insert a single movie

    create_movie_table()
    movie = get_movie("The Big New Movie", 2015)
    if movie is None:
        insert_movie("The Big New Movie", 2015,
                              "Nothing happens at all.", 0)
    app.run(debug=True)

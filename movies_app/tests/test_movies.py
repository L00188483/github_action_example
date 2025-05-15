from datetime import datetime
import time

import boto3
import docker
from pprint import pprint
import pytest

from movies_app.MoviesCreateTable import create_movie_table
from movies_app.insert_movie import insert_movie
from movies_app.get_movie import get_movie
from movies_app.delete_movie import delete_movie


MOVIE_TITLE = "A Test Movie"
MOVIE_YEAR = 2015
MOVIE_PLOT = "This is a plot."


@pytest.fixture   # or: @pytest.fixture(scope="session")
def dynamodb_container():
    # Python equivalent to launching a docker container i.e. equivalent to:
    #  $ docker run -d --rm -p 8000:8000 --name=dynamodb amazon/dynamodb-local -jar DynamoDBLocal.jar

    # python client for interacting with docker:
    client = docker.from_env()

    container_name = f"dynamodb-test-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # run a container:
    container = client.containers.run(
        "amazon/dynamodb-local",
        command="-jar DynamoDBLocal.jar",
        ports={"8000/tcp": 8000},
        name=container_name,
        detach=True,
        remove=True  # auto-remove when stopped
    )
    time.sleep(2)

    yield container
    container.stop()


@pytest.fixture
def dynamodb_connection(dynamodb_container):
    yield boto3.resource(
        'dynamodb', endpoint_url="http://localhost:8000",
        region_name='eu-west-1'
    )


@pytest.fixture
def movie_table(dynamodb_connection):
    yield create_movie_table(dynamodb=dynamodb_connection)


def _count_table_items(dynamodb_connection, table_name):
    table = dynamodb_connection.Table(table_name)
    response = table.scan()
    return len(response['Items'])



############### Tests ##################


def test_insert_and_get_movie(movie_table, dynamodb_connection):

    insert_movie(
        MOVIE_TITLE, MOVIE_YEAR, MOVIE_PLOT, 0,
        dynamodb=dynamodb_connection
    )

    movie = get_movie(
        MOVIE_TITLE,
        MOVIE_YEAR,
        dynamodb=dynamodb_connection
    )

    num_movies = _count_table_items(
        dynamodb_connection, 'Movies'
    )

    assert num_movies == 1
    assert movie is not None
    assert movie['title'] == MOVIE_TITLE
    assert movie['year'] == MOVIE_YEAR


def test_delete_movie(movie_table, dynamodb_connection):

    insert_movie(
        MOVIE_TITLE, MOVIE_YEAR, MOVIE_PLOT, 0,
        dynamodb=dynamodb_connection
    )

    num_movies_before = _count_table_items(
        dynamodb_connection, 'Movies'
    )

    delete_movie(
        MOVIE_TITLE,
        MOVIE_YEAR,
        dynamodb=dynamodb_connection
    )

    num_movies_after = _count_table_items(
        dynamodb_connection, 'Movies'
    )

    assert num_movies_before == 1
    assert num_movies_after == 0

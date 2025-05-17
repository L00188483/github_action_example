import time

import boto3
import docker
from pprint import pprint
import pytest

from movies_app.service_layer.MoviesCreateTable import create_movie_table
from movies_app.service_layer.insert_movie import insert_movie
from movies_app.service_layer.get_movie import get_movie
from movies_app.service_layer.delete_movie import delete_movie


# setup variables for the tests below (test_insert_and_get_movie, test_delete_movie)
MOVIE_TITLE = "A Test Movie"
MOVIE_YEAR = 2015
MOVIE_PLOT = "This is a plot."


def create_dynamodb_container():
    """
    Python equivalent to launching a docker container i.e. equivalent to:
      $ docker run -d --rm -p 8000:8000 --name=dynamodb amazon/dynamodb-local -jar DynamoDBLocal.jar
    """

    # python client for interacting with docker:
    client = docker.from_env()

    container_name = "dynamodb-test"

    # delete container if it already exists
    try:
        existing_container = client.containers.get(container_name)
        print(f"Container '{container_name}' already exists. Removing it...")
        existing_container.stop()  # stop() also removes it when remove=True
        time.sleep(3)

    except docker.errors.NotFound:
        pass

    # run a container:
    return client.containers.run(
        "amazon/dynamodb-local",
        command="-jar DynamoDBLocal.jar",
        ports={"8000/tcp": 8000},
        name=container_name,
        detach=True,
        remove=True  # auto-remove when stopped
    )


def _count_table_items(dynamodb_connection, table_name):
    table = dynamodb_connection.Table(table_name)
    response = table.scan()
    return len(response['Items'])


@pytest.fixture
def dynamodb_connection():

    # Create the DynamoDB container
    container = create_dynamodb_container()
    time.sleep(2)

    # Make a connection to the DB
    dynamodb_connection = boto3.resource(
        'dynamodb',
        endpoint_url="http://localhost:8000",
        region_name='eu-west-1',
        aws_access_key_id="fakeMyKeyId",
        aws_secret_access_key="fakeSecretAccessKey"
    )

    # create the 'Movies' table
    create_movie_table(dynamodb=dynamodb_connection)

    # return the connection
    yield dynamodb_connection

    # after a test completes, stop the container
    container.stop()


############### Tests ##################


# this test depends on the 'dynamodb_connection' fixture
def test_insert_and_get_movie(dynamodb_connection):

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


def test_delete_movie(dynamodb_connection):

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

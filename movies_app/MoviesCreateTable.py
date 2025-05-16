import boto3


def create_movie_table(dynamodb=None):
    """
    Create 'Movies' table if it does not exist.
    """
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    try:
        # Check if table exists by trying to describe it
        table = dynamodb.Table('Movies')
        table.load()  # This will raise ResourceNotFoundException if table doesn't exist
        print("Table 'Movies' already exists.")
        return table
    except ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'ResourceNotFoundException':
            return _create_movie_table(dynamodb=dynamodb)
        else:
            raise e


def _create_movie_table(dynamodb):
    """ Create 'Movies' table. """
    table = dynamodb.create_table(
        TableName='Movies',
        KeySchema=[
            {
                'AttributeName': 'year',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'title',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'year',
                'AttributeType': 'N'
            },
            {
                'AttributeName': 'title',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    movie_table = create_movie_table()
    print("Table status:", movie_table.table_status)

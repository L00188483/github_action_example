import boto3
from flask import Flask, jsonify

dynamodb = boto3.client('dynamodb', endpoint_url="http://localhost:8000")

app = Flask(__name__)


@app.route('/')
def index():
    return "This is the main page."
    
@app.route('/get-items')
def get_items():
    return jsonify(dynamodb.scan(TableName='Movies'))


if __name__=='__main__':
    app.run()

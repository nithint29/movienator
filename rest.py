from flask import Flask, jsonify
import boto3
import json
import decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

app = Flask(__name__)
app.json_encoder = DecimalEncoder

# GET
@app.route('/info')
def get_movie_info():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('movies')

    response = table.scan(
        ExpressionAttributeValues={
            ':status':'Released',
        },
        ExpressionAttributeNames={
            '#release_status':'status'
        },
        ProjectionExpression='title,genres,poster_path,revenue',
        FilterExpression='#release_status <> :status'
    )

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'],
                ExpressionAttributeValues={
                    ':released':'Released',
                },
                ExpressionAttributeNames={
                    '#release_status':'status'
                },
                ProjectionExpression='title,genres,poster_path,revenue',
                FilterExpression='#release_status <> :status'
            )
            items += response['Items']
        else:
            break
    
    return jsonify(items)


# GET
@app.route('/past')
def get_past_info():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('movies')

    response = table.scan(
        ExpressionAttributeValues={
            ':status': 'Released',
        },
        ExpressionAttributeNames={
            '#release_status': 'status'
        },
        ProjectionExpression='title,genres,poster_path,revenue',
        FilterExpression='#release_status  =:status'
    )

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'],
                ExpressionAttributeValues={
                    ':released': 'Released',
                },
                ExpressionAttributeNames={
                    '#release_status': 'status'
                },
                ProjectionExpression='title,genres,poster_path,revenue',
                FilterExpression='#release_status =:status'
            )
            items += response['Items']
        else:
            break

    return jsonify(items)

if __name__ == '__main__':
    app.run(host='172.30.20.201', port=5000)
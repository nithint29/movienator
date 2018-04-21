from flask import Flask
import boto3

app = Flask(__name__)

@app.route("/movies")
def retrieve_movies(table):
    response = table.scan(
        ExpressionAttributeValues={
            ':status':'Released',
        },
        ExpressionAttributeNames={
            '#release_status':'status'
        },
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
                FilterExpression='#release_status <> :status'
            )
            items += response['Items']
        else:
            break

    return items

if __name__ == '__main__':
    
    #dynamodb = boto3.resource('dynamodb')
    #table = dynamodb.Table('movies')

    #items=retrieve_movies(table)

    app.run(host='0.0.0.0', port=5000)
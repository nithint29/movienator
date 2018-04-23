from flask import Flask
import boto3

app = Flask(__name__)

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
    app.run(host='0.0.0.0', port=5000)
from flask import Flask
import boto3

app = Flask(__name__)

# GET
@app.route("/movies")
def retrieve_revenue(table):
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

    revenues=[]
    for item in items:
        revenues.append(item['revenue'])
    
    return revenues

if __name__ == '__main__':
    
    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('movies')

    app.run(host='0.0.0.0', port=5000)
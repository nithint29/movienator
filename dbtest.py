import boto3
from boto3.dynamodb.conditions import Key, Attr
from sklearn.feature_extraction import DictVectorizer

features = ['Adult', 'Budget', 'Runtime', 'Genre']

def pre_process(response):
    X = []
    for movie in response['Items']:
        x = {}


if __name__=='__main__':
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('movies')

    print(table.creation_date_time)
    # print(table.scan())

    response = table.query(
        KeyConditionExpression=Key('Title').eq("Inception")
    )

    print(response['Items'][0])


    pre_process(response)




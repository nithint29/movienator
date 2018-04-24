import boto3
from time import sleep
from tmdbv3api import TMDb, Movie, Person
from botocore.exceptions import ClientError

def scan_table(table):
    response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items

def append_id(ids,items):
    for item in items:
        ids.append(item['id'])

def update_poster_paths(table,items,ids):
    for (item,id) in zip(items,ids):
        sleep(0.26)
        det=movie.details(id)
        if(hasattr(det, 'poster_path')):
           
            poster_path=getattr(det,'poster_path')
        
            response = table.update_item(
                Key={
                    'id': item['id'] 
                },
                UpdateExpression='set #value1 = :val1',
                ExpressionAttributeNames={
                    '#value1':'poster_path'
                },
                ExpressionAttributeValues={
                    ':val1':poster_path
                },
                ConditionExpression='attribute_exists(id)',
                ReturnValues="UPDATED_NEW"
            )
        else:
            print(id)

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    moviesnew = dynamodb.Table('movies_new')
    movies = dynamodb.Table('movies')

    tmdb = TMDb()
    movie = Movie()

    tmdb.api_key='a334426826809d332101199d1acebb0f'

    items=scan_table(movies)

    ids=[]
    append_id(ids,items)

    update_poster_paths(movies,items,ids)
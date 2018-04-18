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
        ids.append(item['ID'])

def update_ids(table,items,ids):
    for (item,id) in zip(items,ids):
        sleep(0.26)
        credits=movie.credits(id)
        pids=[]
        if(hasattr(credits, 'cast')):
            for m in credits.cast[:10]:
                pid=m.get('id') if m.get('id') != '' else None
                pids.append(pid)
            
            response = table.update_item(
                Key={
                    'Title': item['Title'],
                    'ID': item['ID'] 
                },
                UpdateExpression='set #value1 = :val1',
                ExpressionAttributeNames={
                    '#value1':'person_ids'
                },
                ExpressionAttributeValues={
                    ':val1':pids
                },
                ConditionExpression='attribute_exists(Title) and attribute_exists(ID)',
                ReturnValues="UPDATED_NEW"
            )
        else:
            print(id)

if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    moviesnew = dynamodb.Table('movies_new')

    tmdb = TMDb()
    movie = Movie()

    tmdb.api_key='a334426826809d332101199d1acebb0f'

    items=scan_table(moviesnew)

    ids=[]
    append_id(ids,items)

    update_ids(moviesnew,items,ids)
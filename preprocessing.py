import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal

features = ['Adult', 'Budget', 'Runtime', 'vote_average', 'Popularity', 'original_language', 'vote_count']
complex_features = ['spoken_languages', 'production_countries', 'Genres', 'production_companies']
# Genres = {'Western', 'Action', 'Comedy', 'Romance', 'Documentary', 'Thriller', 'War', 'Crime', 'Science Fiction', 'History', 'Mystery', 'Music', 'Fantasy', 'Adventure', 'Foreign', 'Family', 'Horror', 'Animation', 'Drama'}

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

def pre_process(data, f = None, cf = None):
    if (cf != None):
        complex_features = cf
    if(f != None):
        features = f

    X = []
    Y = []
    for movie in data:
        print(movie['Title'])
        x = {}
        for f in features:
            x[f] = movie[f]

        for cf in complex_features:
            simp= cleaner(movie, cf, 'Name')

            for s in simp:
                x[s] = True

        Y.append(movie['Revenue'])
        X.append(x)

    return X, Y


def extractor(response, dictList, attribute):
    ### example: extractor(table.scan()['Items'], 'Genres', 'Name')

    s = set([])
    for movie in response:
        for g in movie[dictList] if movie[dictList] != None else []:
            s.add(g[attribute])

    return list(s)

def cleaner(movie, dictList, attribute):
    ### example: extractor(movie, 'Genres', 'Name')

    s = set([])
    for g in movie[dictList] if movie[dictList] != None else []:
        s.add(g[attribute])

    return list(s)

def fullscan(table):
    response = table.scan()
    data = response['Items']

    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data

def release_info(table):
    response = fullscan(table)

    for movie in response:
        release= movie['release_date'].split('-')
        month = decimal.Decimal(release[1])
        quarter = decimal.Decimal( (int(release[1])-1)//3 + 1)
        update = table.update_item(
            Key={
                'id':movie['id']
            },
            UpdateExpression="set release_month = :m, release_quarter = :q",
            ExpressionAttributeValues={
                ':m':month,
                ':q':quarter
            },
            ReturnValues="UPDATED_NEW"
        )
        print(update)


if __name__=='__main__':
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('movies')

    print(table.creation_date_time)
    # print(table.scan())

    # response = table.query(
    #     KeyConditionExpression=Key('Title').eq("Inception")
    # )

    data = fullscan(table)

    print(len(data))

    release_info(table)





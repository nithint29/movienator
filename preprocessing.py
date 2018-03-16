import boto3
from boto3.dynamodb.conditions import Key, Attr
from sklearn.feature_extraction import DictVectorizer

features = ['Adult', 'Budget', 'Runtime', 'vote_average', 'Popularity', 'original_language', 'vote_count']
complex_features = ['spoken_languages', 'production_countries', 'Genres', 'production_companies']
# Genres = {'Western', 'Action', 'Comedy', 'Romance', 'Documentary', 'Thriller', 'War', 'Crime', 'Science Fiction', 'History', 'Mystery', 'Music', 'Fantasy', 'Adventure', 'Foreign', 'Family', 'Horror', 'Animation', 'Drama'}

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




if __name__=='__main__':
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('movies')

    print(table.creation_date_time)
    # print(table.scan())

    response = table.query(
        KeyConditionExpression=Key('Title').eq("Inception")
    )

    # print(response['Items'][0])

    # for cf in complex_features:
    #     simplified = cleaner(response['Items'][0], cf, 'Name')
    #     print(cf)
    #     print(response['Items'][0][cf])


    # pre_process(response['Items'])

    # print(extractor(response['Items'], 'spoken_languages', 'Name'))

    # data = table.scan()['Items']
    # X,Y = pre_process(data)

    response = table.scan()
    data = response['Items']
    print(len(data))

    while response.get('LastEvaluatedKey'):
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    print(len(data))




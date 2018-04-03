import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import boto3
import os
import pytz
import omdb
import csv

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
# Get the service resource.
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('movies_new')

#setting api key
omdb.set_default('apikey', '3d0a11ee')
#client = omdb.OMDBClient(apikey='3d0a11ee')

def scan_table():
    response = table.scan()
    #data = response['Items']

    items = response['Items']
    while True:
        #print(len(response['Items']))
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items
movs= scan_table()
mylist = []
for i in movs:
    title = i['Title']
    mylist.append(title)

rottenscores = []
f = open("allrottens.csv","w")
with f:
    myfields = ['movname','rotten']
    writer = csv.DictWriter(f, fieldnames=myfields) 
    for i in mylist:
        print(i)
        try:
            x = omdb.get(title=i)
            writer.writerow({'movname': i, 'rotten':str(x['ratings'][1]['value'])})
        except (KeyError, IndexError,UnicodeEncodeError) as e:
            writer.writerow({'movname': i.encode('utf-8'), 'rotten':'No ratings'})

f.close()
 #   rottenscores.append(str(x['ratings'][1]['value']))
#omdb.set_default('apikey', '3d0a11ee')
#omdb.set_default('tomatoes', True)
#x = omdb.get(title='Shark Night')
#y = omdb.title('Avatar', year = 2009, tomatoes = True)


#print(rottenscores)

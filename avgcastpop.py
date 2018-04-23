from __future__ import print_function # Python 2/3 compatibility
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import boto3
import os
import pytz
import decimal
import csv
from pytrends.request import TrendReq



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
movTable = dynamodb.Table('movies')
castTable = dynamodb.Table('cast_new')
crewTable = dynamodb.Table('crew')

def scan_table():
    response = movTable.scan()
    #data = response['Items']

    items = response['Items']
    while True:
        #print(len(response['Items']))
        if response.get('LastEvaluatedKey'):
            response = movTable.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items
movs= scan_table()
mylist = []
for i in movs:
    movid = i['id']
    mylist.append(movid)

avgPop = []
count = 1
#f = open("avgpop4.csv","w")
#with f:
    #myfields = ['movname', 'avgpop']
    #writer = csv.DictWriter(f, fieldnames = myfields)
for mov in mylist:
    try:
        print(count)
        response2 = movTable.query(
        KeyConditionExpression=Key('id').eq(mov)
        )
        D = decimal.Decimal
        for i in response2['Items']:
                #print(i['person_ids'][0])
            popsum = 0
            leng = 0
            for x in i['person_ids']:   #going through all personids
                castResp = castTable.query(
                KeyConditionExpression=Key('person_id').eq(x)
                )
                crewResp = crewTable.query(
                KeyConditionExpression=Key('person_id').eq(x)
                )
                if len(castResp['Items'])!=0:
                    for i in castResp['Items']:
                        if i['popularity'] != 'None':
                            #print(i['popularity'])
                            leng = leng + 1
                            popsum = popsum + D(i['popularity'])
                        else:
                            for i in crewResp['Items']:
                                if i['popularity'] != 'None':
                                        #print(i['popularity'])
                                    leng = leng + 1
                                    popsum = popsum + D(i['popularity'])
                #writer.writerow({'movname': mov, 'avgpop': (popsum/leng)})
            print(popsum/leng)                        
            avgPop.append(popsum/leng)
            count = count + 1
    except (KeyError, IndexError, UnicodeEncodeError, ZeroDivisionError) as e:
            #writer.writerow({'movname': mov.encode('utf-8'), 'avgpop': 'No avg pop'})
        avgPop.append('No avg pop')    
            #print(popsum)
            #print(leng)
 
    
    

for item, v in zip(movs, avgPop) :
        response = movTable.update_item(
            Key={
                'id': item['id'] 
            },
            UpdateExpression="set #attrName = :attrValue",
            ExpressionAttributeNames={
                "#attrName" : "AvgCastCrewPop"
            },
            ExpressionAttributeValues={
                ':attrValue': v
            },
            ConditionExpression="attribute_exists(id)",
            ReturnValues="UPDATED_NEW"
        )    
#f.close()

#print(avgpop)
 #   avgPop.append(popsum/leng)
    #for i in response3['Items']:
    #   print(i['popularity'])

#print(len(mylist))


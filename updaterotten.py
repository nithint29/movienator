import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import boto3
import os
import pytz
import omdb
import csv
import pandas as pd

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

file = open("allrottens.csv")
reader = csv.reader(file)

scores = []
for line in reader:
    scores.append(line[1])


for item, v in zip(movs, scores) :
        response = table.update_item(
            Key={
                'Title': item['Title'],
                'ID': item['ID'] 
            },
            UpdateExpression="set #attrName = :attrValue",
            ExpressionAttributeNames={
                "#attrName" : "RottenTomatoScore"
            },
            ExpressionAttributeValues={
                ':attrValue': v
            },
            ConditionExpression="attribute_exists(Title) and attribute_exists(ID)",
            ReturnValues="UPDATED_NEW"
        )



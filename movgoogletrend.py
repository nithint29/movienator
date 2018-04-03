# -*- coding: utf-8 -*-
from __future__ import print_function # Python 2/3 compatibility
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import boto3
import os
import pytz
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
table = dynamodb.Table('movies_new')
#creating google trend table
googletrend = dynamodb.Table('GoogleTrendStuff')

def isEnglish(s):
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

    
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

# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

mynum = 905
num = 154756

while mynum <=960:
    print('mynum=', mynum)
    pytrend.build_payload(kw_list=mylist[mynum:mynum+5], timeframe='all', geo='US')
    result = interest_over_time_df = pytrend.interest_over_time()
    tot_term = [interest_over_time_df]
    dc = result.to_dict(orient = 'dict')

    for j in range(0, len(dc.keys())):  #title loop
        if (dc.keys()[j] == 'isPartial'):
            continue
        else:
            for k in range(0, len(dc.values()[0])): #date loop
                print('num=',num)
                num = num+1;
                googletrend.put_item(
                    Item = {
                        'ID': num,
                        'Title': str(dc.keys()[j]),
                        'DateInfo':{
                            'date': dc.values()[j].keys()[k].isoformat(),
                            'searches': dc.values()[j].values()[k]
                            }
                        }
                    )
    mynum = mynum+5;








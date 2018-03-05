from __future__ import print_function # Python 2/3 compatibility
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import boto3
import os
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
table = dynamodb.Table('movies')

response = table.scan(AttributesToGet=['Title'])
mylist = []
for i in response['Items']:
    response_dict = json.loads(json.dumps(i, cls=DecimalEncoder))
    mylist.append(response_dict.get("Title",{}))


# Login to Google. Only need to run this once, the rest of requests will use the same session.
pytrend = TrendReq()

#keywords
list_mov = ["Avengers", "Captain America: Civil War", "Antman"]


pytrend.build_payload(kw_list=mylist[0:5], timeframe='all', geo='US')

# Interest Over Time, change "dfi"
interest_over_time_df = pytrend.interest_over_time()


tot_term = [interest_over_time_df]

print(interest_over_time_df.head())

interest_over_time_df.to_csv('tot_topics.csv')

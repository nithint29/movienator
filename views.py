import boto3
import os
import json
import time
import argparse
import http.client
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

DEVELOPER_KEY = 'AIzaSyAjWDb7sC0cKDFe3HU-09WeRpA_6TgANyw'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def scan_table():
    response = table.scan()

    items = response['Items']
    while True:
        if response.get('LastEvaluatedKey'):
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            items += response['Items']
        else:
            break

    return items
    
def append_titles(titles, items):
    for item in items:
        title = item['Title']
        titles.append(title)

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    search_response = youtube.search().list(q=options.q,part='id,snippet',maxResults=options.max_results
    ).execute()
    
    vid = search_response['items'][0]['id']['videoId']

    results = youtube.videos().list(part='snippet,statistics',id=vid).execute()

    if 'statistics' in results['items'][0]:
        if 'viewCount' in results['items'][0]['statistics']: #account for videos without viewcount
            vc = results['items'][0]['statistics']['viewCount']
        else:
            vc = -1
    else:
        print('There aren\'t any stats for this video yet.')
    
    return vc

if __name__ == "__main__":
    
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('movies_new')

    titles=[]
    views=[]
    data = scan_table()
    #print(len(data))

    append_titles(titles, data)
    #print(len(titles))

    #get viewcount for all items
    for i in range(0, len(titles)):
        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default=titles[i] + " trailer")
        parser.add_argument('--max-results', help='Max results', default=1)
        args = parser.parse_args()

        try:
            view = youtube_search(args)
            views.append(view)
            #count+=1
            #print(count)

        except (KeyError, HttpError) as e:
            pass
            print('An error %d occurred:\n%s' % (e.resp.status, e.content))            

        time.sleep(1)
    
    #print(len(views))
    
    #update table with viewcount
    for item, v in zip(data, views) :
        response = table.update_item(
            Key={
                'Title': item['Title'],
                'ID': item['ID'] 
            },
            UpdateExpression="set #attrName = :attrValue",
            ExpressionAttributeNames={
                "#attrName" : "trailerViews"
            },
            ExpressionAttributeValues={
                ':attrValue': int(v)
            },
            ConditionExpression="attribute_exists(Title) and attribute_exists(ID)",
            ReturnValues="UPDATED_NEW"
        )
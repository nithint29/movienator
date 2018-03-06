import boto3
import os
import json
import time
import argparse
import http.client
import google.oauth2.credentials
from pytrends.request import TrendReq
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

"""
# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret_310063786675-kk87kddiv3g0ua9n8eous466tn273422.apps.googleusercontent.com.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)
"""

DEVELOPER_KEY = 'AIzaSyAjWDb7sC0cKDFe3HU-09WeRpA_6TgANyw'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def append_titles(titles, response):
    for i in range(0, len(response['Items'])):
        title = response['Items'][i]['original_title']
        titles.append(title)

def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    search_response = youtube.search().list(q=options.q,part='id,snippet',maxResults=options.max_results
    ).execute()
    
    vid = search_response['items'][0]['id']['videoId']

    results = youtube.videos().list(part='snippet,statistics',id=vid).execute()

    if 'statistics' in results['items'][0]:
        vc = results['items'][0]['statistics']['viewCount']
    
    else:
        print('There aren\'t any localizations for this video yet.')
    
    return vc
#video_keys=[]

if __name__ == "__main__":
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')

    table = dynamodb.Table('movies')
    print(table.creation_date_time)

    response = table.scan()

    titles=[]
    views=[]
    append_titles(titles, response)

    print(len(titles))

    
    for i in range(0, len(titles)):
        parser = argparse.ArgumentParser()
        parser.add_argument('--q', help='Search term', default=titles[i] + " trailer")
        parser.add_argument('--max-results', help='Max results', default=1)
        args = parser.parse_args()

        try:
            view = youtube_search(args)
            views.append(view)

        except HttpError as e:
            print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

        time.sleep(1)
    
    for i in range(0, len(views)):
        print(views[i])
    
    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default=titles[0] + " trailer")
    parser.add_argument('--max-results', help='Max results', default=1)
    args = parser.parse_args()

    try:
        view = youtube_search(args)
        print(view)
        #print(contents[0]['items']['id']['videoId'])
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))
    """
    
    







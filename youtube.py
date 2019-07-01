# -*- coding: utf-8 -*-

# Sample Python code for youtube.liveChatMessages.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

from google.oauth2.credentials import Credentials
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from tornado.ioloop import PeriodicCallback

import config

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    # Get credentials and create an API client
    try:
        with open('youtube_credentials.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            credentials = Credentials(data['token'], data['refresh_token'], data['id_token'], data['token_uri'], data['client_id'], data['client_secret'], data['scopes'])
    except:
        client_config = config.YOUTUBE_CREDENTIALS
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(client_config, scopes)
        credentials = flow.run_console()
        data = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'id_token': credentials.id_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes,
        }
        with open('youtube_credentials.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)
    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

    request = youtube.liveBroadcasts().list(
        part="snippet,contentDetails",
        broadcastType="all",
        mine=True
    )
    response = request.execute()
    print(response)
    chat_id = None
    for broadcast in response['items']:
        chat_id = broadcast['snippet']['liveChatId']
    if chat_id is None:
        raise ValueError('Not streaming!')

    request = youtube.liveChatMessages().insert(
        part="snippet",
        body={
          "snippet": {
            "liveChatId": chat_id,
            "type": "textMessageEvent",
            "textMessageDetails": {
              "messageText": "Your cool text message goes here!"
            }
          }
        }
    )
    response = request.execute()

    print(response)

if __name__ == "__main__":
    main()

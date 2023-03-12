# Reference https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html

import os
import pickle

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import configparser

app_name = 'VideoLister'

config = configparser.ConfigParser()
config.read('config.ini')

credentials = None
pickle_token_file = config[app_name]['token_path']

if os.path.exists(pickle_token_file):
    print("Loading credentials from a pickle file")
    with open(pickle_token_file, "rb") as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid:
    if credentials and credentials.expired and credentials.refresh_token:
        print("Refreshing access token")
        credentials.refresh(Request())
        with open(pickle_token_file, "rb") as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(config[app_name]['client_secret_path'],
                                                         scopes=["https://www.googleapis.com/auth/youtube.readonly"])
        flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
        credentials = flow.credentials

        with open(pickle_token_file, "wb") as token:
            print("Saving the credentials in a pickle file")
            pickle.dump(credentials, token)

youtube = build("youtube", "v3", credentials=credentials)

request = youtube.playlistItems().list(
    part="snippet",
    playlistId=config[app_name]['playlist_id'],
    maxResults=50
)

response = request.execute()
file = open(config[app_name]['list_path'], "w")

while True:
    last_video_reached = False
    for item in response["items"]:
        snippet = item["snippet"]
        print(config[app_name]['last_video_id'])
        if config[app_name]['last_video_id'] == snippet["resourceId"]["videoId"]:
            last_video_reached = True
            break
        print(f'{snippet["title"]}: {snippet["resourceId"]["videoId"]}')
        file.write(f'{snippet["resourceId"]["videoId"]}\n')
    if "nextPageToken" not in response.keys() or last_video_reached:
        break
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=config[app_name]['playlist_id'],
        maxResults=50,
        pageToken=response["nextPageToken"]
    )
    response = request.execute()

file.close()
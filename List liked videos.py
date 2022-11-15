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

request = youtube.videos().list(
    part="snippet",
    maxResults=50,
    myRating="like"
)

response = request.execute()
file = open(config[app_name]['list_path'], "w")

while True:
    for item in response["items"]:
        snippet = item["snippet"]
        print(f'{snippet["title"]}: {item["id"]}')
        if snippet["categoryId"] == "10":  # Music videos
            file.write(f'{item["id"]}\n')
    if "nextPageToken" not in response.keys():
        break
    request = youtube.videos().list(
        part="snippet",
        maxResults=50,
        myRating="like",
        pageToken=response["nextPageToken"]
    )
    response = request.execute()

file.close()
# Reference https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html
import json
import os
import pickle
from collections import defaultdict

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import configparser

app_name = 'VideoListerForPlaylists'

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

videos_by_languages = defaultdict(list)

while True:
    video_ids = [item["snippet"]["resourceId"]["videoId"] for item in response["items"]]
    video_info_req = youtube.videos().list(
        part="snippet",
        id=",".join(video_ids)
    )
    video_info_response = video_info_req.execute()

    for item in video_info_response["items"]:
        default_audio_language = item["snippet"].get("defaultAudioLanguage")
        if not default_audio_language:
            print(f"Skipping {item["snippet"]["title"]} ({item["id"]}), reverting to default language ({default_audio_language}). "
                  f"No default language found for it.") # Unlisted but also likely unavailable
            # Seems like unlisted videos do not get defaultAudioLanguage metadata
            continue
        videos_by_languages[default_audio_language].append(item["snippet"]["title"])

    if "nextPageToken" not in response.keys():
        break
    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=config[app_name]['playlist_id'],
        maxResults=50,
        pageToken=response["nextPageToken"]
    )
    response = request.execute()

print(videos_by_languages)

with open(config[app_name]['list_path'], "w", encoding='UTF-8') as file:
    json.dump(videos_by_languages, file)

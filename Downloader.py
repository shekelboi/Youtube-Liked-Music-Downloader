# Reference https://googleapis.github.io/google-api-python-client/docs/dyn/youtube_v3.html

import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

credentials = None
pickle_token_file = "token.pickle"

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
        flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", scopes=["https://www.googleapis.com/auth/youtube.readonly"])
        flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
        credentials = flow.credentials

        with open(pickle_token_file, "wb") as token:
            print("Saving the credentials in a pickle file")
            pickle.dump(credentials, token)
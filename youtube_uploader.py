from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
from .config import settings

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def _get_creds() -> Credentials:
    creds = None
    if os.path.exists(settings.youtube_token_path):
        creds = Credentials.from_authorized_user_file(settings.youtube_token_path, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(settings.youtube_client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(settings.youtube_token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
    return creds


def upload_short(file_path: str, title: str, description: str) -> dict:
    creds = _get_creds()
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "categoryId": settings.youtube_category_id,
            "tags": ["shorts", "satisfying", "simulation", "vfx"],
        },
        "status": {
            "privacyStatus": settings.youtube_privacy_status,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        _, response = request.next_chunk()
    return response

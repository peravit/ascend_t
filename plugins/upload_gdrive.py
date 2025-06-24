from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import os

GDRIVE_FOLDER_ID = "1wi8QDJt4EKXLwDuqmaECcHsSqWzBYi3_"

def upload_to_gdrive(filepath):
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("/opt/airflow/gdrive/credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("/opt/airflow/gdrive/credentials.json")
    drive = GoogleDrive(gauth)
    file = drive.CreateFile({'parents': [{'id': GDRIVE_FOLDER_ID}], 'title': os.path.basename(filepath)})
    file.SetContentFile(filepath)
    file.Upload()
    print(f" Uploaded {os.path.basename(filepath)}")

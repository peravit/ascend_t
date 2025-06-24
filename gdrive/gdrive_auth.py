import os
from pydrive2.auth import GoogleAuth

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET_PATH = os.path.join(BASE_DIR, 'client_secrets.json')

gauth = GoogleAuth()
GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = CLIENT_SECRET_PATH

gauth.LocalWebserverAuth(params={"access_type": "offline", "prompt": "consent"})

gauth.SaveCredentialsFile(os.path.join(BASE_DIR, "credentials.json"))

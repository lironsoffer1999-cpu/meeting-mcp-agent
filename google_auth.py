import os
import logging
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

# If modifying these SCOPES, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar'
]

def get_google_service(service_name: str, version: str):
    """
    Authenticates the user and returns the requested Google API service.
    Handles token creation, refresh, and storage.
    """
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'

    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing expired Google API token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(credentials_path):
                logger.error(f"Error: {credentials_path} not found. Please follow the instructions in README.md.")
                raise FileNotFoundError(f"{credentials_path} is missing.")
            
            logger.info("Starting new Google API authentication flow...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the credentials for the next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build(service_name, version, credentials=creds)

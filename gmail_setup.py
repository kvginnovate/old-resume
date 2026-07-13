"""
Gmail API Setup Script
- Downloads OAuth credentials from Google Cloud Console
- Creates token.json for authentication
"""

import os
import json
from pathlib import Path

# Check if google-api-python-client is installed
try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    print("[OK] Google API libraries installed")
except ImportError:
    print("[!] Missing libraries. Install them with:")
    print("    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    exit(1)

# If modifying these scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.json'

def authenticate():
    """Authenticate with Gmail API via OAuth2"""
    creds = None
    
    # Check for existing token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
        print("[OK] Loaded existing token")
    
    # If no valid credentials, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("[...] Refreshing expired token...")
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                print(f"[!] {CREDENTIALS_FILE} not found!")
                print()
                print("To get credentials.json:")
                print("1. Go to https://console.cloud.google.com/")
                print("2. Create a project (or select existing)")
                print("3. Enable Gmail API: APIs & Services > Library > search 'Gmail API' > Enable")
                print("4. Create credentials: APIs & Services > Credentials > Create Credentials > OAuth client ID")
                print("5. Application type: Desktop app")
                print("6. Download the JSON and save as 'credentials.json' in this folder")
                exit(1)
            
            print("[...] Starting OAuth flow (browser will open)...")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save token for next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())
        print("[OK] Token saved")
    
    return creds

def test_connection(creds):
    """Test Gmail API connection"""
    service = build('gmail', 'v1', credentials=creds)
    
    # Get profile info
    profile = service.users().getProfile(userId='me').execute()
    print()
    print("=" * 60)
    print("GMAIL CONNECTION SUCCESSFUL")
    print("=" * 60)
    print(f"  Email: {profile['emailAddress']}")
    print(f"  Messages Total: {profile['messagesTotal']}")
    print(f"  Threads Total: {profile['threadsTotal']}")
    print(f"  History ID: {profile['historyId']}")
    print("=" * 60)
    
    return service, profile

if __name__ == '__main__':
    print("--- Gmail API Setup ---")
    creds = authenticate()
    service, profile = test_connection(creds)
    print()
    print("Setup complete! Run 'python fetch_emails.py' to fetch your emails.")

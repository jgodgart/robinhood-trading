import os
import io
import json
import sys
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

FILE_ID = '1OFEsZJAh97t_AqLOP1zRRPrX2SbyrCDj'

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPTS_DIR, ".."))
STATE_FILE = os.path.join(BASE_DIR, "claude", "robinhood-live-state.json")

def download_file():
    print("📥 Initializing Google Drive downloader...")
    
    import google.auth
    
    try:
        creds, project = google.auth.default(scopes=['https://www.googleapis.com/auth/drive.readonly'])
    except Exception as e:
        print(f"❌ Error getting Google Cloud credentials: {e}")
        sys.exit(1)

    try:
        service = build('drive', 'v3', credentials=creds)
        
        # Ensure the destination directory exists
        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
        
        request = service.files().get_media(fileId=FILE_ID)
        fh = io.FileIO(STATE_FILE, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            if status:
                print(f"Downloading... {int(status.progress() * 100)}%")
                
        print(f"✅ Successfully downloaded snapshot to {STATE_FILE}")
        
    except Exception as e:
        print(f"❌ Error downloading file from Google Drive: {e}")
        sys.exit(1)

if __name__ == '__main__':
    download_file()

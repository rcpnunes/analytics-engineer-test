import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

# --- Constants ---
# Google Drive folder ID (extracted from the URL you provided)
DRIVE_FOLDER_ID = "1jsbUFMKBKrkBJ8lZhQgFKcX5KyDKAXrB"

# Robust paths for files
SRC_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SRC_DIR)
DATA_DIR = os.path.join(PROJECT_ROOT, 'data')
CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, 'credentials.json')

# List of files to upload
FILES_TO_UPLOAD = [
    "coffee_sales_historical.csv",
    "currency_rates_historical.csv"
]

def authenticate():
    """Handles Google Drive authentication."""
    gauth = GoogleAuth()
    # Try to load saved credentials
    gauth.LoadCredentialsFile(CREDENTIALS_FILE)
    if gauth.credentials is None:
        # Authenticate via browser if no credentials are found
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh credentials if expired
        gauth.Refresh()
    else:
        # Initialize credentials if already authorized
        gauth.Authorize()
    
    # Save credentials for future runs
    gauth.SaveCredentialsFile(CREDENTIALS_FILE)
    
    return GoogleDrive(gauth)

def upload_files_to_drive():
    """
    Finds the result CSVs and uploads them to the specified Google Drive folder.
    """
    print("--- Starting Google Drive Upload Process ---")
    drive = authenticate()

    for filename in FILES_TO_UPLOAD:
        file_path = os.path.join(DATA_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"Warning: File '{filename}' not found in /data. Skipping.")
            continue

        try:
            print(f"Uploading '{filename}' to Google Drive...")
            
            # Set file metadata (title and parent folder)
            file_metadata = {
                'title': filename,
                'parents': [{'id': DRIVE_FOLDER_ID}]
            }
            
            gfile = drive.CreateFile(file_metadata)
            # Set file content
            gfile.SetContentFile(file_path)
            # Perform upload
            gfile.Upload()
            
            print(f"Success! '{filename}' uploaded.")

        except Exception as e:
            print(f"Error uploading '{filename}': {e}")
            
    print("\n--- Google Drive Upload Process Finished ---")

if __name__ == "__main__":
    upload_files_to_drive()
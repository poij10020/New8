import pandas as pd
import requests
from time import sleep
import re
import os

def extract_file_id_from_url(url):
    match = re.search(r'/d/([^/]+)', url)
    return match.group(1) if match else None

access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
page_id = os.getenv('FACEBOOK_PAGE_ID')

def upload_video_to_facebook(file_id, description):
    file_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    video_file_path = '/tmp/video.mp4'
    response = requests.get(file_url)
    with open(video_file_path, 'wb') as file:
        file.write(response.content)
    upload_url = f'https://graph.facebook.com/v20.0/{page_id}/videos'
    with open(video_file_path, 'rb') as video_file:
        upload_response = requests.post(upload_url, files={'file': video_file}, data={
            'access_token': access_token,
            'description': description
        })
    if upload_response.status_code == 200:
        print(f'Video uploaded successfully from file ID: {file_id}')
    else:
        print(f'Error uploading video from file ID {file_id}: {upload_response.text}')

def process_csv_and_upload(csv_file_path):
    df = pd.read_csv(csv_file_path)
    for _, row in df.iterrows():
        file_id = row['file_id']
        description = row['description'] if 'description' in row else 'Default description'
        if pd.notna(file_id):
            upload_video_to_facebook(file_id, description)
            sleep(120)  # Wait for 2 minutes before uploading the next video

if __name__ == '__main__':
    csv_file_path = 'videos.csv'
    process_csv_and_upload(csv_file_path)

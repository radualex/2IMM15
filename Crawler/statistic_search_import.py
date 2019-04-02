#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python geolocation_search.py --q=surfing --location-"37.42307,-122.08427" --location-radius=50km --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

from googleapiclient.discovery import build
from config import configYoutube

# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = None
YOUTUBE_API_SERVICE_NAME = None
YOUTUBE_API_VERSION = None


def youtube_search_ids(ids):

    params = configYoutube()

    DEVELOPER_KEY = params['developerKey']
    YOUTUBE_API_SERVICE_NAME = params['youtube_api_service_name']
    YOUTUBE_API_VERSION = params['youtube_api_version']

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    video_ids = ','.join(ids)

    video_response = youtube.videos().list(
        id=video_ids,
        part='id, statistics'
    ).execute()

    id = []
    viewCount = []
    likeCount = []
    dislikeCount = []
    favoriteCount = []

    for video_result in video_response.get('items', []):
        id.append(video_result['id'])
        viewCount.append(video_result['statistics']['viewCount'])
        likeCount.append(video_result['statistics']['likeCount'])
        dislikeCount.append(video_result['statistics']['dislikeCount'])
        favoriteCount.append(video_result['statistics']['favoriteCount'])

    dictionary = {'id': id,
                  'viewCount': viewCount,
                  'likeCount': likeCount,
                  'dislikeCount': dislikeCount}

    return dictionary

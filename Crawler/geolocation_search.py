#!/usr/bin/python

# This sample executes a search request for the specified search term.
# Sample usage:
#   python geolocation_search.py --q=surfing --location-"37.42307,-122.08427" --location-radius=50km --max-results=10
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console. Search for "REPLACE_ME" in this code
#       to find the correct place to provide that key..

import argparse

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = 'AIzaSyCNQN3P1pGEMMJYcqBptyjNtMoTXZK0hOk'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def youtube_search(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=options.q,
        type='video',
        location=options.location,
        locationRadius=options.location_radius,
        part='id',
        maxResults=options.max_results
    ).execute()

    search_videos = []

    # Merge video ids
    for search_result in search_response.get('items', []):
        if search_result["id"]["kind"] == "youtube#video":
            search_videos.append(search_result['id']['videoId'])
    video_ids = ','.join(search_videos)

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
        id=video_ids,
        part='snippet, status, statistics'
    ).execute()

    videos = []

    # Add each result to the list, and then display the list of matching videos.
    for video_result in video_response.get('items', []):
        if video_result["status"]["uploadStatus"] == "processed":
            videos.append('%s, (%s)' % (video_result['snippet']['title'],
                                        video_result['id']))

    print('Videos:\n', '\n'.join(videos), '\n')
    print('Count:', len(videos))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term', default='Google')
    parser.add_argument('--location', help='Location',
                        default='38.61048,-121.44730')
    parser.add_argument('--location-radius',
                        help='Location radius', default='1000km')
    parser.add_argument('--max-results', help='Max results', default=50)
    args = parser.parse_args()

    try:
        youtube_search(args)
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

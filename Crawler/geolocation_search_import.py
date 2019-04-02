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


def youtube_search(q="computer science tutorial", max_results=50,
                   order="relevance", token=None,
                   location="38.61048,-121.44730", location_radius="1000km"):

    params = configYoutube()

    DEVELOPER_KEY = params['developerkey']
    YOUTUBE_API_SERVICE_NAME = params["youtube_api_service_name"]
    YOUTUBE_API_VERSION = params["youtube_api_version"]

    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    # Call the search.list method to retrieve results matching the specified
    # query term.
    search_response = youtube.search().list(
        q=q,
        type='video',
        location=location,
        locationRadius=location_radius,
        part='id',
        maxResults=max_results,
        pageToken=token,
        order=order
    ).execute()

    # print(search_response['nextPageToken'])

    dictionary = dict()

    id = []
    title = []
    description = []
    publishedAt = []
    duration = []
    channelId = []
    channelTitle = []
    thumbnailUrl = []
    thumbnailWidth = []
    thumbnailHeight = []
    statisticsViewCount = []
    statisticsLikeCount = []
    statisticsDislikeCount = []
    tags = []

    for search_result in search_response.get('items', []):
        if search_result["id"]["kind"] == "youtube#video":

            id.append(search_result['id']['videoId'])

            video_response = youtube.videos().list(
                id=search_result['id']['videoId'],
                part='snippet, status, statistics, contentDetails'
            ).execute()

            responseItem = video_response['items'][0]
            if responseItem["status"]["uploadStatus"] == "processed":

                # print(responseItem['statistics'])
                title.append(responseItem['snippet']['title'])
                channelId.append(responseItem['snippet']['channelId'])
                channelTitle.append(responseItem['snippet']['channelTitle'])
                description.append(responseItem['snippet']['description'])
                publishedAt.append(responseItem['snippet']['publishedAt'])
                duration.append(responseItem['contentDetails']['duration'])
                if 'viewCount' in responseItem['statistics'].keys():
                    statisticsViewCount.append(
                        responseItem['statistics']['viewCount'])
                if 'likeCount' in responseItem['statistics'].keys():
                    statisticsLikeCount.append(
                        responseItem['statistics']['likeCount'])
                if 'dislikeCount' in responseItem['statistics'].keys():
                    statisticsDislikeCount.append(
                        responseItem['statistics']['dislikeCount'])
                thumbnailUrl.append(
                    responseItem['snippet']['thumbnails']['default']['url'])
                thumbnailWidth.append(
                    responseItem['snippet']['thumbnails']['default']['width'])
                thumbnailHeight.append(
                    responseItem['snippet']['thumbnails']['default']['height'])

                if 'tags' in responseItem['snippet'].keys():
                    tags.append(responseItem['snippet']['tags'])
                else:
                    tags.append([])

    dictionary = {'id': id, 'title': title,
                  'description': description,
                  'publishedAt': publishedAt,
                  'duration': duration,
                  'channelId': channelId,
                  'channelTitle': channelTitle,
                  'viewCount': statisticsViewCount,
                  'likeCount': statisticsLikeCount,
                  'dislikeCount': statisticsDislikeCount,
                  'thumbnail-url': thumbnailUrl,
                  'thumbnail-width': thumbnailWidth,
                  'thumbnail-height': thumbnailHeight,
                  'tags': tags}
    if 'nextPageToken' in search_response:
        dictionary['nextPageToken'] = search_response['nextPageToken']


    print("EXTRA:")
    search_videos = []

    # Merge video ids
    for search_result in search_response.get('items', []):
        search_videos.append(search_result['id']['videoId'])
    video_ids = ','.join(search_videos)

    # Call the videos.list method to retrieve location details for each video.
    video_response = youtube.videos().list(
        id=video_ids,
        part='snippet, recordingDetails, statistics'
    ).execute()

    videos = []

    # Add each result to the list, and then display the list of matching videos.
    for video_result in video_response.get('items', []):
        videos.append('%s, %s %s, %s' % (video_result['snippet']['title'],
                                        video_result['statistics']['viewCount'],
                                         video_result['statistics']['likeCount'],
                                             video_result['statistics']['dislikeCount']))

    print('\n'.join(videos))

    return dictionary

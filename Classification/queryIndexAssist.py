import argparse
from database import get_data_for_query_processing, get_video_complete

#get the words searched for
#match with indexed database
#order from least occuring to most occuring words
#save the found videos, and during how many searches it was found
#order by most times found
#take most found video and add 2 to the other videos that share author
#return top 5
queryDict = dict()
queriedIDs = dict()
videos = {}
#get words from query

#give words their occurrence
for key in queryDict:
    if key in dictionary.keys():
        queryDict[key] = dictionary[key]

dict = get_data_for_query_processing()

keyFreq = 0 #how frequent the current key is
for key in sorted (queryDict):
    keyFreq =+
    for vidID in dict[key]
        queriedIDs[vidID] =+ keyFreq

sorted(queriedIDs, reverse = True)

for video in queriedIDs
    videos[video] = queriedIDs[video], get_video_complete(video)

for x in videos
    if videos[x][6] = videos[0][6]
        videos[x][0]=+2

sorted(videos, reverse = True)
iter = 0
answers = {}
for x in videos
    answers[x] = videos[x]
    answers[x].pop(0)
    iter =+ 1
    if iter = 5
        break
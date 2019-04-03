import argparse
from database import get_data_for_query_processing, get_video_complete
from basewords import get_weighted_words
#get the words searched for
#match with indexed database
#order from least occuring to most occuring words
#save the found videos, and during how many searches it was found
#order by most times found
#take most found video and add 2 to the other videos that share author
#return top 5
queryDict = {}
queriedIDs = {}
videos = {}
weighed_words = get_weighted_words()
#get words from query

#give words their occurrence
for key in queryDict:
    if key in weighed_words.keys():
        queryDict[key] = weighed_words[key]

dict = get_data_for_query_processing()

keyFreq = 0 #how frequent the current key is
for key in sorted (queryDict):
    keyFreq =+ 1
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
return answers

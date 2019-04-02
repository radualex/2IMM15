import argparse

from database import get_data_for_query_processing, get_videos, get_videos_complete, get_statistics
from query_processing import split_query_into_words_and_operators, create_incidence_matrices, process_matrices, extract_video_names_from_final_matrix, jsonify
from datetime import datetime


def main(query):
    if(query is None):
        return "Query is empty"

    videoIds = []
    for videoId in get_videos():
        vId = videoId[0]
        videoIds.append(vId)

    dict = get_data_for_query_processing()
    tokens_and_operators = split_query_into_words_and_operators(query)
    tokens = tokens_and_operators['tokens']
    operators = tokens_and_operators['operators']
    matrices = create_incidence_matrices(dict, tokens, videoIds)

    final_matrix = process_matrices(matrices, operators)
    print(final_matrix)
    videosComplete = get_videos_complete()

    videos = extract_video_names_from_final_matrix(final_matrix, videosComplete)

    return jsonify(videos)


def statistics_by_id(id):
    if(id is None):
        return "Id is empty"

    statistics = get_statistics(id)

    json = "{\"statistics\":["
    for statistic in statistics:
        json += "{"
        json += "\"viewCount\":\"" + str(statistic[0]) + "\","
        json += "\"likeCount\":\"" + str(statistic[1]) + "\","
        json += "\"dislikeCount\":\"" + str(statistic[2]) + "\","
        json += "\"inserted_at\":\"" + statistic[3].strftime('%Y-%m-%dT%H:%M:%S.%f%z') + "\""
        json += "},"

    json = json[:-1]
    json += "]}"

    return json

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--query', help='query', default=None)
    args = parser.parse_args()

    print(main(args))

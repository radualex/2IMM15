import argparse

from database import get_data_for_query_processing, get_videos, get_videos_complete
from query_processing import split_query_into_words_and_operators, create_incidence_matrices, process_matrices, extract_video_names_from_final_matrix, jsonify


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

    videos = extract_video_names_from_final_matrix(final_matrix, videoIds)
    return jsonify(videos)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--q', help='query', default=None)
    args = parser.parse_args()

    print(main(args.q))

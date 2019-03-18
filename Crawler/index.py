import argparse

from database import get_data_for_indexing, get_videos
from text_processing import process_text

# from text_processing import split_into_senteces, tokenize_filter_punctuation, remove_nonalpha_and_stop_words, normalize, stemming


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--download', help='Download nltk required packages', action='store_true')
    args = parser.parse_args()

    if(args.download):
        download_stop_words()
    # print(get_data_for_indexing("lacpTQuE9u8"))
    for videoId in get_videos():
        data = get_data_for_indexing(videoId[0])
        title = process_text(data["title"])
        description = process_text(data["description"])
        tags = process_text(data["tags"])
        final_set = set()
        final_set.update(title)
        final_set.update(description)
        final_set.update(tags)

        print(final_set)

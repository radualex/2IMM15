import argparse

from database import get_data_for_indexing, get_videos, populate_indexing_tables
from text_processing import process_text, download_stop_words
from index_processing import add_tuples_to_dictionary
# from text_processing import split_into_senteces, tokenize_filter_punctuation, remove_nonalpha_and_stop_words, normalize, stemming


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--download', help='Download nltk required packages', action='store_true')
    args = parser.parse_args()

    if(args.download):
        download_stop_words()

    dictionary = dict()

# for all videos get the title, description and tags.
# then tokenize, normalize, remove stopword, non-alpha, and stem the words. return word_tokens
# create a set of these tokens (avoid duplicates) and create the hashmap (key: word, value: array of videoIds)
# finally, add the data from dictionary to DatabaseError

    for videoId in get_videos():
        vId = videoId[0]
        data = get_data_for_indexing(vId)
        title = process_text(data["title"])
        description = process_text(data["description"])
        tags = process_text(data["tags"])
        final_set = set()
        final_set.update(title)
        final_set.update(description)
        final_set.update(tags)

        add_tuples_to_dictionary(final_set, vId, dictionary)

    populate_indexing_tables(dictionary)

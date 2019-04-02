import argparse

from geolocation_search_import import youtube_search
from statistic_search_import import youtube_search_ids
from googleapiclient.errors import HttpError
from database import insert_video_table_data, insert_thumbnail_table_data, insert_statistics_table_data, insert_tag_table_data, get_count_video_table, truncate_all_tables, truncate_indexer_tables, select_video_ids


def call_youtube_ids(ids):
    dict = youtube_search_ids(ids)

    return dict


def load_statistics():
    ids = select_video_ids()
    dict = call_youtube_ids(ids)

    insert_statistics_table_data(dict)


if __name__ == '__main__':
    try:
        load_statistics()
        print("Completed updating statistics")

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

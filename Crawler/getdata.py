import argparse

from geolocation_search_import import youtube_search
from googleapiclient.errors import HttpError
from database import insert_video_table_data, insert_thumbnail_table_data, insert_statistics_table_data, insert_tag_table_data, get_count_video_table, truncate_all_tables, truncate_indexer_tables


def call_youtube(args):
    dict = youtube_search(args.q, args.max_results,
                          args.order, args.token,
                          args.location, args.location_radius)

    return dict


def insert_all_data(args):
    dict = call_youtube(args)
    insert_video_table_data(dict)
    insert_statistics_table_data(dict)
    insert_thumbnail_table_data(dict)
    insert_tag_table_data(dict)

    return dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term',
                        default='computer science tutorial')
    parser.add_argument('--location', help='Location',
                        default='38.61048,-121.44730')  # arond Sacramento
    parser.add_argument('--location-radius',
                        help='Location radius', default='1000km')
    parser.add_argument('--max-results', help='Max results', default=50)
    parser.add_argument('--order', help='Order', default='relevance')
    parser.add_argument('--token', help='Page token', default=None)
    parser.add_argument(
        '--d', help='Truncate all tables', action='store_true')
    parser.add_argument(
        '--dindexer', help='Truncate all tables related to indexer',
        action='store_true')
    args = parser.parse_args()

    try:
        if(args.d):
            truncate_all_tables()
        elif(args.dindexer):
            truncate_indexer_tables()
        else:
            dict = insert_all_data(args)

            while 'nextPageToken' in dict and get_count_video_table() < 200:
                args.token = dict["nextPageToken"]
                dict = insert_all_data(args)

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

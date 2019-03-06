import argparse

from geolocation_search_import import youtube_search
from googleapiclient.errors import HttpError


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
    args = parser.parse_args()

    try:
        dict = youtube_search(args.q, args.max_results, args.order,
                              args.token, args.location, args.location_radius)

        print('Videos:\n', '\n'.join(dict['id']), '\n')

        # if 'nextPageToken' in dict:
        #     dict = youtube_search(token=dict['nextPageToken'])
        #     print('Videos:\n', '\n'.join(dict['videos']), '\n')

        # modify the script to get the data according to our schema and return in dict
        # add to database here. add a while for nextPageToken
    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

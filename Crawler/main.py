import argparse
from getdata import main as crawl
from index import main as indexing
from query import main as querying


# pass q = search term for youtube, location = x,y lang, lat coords, location-radius= Xkm, max-results=[1,50] for crawling
# pass i, download = (first time to get the nltk packages) for Indexing
# pass query= a query with boolean operators for querying
def main(args):
    if(args.q or args.d or args.dindexer):
        crawl(args)
    if(args.i):
        indexing(args)
    if(args.query):
        print(querying(args.query))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--q', help='Search term',
                        default=None)
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

    parser.add_argument(
        '--i', help='Index', action='store_true')
    parser.add_argument(
        '--download', help='Download nltk required packages', action='store_true')

    parser.add_argument(
        '--query', help='query', default=None)
    args = parser.parse_args()

    main(args)

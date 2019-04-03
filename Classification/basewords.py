import psycopg2
from config import config
from database import populate_indexing_tables, get_data_for_baseword_weighing
from index import index

def get_weighted_words():
    #import the basewordLib.txt dictionary
    filename = 'basewordLib.txt'
    basewords = {}
    with open(filename) as fh:
        for line in fh:
            baseword, frequency = line.strip().split(' ', 1)
            basewords[baseword] = frequency

    dictionary = get_data_for_baseword_weighing()
    #multiply the indexed frequencies by the weights form the file
    for key in dictionary
        if key in basewords.keys():#may want to make this a contains
            dictionary[key] = dictionary[key]*basewords[key]

    return dictionary

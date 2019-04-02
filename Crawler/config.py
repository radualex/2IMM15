from configparser import ConfigParser
import os


def config(filename='\\config.ini', section='postgresql'):

    db = {}
    db['host'] = '127.0.0.1'
    db['database'] = 'youtube'
    db['user'] = 'postgres'
    db['password'] = 'postgres'

    return db

    # create a parser
    parser = ConfigParser()
    # read config file

    parser.read(os.path.dirname(__file__)+filename)

    print(parser.items())

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db


def configYoutube(filename='\\config.ini', section='ytube'):

    youtube = {}
    youtube['developerKey'] = 'AIzaSyD5lOC4iMR5QweNOd5uEMALQt47EMemv8Q'
    youtube['youtube_api_service_name'] = 'youtube'
    youtube['youtube_api_version'] = 'v3'

    return youtube

    # create a parser
    #parser = ConfigParser()
    # read config file
    #parser.read(os.path.dirname(__file__)+filename)

    # get section, default to postgresql
    #youtube = {}
    #if parser.has_section(section):
#        params = parser.items(section)
#        for param in params:
#            youtube[param[0]] = param[1]
#    else:
#        raise Exception(
            #'Section {0} not found in the {1} file'.format(section, filename))

    #return youtube

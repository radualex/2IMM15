from configparser import ConfigParser
import os

def config(filename='\\config.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(os.path.dirname(__file__)+filename)

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
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(os.path.dirname(__file__)+filename)

    # get section, default to postgresql
    youtube = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            youtube[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return youtube

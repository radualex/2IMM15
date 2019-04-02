import psycopg2
from config import config


def connect():
    try:
        conn = None
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def truncate_indexer_tables():
    try:
        conn = connect()
        cur = conn.cursor()
        query = """DELETE FROM word;"""

        cur.execute(query)
        conn.commit()
        count = cur.rowcount

        print(count, "Record deleted successfully (word).")

        query = """DELETE FROM posting;"""

        cur.execute(query)
        conn.commit()
        count = cur.rowcount

        print(count, "Record deleted successfully (posting).")

        cur.close()
        disconnect(conn)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def truncate_all_tables():
    try:
        conn = connect()
        cur = conn.cursor()
        query = """DELETE FROM tag;"""

        cur.execute(query)
        conn.commit()
        count = cur.rowcount

        print(count, "Record deleted successfully (tag).")

        query = """DELETE FROM statistics;"""

        cur.execute(query)
        conn.commit()
        count = cur.rowcount

        print(count, "Record deleted successfully (statistics).")

        query = """DELETE FROM thumbnail;"""

        cur.execute(query)
        conn.commit()
        count = cur.rowcount

        print(count, "Record deleted successfully (thumbnail).")

        query = """DELETE FROM video;"""

        cur.execute(query)
        conn.commit()
        count = cur.rowcount

        truncate_indexer_tables()
        
        cur.close()
        disconnect(conn)

        print(count, "Record deleted successfully (video).")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_video_table_data(dict):
    try:
        conn = connect()
        cur = conn.cursor()

        i = 0
        while i < len(dict["id"]):
            if get_video_item_from_table(dict["id"][i]) is None:
                row = [dict["id"][i], dict["title"][i], dict["description"][i],
                       dict["publishedAt"][i], dict["duration"][i],
                       dict["channelId"][i], dict["channelTitle"][i]]

                query = """INSERT INTO video(id,title,description,publishedAt,duration,channelId,channelTitle) VALUES (%s,%s,%s,%s,%s,%s,%s)"""

                cur.execute(query, row)
                conn.commit()
                count = cur.rowcount
                print(count, "Record inserted successfully into video table")
            i += 1

        cur.close()
        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_statistics_table_data(dict):
    try:
        conn = connect()
        cur = conn.cursor()

        i = 0
        while(i < len(dict["id"])):
            if get_video_item_from_table(dict["id"][i]) is not None:
                row = [dict["viewCount"][i], dict["likeCount"]
                       [i], dict["dislikeCount"][i], dict["id"][i]]

                query = """INSERT INTO statistics(viewcount,likecount,dislikecount
                ,videoid) VALUES (%s,%s,%s,%s)"""

                cur.execute(query, row)
                conn.commit()
                count = cur.rowcount
                print(count, "Record inserted successfully into statistics table")
            i += 1

        cur.close()
        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_thumbnail_table_data(dict):
    try:
        conn = connect()
        cur = conn.cursor()

        i = 0
        while(i < len(dict["id"])):
            if get_video_item_from_table(dict["id"][i]) is not None:
                row = [dict["thumbnail-url"][i], dict["thumbnail-width"]
                       [i], dict["thumbnail-height"][i], dict["id"][i]]

                query = """INSERT INTO thumbnail(url,width,height
                ,videoid) VALUES (%s,%s,%s,%s)"""

                cur.execute(query, row)
                conn.commit()
                count = cur.rowcount
                print(count, "Record inserted successfully into thumbnail table")
            i += 1

        cur.close()
        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def insert_tag_table_data(dict):
    try:
        conn = connect()
        cur = conn.cursor()

        i = 0
        while(i < len(dict["id"])):
            if get_video_item_from_table(dict["id"][i]) is not None:
                for tag in dict["tags"][i]:
                    row = [tag, dict["id"][i]]

                    query = """INSERT INTO tag(value,videoid) VALUES (%s,%s)"""

                    cur.execute(query, row)
                    conn.commit()
                    count = cur.rowcount
                    print(count, "Record inserted successfully into tag table")
            i += 1

        cur.close()
        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_video_item_from_table(id):
    try:
        conn = connect()
        cur = conn.cursor()

        query = """SELECT id FROM video WHERE id = %s"""

        cur.execute(query, (id, ))
        record = cur.fetchone()

        cur.close()
        disconnect(conn)

        return record[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_count_video_table():
    try:
        conn = connect()
        cur = conn.cursor()

        query = """SELECT COUNT(*) FROM video"""

        cur.execute(query)
        record = cur.fetchone()

        cur.close()
        disconnect(conn)

        return record[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


# Indexing
def get_videos():
    try:
        conn = connect()
        cur = conn.cursor()

        query = """SELECT id FROM video"""

        cur.execute(query)
        records = cur.fetchall()

        cur.close()
        disconnect(conn)

        return records
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_videos_complete():
    try:
        conn = connect()
        cur = conn.cursor()

        query = """SELECT * FROM video"""

        cur.execute(query)
        records = cur.fetchall()

        cur.close()
        disconnect(conn)

        return records
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_data_for_indexing(videoId):
    try:
        tags = set()
        conn = connect()
        cur = conn.cursor()

        query = """SELECT title,description FROM video WHERE id = %s"""
        cur.execute(query, (videoId, ))
        record = cur.fetchone()

        query = """SELECT value FROM tag WHERE videoid=%s"""
        cur.execute(query, (videoId, ))
        records_tags = cur.fetchall()

        for r in records_tags:
            tags.update(r)

        records_tags = ', '.join(tags) + '.'

        dictionary = {
            'title': record[0], 'description': record[1], 'tags': records_tags}

        cur.close()
        disconnect(conn)

        return dictionary
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def populate_indexing_tables(dictionary):
    try:
        conn = connect()
        cur = conn.cursor()

        for key in dictionary:
            freq = len(dictionary[key])

            query = """INSERT INTO word(word,frequency) VALUES (%s,%s) RETURNING wordid"""
            cur.execute(query, (key, freq))
            conn.commit()
            lastId = cur.fetchone()[0]
            print("Record inserted successfully into word table")

            for item in dictionary[key]:
                query = """INSERT INTO posting(wordid,videoid) VALUES (%s,%s)"""
                cur.execute(query, (lastId, item))
                conn.commit()
                count = cur.rowcount
                print(count, "Record inserted successfully into posting table")

        cur.close()
        disconnect(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_data_for_query_processing():
    try:
        dict = {}
        conn = connect()
        cur = conn.cursor()

        query = """SELECT * FROM word;"""
        cur.execute(query)
        conn.commit()
        words = cur.fetchall()

        for word in words:
            id = word[0]
            actual_word = word[1]
            query = """SELECT videoId FROM posting WHERE wordId = %s"""
            cur.execute(query, (id, ))
            videoIds = cur.fetchall()
            dict[actual_word] = []
            for videoId in videoIds:
                dict[actual_word].append(videoId[0])

        cur.close()
        disconnect(conn)

        return dict
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def disconnect(conn):
    try:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def select_video_ids():
    try:
        conn = connect()
        cur = conn.cursor()

        query = """SELECT id FROM video"""

        cur.execute(query, (id, ))
        records = cur.fetchall()

        ids = []
        for record in records:
            ids.append(record[0])

        cur.close()
        disconnect(conn)

        return ids
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

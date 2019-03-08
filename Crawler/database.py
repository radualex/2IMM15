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
                    print(count, "Record inserted successfully into thumbnail tag")
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


def disconnect(conn):
    try:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

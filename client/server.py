from flask import Flask, render_template, redirect, url_for
import pymysql
import requests as req
import json

app = Flask(__name__)


class Entry:
    def __init__(self, title, description, views, likes, dislikes, date, id, published, channelTitle, channelId, url, width, height):
        self.title = title
        self.description = description
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.date = date
        self.id = id
        self.published = published
        self.channelTitle = channelTitle
        self.channelId = channelId
        self.url = url
        self.width = width
        self.height = height


def query_entries(query, entries):
    result = []

    for entry in entries:
        if query in entry.title or query in entry.description:
            result.append(entry)

    return result


def parse_videos(videos):
    videosjson = json.loads(videos)
    result = []

    if 'videos' in videosjson:
        for video in videosjson['videos']:
            entry = Entry(str(video['title']), str(video['description']), str(video['viewCount']), str(video['likeCount']),
                          str(video['dislikeCount']), str(video['publishedAt']), str(video['id']),
                          str(video['publishedAt']), str(video['channelTitle']), str(video['channelId']),
                          str(video['url']), str(video['width']), str(video['height']))
            result.append(entry)

    return result


def load_data(query):
    url = 'http://localhost:3000/query/' + query
    resp = req.get(url)

    return resp.text


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "user"
        password = "password"
        db = "employees"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()


@app.route('/')
def fakeindex():
    return redirect(url_for('index'))


@app.route('/query/')
def index():
    entries = []

    return render_template('base.html', entries=entries, content_type='application/json')


@app.route('/query/<query>')
def query(query):
    videos = load_data(query)

    video_entries = parse_videos(videos)

    entries = video_entries[:10]

    return render_template('base.html', entries=entries, query=query, content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template
import pymysql

app = Flask(__name__)


class Entry:
    def __init__(self, title, description, views, likes, dislikes, date):
        self.title = title
        self.description = description
        self.views = views
        self.likes = likes
        self.dislikes = dislikes
        self.date = date


def generate_entries(amount):
    amount += 1
    entries = []
    for i in range(1, amount):
        entry = Entry(10 * "Title " + str(i), "Entry description " + str(i), i * 100000, i * 100, i * 10, "1/" + str(i) + "/2019")
        entries.append(entry)

    return entries


def query_entries(query, entries):
    result = []

    for entry in entries:
        if query in entry.title or query in entry.description:
            result.append(entry)

    return result


class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "user"
        password = "password"
        db = "employees"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()

    def list_employees(self, limit=50):
        self.cur.execute("SELECT first_name, last_name, gender FROM employees LIMIT " + str(limit))
        result = self.cur.fetchall()
        return result


@app.route('/')
def index():
    entries = generate_entries(10)

    return render_template('base.html', entries=entries, content_type='application/json')


@app.route('/<query>')
def query(query):
    entries = generate_entries(100)
    entries = query_entries(query, entries)

    return render_template('base.html', entries=entries, query=query, content_type='application/json')


@app.route('/test/<limit>')
def employees(limit):
    db = Database()
    res = db.list_employees(limit)
    return render_template('employees.html', result=res, content_type='application/json')


if __name__ == '__main__':
    app.run(debug=True)

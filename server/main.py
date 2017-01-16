from flask import Flask, request, session, g, jsonify
from functools import wraps
import json
import os, sys
import uuid
import sqlite3

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'pipgame.db'),
    SECRET_KEY='peppered beef',
    USERNAME='admin',
    PASSWORD='default'
))

def db_serialize(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        cur = fn(*args, **kwargs)
        jsonable = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        return jsonify({"result":jsonable})
    return wrapper

def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('initdb')
def initdb_command():
    init_db()
    print("Initialized the DB")

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
@db_serialize
def home():
    db = get_db()
    cur = db.execute('select name, score from players order by score desc limit 10')
    return cur

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        db = get_db()
        cur = db.execute('select 1 from players where name = ? and password = ?', (data['name'], data['password']))
        if cur.fetchone() is None:
            return jsonify({"error":"Invalid Login"}), 401
        token = str(uuid.uuid4())
        session['username'] = data['name']
        session['token'] = token
        return jsonify({"result":{"token":token}})
    except KeyError as e:
        return jsonify({"error":"You did not include all required fields"}), 400
    except Exception as e:
        return jsonify({"error":str(e)}), 500

@app.route('/player', methods=['POST'])
def addPlayer():
    try:
        data = request.get_json()
        db = get_db()
        try:
            cur = db.execute('insert into players (name, password, score, options) values (?, ?, ?, ?)',
                        [
                             data['name'],
                             data['password'],
                             data.get('score', 0),
                             json.dumps(data.get('options', {}))
                        ])
            db.commit()
        except KeyError as e:
            return jsonify({"error":"You did not include all required fields"}), 400
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    return jsonify({"result":"success"})


@app.route('/player', methods=['PUT'])
def updatePlayer():
    try:
        data = request.get_json()
        print("Token: {}, Data: {}".format(session['token'], data['token']), file=sys.stderr)
        if session['token'] == data.get('token', ""):
            db = get_db()

            tmp = {}
            for key in ["password", "score", "options"]:
                if key in data:
                    tmp[key] = data[key]
            print(tmp, file=sys.stderr)

            columns = ', '.join(tmp.keys())
            placeholders = ':'+', :'.join(tmp.keys())
            query = 'UPDATE players ({}) VALUES ({}) WHERE name = ({})'.format(columns, placeholders, session['username'])
            print(query, file=sys.stderr)

            db.execute(query, tmp)
            db.commit()
        else:
            return jsonify({"error":"Invalid Token!"})
    except Exception as e:
        return jsonify({"error":str(e)}), 500
    return jsonify({"result":"success"})

# Work in progress... see contract for expected results

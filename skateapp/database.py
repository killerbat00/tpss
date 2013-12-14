from skateapp import app
from contextlib import closing
import sqlite3
import os
from flask import g

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE_URI'])
    rv.row_factory = sqlite3.Row
    return rv

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = connect_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

if not os.path.exists(app.config['DATABASE_URI']):
    init_db()

from skateapp import app
from contextlib import closing
import sqlite3
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

init_db()

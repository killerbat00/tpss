from skateapp import app, utils
from contextlib import closing
import sqlite3, os
from flask import g, session

class User(object):
    def __init__(self, uname, pw):
        self.username = uname
        self.password = utils.encrypt(pw)

    def login(self):
        cur = query_db('select * from users where username = ? and password = ?', [self.username, self.password], one=True)
        if cur == None:
            return False
        if cur[1] == 'bmorrow':
            if cur[3] == 1:
                session['is_admin'] = True
            session['active'] = True
            return True

    def logout(self):
        if session.get('active'):
            session['active'] = False
        if session.get('is_admin'):
            session['is_admin'] = False
        return

def connect_db():
    rv = sqlite3.connect(app.config['DATABASE_URI'])
    rv.row_factory = sqlite3.Row
    return rv

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_db()
    return db

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

if not os.path.exists(app.config['DATABASE_URI']):
    init_db()

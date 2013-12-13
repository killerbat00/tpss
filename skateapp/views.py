from skateapp import app
from database import *
from flask import render_template, flash

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    cur = g.db.execute('select * from spots')
    spots = cur.fetchall()
    return render_template('index.html', spots=spots)

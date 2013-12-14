from skateapp import app
from database import *
from flask import render_template, flash, url_for

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/list')
def list():
    cur = query_db('select * from spots')
    return render_template('list.html', spots=cur)

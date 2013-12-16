from skateapp import app
from database import *
from flask import render_template, flash, url_for, request, redirect, abort
from flask.ext.login import login_required

@app.before_request
def before_request():
    g.db = get_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/')
def home():
    return render_template('map.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['email'] == app.config['ADMIN_USER'] and request.form['password'] == app.config['ADMIN_PW']:
            session['active'] = True
            return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/secret')
def secret():
    if session.get('active'):
        return redirect(url_for('home'))
    else:
        abort(404)

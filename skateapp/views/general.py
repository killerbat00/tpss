from flask import Blueprint, render_template, flash, url_for, request, redirect, abort, session, g
from flask.ext.login import login_required
from skateapp import app, utils
from skateapp.database import database

mod = Blueprint('general', __name__)

@mod.route('/')
def index():
    return render_template('general/map.html')

@mod.route('/about/')
def about():
    return render_template('general/about.html')

@mod.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['email']
        pwd = request.form['password']
        user = database.User(uname, pwd)
        if user.login() == True:
            session['user'] = user.__dict__
            return redirect(url_for('general.index'))
        else:
            return redirect(url_for('general.login'))
    return render_template('general/login.html')

@mod.route('/logout/')
def logout():
    if session['user'] is not None:
        user = database.User(session['user'].get('username'), session['user'].get('password'))
        user.logout()
        session['user'] = None
    return redirect(url_for('general.index'))

@mod.route('/secret/')
def secret():
    if session['user'] is not None:
        if session['active'] == True:
            return render_template('general/secret.html')
    else:
        abort(403)

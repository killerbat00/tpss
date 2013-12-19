from flask import Blueprint, render_template, flash, url_for, request, redirect, abort, session, g
from skateapp import app
from skateapp.utils import requires_login
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
            flash(u'You have successfully logged in.')
            g.user = user
            return redirect(url_for('general.index'))
        else:
            flash(u'Username or password is incorrenct.')
            return redirect(url_for('general.login'))
    return render_template('general/login.html')

@mod.route('/logout/')
def logout():
    if g.user is not None:
        g.user.logout()
        flash(u'You have successfully logged out.')
    return redirect(url_for('general.index'))

@mod.route('/dashboard/')
@requires_login
def dashboard():
    return render_template('general/dashboard.html')

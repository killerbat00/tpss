from flask import Blueprint, render_template, flash, url_for, request, redirect, abort, session
from flask.ext.login import login_required
from skateapp import app

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
        if request.form['email'] == app.config['ADMIN_USER'] and request.form['password'] == app.config['ADMIN_PW']:
            session['active'] = True
            return redirect(url_for('general.index'))
        else:
            return redirect(url_for('general.login'))
    return render_template('general/login.html')

@mod.route('/logout/')
def logout():
    if 'active' in session:
        del session['active']
    return redirect(url_for('general.index'))

@mod.route('/secret/')
def secret():
    if session.get('active'):
        return render_template('general/secret.html')
    else:
        abort(403)

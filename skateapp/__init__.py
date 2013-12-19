from flask import Flask, render_template, session, g, flash
import os
import config

app = Flask(__name__)
env = os.environ['ENV'].lower()

if not env:
    app.config.from_object(config.Config())

if env == 'dev':
    app.config.from_object(config.DevelopmentConfig())
elif env == 'test':
    app.config.from_object(config.TestingConfig())
else:
    app.config.from_object(config.Config())

#jinja_env.globals.update('version',app.config['VERSION'])

@app.errorhandler(403)
def access_denied(e):
    flash(u'You can\'t go there.')
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    flash(u'That page doesn\'t exist.')
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    flash(u'The server has exploded. Great.')
    return render_template('errors/500.html'), 500

from skateapp.database import database
@app.before_request
def before_request():
    g.db = database.get_db()
    try:
        i = session['user_id']
    except KeyError, e:
        g.user = None
        session['user_id'] = None
    finally:
        a = g.db.execute('select * from users where id = ?', [i]).fetchone()
        if a is not None:
            g.user = database.User(a[1], a[2])
        else:
            g.user = None
            session['user_id'] = None

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from skateapp.views import general
from skateapp.views import api

app.register_blueprint(general.mod)
app.register_blueprint(api.mod)

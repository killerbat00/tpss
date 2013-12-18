from flask import Flask, session, g, render_template
import os
import config

app = Flask(__name__)

if not os.environ['ENV']:
    app.config.from_object(config.Config())

if os.environ['ENV'].lower() == 'dev':
    app.config.from_object(config.DevelopmentConfig())
elif os.environ['ENV'].lower() == 'test':
    app.config.from_object(config.TestingConfig())
else:
    app.config.from_object(config.Config())

@app.errorhandler(403)
def access_denied(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('errors/500.html'), 500

@app.before_request
def before_request():
    g.db = get_db()
    g.user = None

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

from skateapp.views import general
from skateapp.views import api

app.register_blueprint(general.mod)
app.register_blueprint(api.mod)

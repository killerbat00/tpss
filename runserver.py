from skateapp import app
from flask.ext.login import *

login_manager = LoginManager()
login_manager.login_view = "/login"
login_manager.init_app(app)

app.run(host='0.0.0.0')

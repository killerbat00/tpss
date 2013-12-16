from skateapp import app
from database import *
from flask.ext.login import *

class User(UserMixin):
    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def register(self):
        pass


from flask import Flask
import os
import config
from flask.ext.login import *

app = Flask(__name__)

if not os.environ['ENV']:
    app.config.from_object(config.Config())

if os.environ['ENV'].lower() == 'dev':
    app.config.from_object(config.DevelopmentConfig())
elif os.environ['ENV'].lower() == 'test':
    app.config.from_object(config.TestingConfig())
else:
    app.config.from_object(config.Config())

import api

from flask import Flask
import os
import config

app = Flask(__name__)
if os.environ['ENV'] == 'dev' or os.environ['ENV'] =='DEV':
    app.config.from_object(config.DevelopmentConfig())

import skateapp.views

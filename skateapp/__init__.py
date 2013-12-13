from flask import Flask
import os
import config

app = Flask(__name__)

if os.environ['ENV'].lower() == 'dev':
    app.config.from_object(config.DevelopmentConfig())
elif os.environ['ENV'].lower() == 'test':
    app.config.from_object(config.TestingConfig())
else:
    app.config.from_object(config.Config())

import views

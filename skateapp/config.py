import logging
import os
from datetime import timedelta

project_name = "skateapp"

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = "/tmp/%s_default.sqlite" % project_name
    SECRET_KEY = "skateappskateapp"

class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URI = "/tmp/%s_dev.sqlite" % project_name
    ADMIN_USER='bmorrow'
    ADMIN_PW='f56/SQdUyq6tOI+8nB/E0g=='

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "/tmp/%s_test.sqlite" % project_name

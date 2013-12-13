import logging
import os
from datetime import timedelta

project_name = "skateapp"

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = "/tmp/%s_dev.sqlite" % project_name
    SECRET_KEY = os.urandom(24)
    LOGGER_NAME = "%s_log" % project_name
    LOG_FILENAME = "%s.log" % project_name
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s %(levelname)s\t: %(message)s"

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    DATABASE_URI = "/tmp/%s_test.sqlite" % project_name

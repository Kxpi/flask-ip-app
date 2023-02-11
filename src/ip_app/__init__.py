"""Responsible for configuring and starting an app"""
import logging
from os import environ
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from .routes import api
from .extensions import db


# default address for testing purposes
DEFAULT_DB_URI = 'postgresql://postgres:postgres@localhost:5432/IP'


def create_app():
    """
    Configure and initialize an app
    """
    logging.basicConfig(level=logging.DEBUG)

    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URI', DEFAULT_DB_URI)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Limiter(app, key_func = get_remote_address, # pylint: disable=E1124
            default_limits = [
            '15 per minute',
            '100 per hour',
            '500 per day'])

    with app.app_context():
        db.init_app(app)
        try:
            db.create_all()
        except Exception as err:
            logging.exception('Exception while creating table - %s', err)
    return app

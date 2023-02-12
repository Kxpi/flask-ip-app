"""Responsible for creating and configuring an app."""
import logging
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from ip_app.routes import api


# initial query when starting an app and connecting to database
INIT_QUERY = 'CREATE TABLE IF NOT EXISTS ip_addresses(ip_addr VARCHAR(16) UNIQUE)'


def create_app():
    """
    Creates and configures the app.
    """
    # set Flask server log level to errors only
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # create custom logger
    logging.basicConfig(format='%(asctime)s - %(levelname)s: %(message)s',
        datefmt='%H:%M:%S-%d/%m/%Y ',
        level=logging.DEBUG)

    # configure app, add blueprint routes
    app = Flask(__name__)
    app.register_blueprint(api, url_prefix='/')

    # configure rate limiting per client IP address
    Limiter(
        get_remote_address,
        app = app,
        default_limits = ['15 per minute', '100 per hour', '250 per day'])

    return app

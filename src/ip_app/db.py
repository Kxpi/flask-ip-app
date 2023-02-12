"""Creates connection to database based on provided env vars or default values."""
import sys
from os import environ
from redis import Redis


REDIS_HOST = environ.get('REDIS_HOST', 'redis')
REDIS_PASS = environ.get('REDIS_PASS', 'password')
REDIS_PORT = int(environ.get('REDIS_PORT', 6379))
REDIS_SET_NAME = 'ip_addresses'

try:
    redis_client = Redis(
        host = REDIS_HOST,
        port = REDIS_PORT,
        db = 0)
except Exception as e:
    sys.exit(e)

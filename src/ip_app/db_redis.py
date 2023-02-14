"""Module with functions used for database related operations."""
import logging
from os import environ
from typing import Iterator
from redis import Redis, ConnectionPool, exceptions


REDIS_HOST = environ.get('REDIS_HOST', 'redis')
REDIS_PASS = environ.get('REDIS_PASS', 'password')
REDIS_PORT = int(environ.get('REDIS_PORT', 6379))
REDIS_SET_NAME = 'ip_addresses'

POOL = ConnectionPool(
        host = REDIS_HOST,
        port = REDIS_PORT,
        db = 0,
        decode_responses=True)


def add_ip(client_ip: str) -> None:
    """
    Add record with IP address to database.
    """
    try:
        redis_client = Redis(connection_pool = POOL)
        redis_client.sadd(REDIS_SET_NAME, client_ip)
    except (exceptions.RedisError, exceptions.ConnectionError):
        logging.exception('Failed to connect with redis')


def get_all_ips() -> Iterator[str]:
    """
    Return all records stored in database.
    """
    try:
        redis_client = Redis(connection_pool = POOL)
        for ip in redis_client.smembers(REDIS_SET_NAME): # pylint: disable=C0103
            yield ip
    except (exceptions.RedisError, exceptions.ConnectionError):
        logging.exception('Failed to connect with redis')

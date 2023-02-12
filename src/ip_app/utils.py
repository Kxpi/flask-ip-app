"""Module with functions used for database related operations"""
from typing import Iterator

from ip_app.db import redis_client, REDIS_SET_NAME


def add_ip(client_ip: str) -> None:
    """
    Add record with IP address to database.
    """
    redis_client.sadd(REDIS_SET_NAME, client_ip)


def get_all_ips() -> Iterator[str]:
    """
    Return all records stored in database.
    """
    for ip in redis_client.smembers(REDIS_SET_NAME): # pylint: disable=C0103
        yield ip.decode('utf-8')

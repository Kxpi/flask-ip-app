"""Module with functions used for database related operations"""
from .models import IP
from .extensions import db


def check_for_ip(client_ip: str) -> bool:
    """
    Check if IP doesn't exist already in database
    """
    return bool(db.session.query(IP).filter_by(ip_addr = client_ip).first())


def insert_ip(client_ip: str):
    """
    Add record with IP address to database 
    """
    new_record = IP(client_ip)
    db.session.add(new_record)


def get_all_ips(accept_header: str) -> str:
    """
    Return all records stored in database in given format
    """
    return accept_header

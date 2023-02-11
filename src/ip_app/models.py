"""Contains SQLAlchemy model for database operations""" 
from .extensions import db

# pylint: disable=R0903
class IP(db.Model):
    """
    Model for IP table with one column - client's IP addresses
    """
    __tablename__ = 'ip_address'
    ip_addr = db.Column(db.String(16), primary_key=True)

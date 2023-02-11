"""Module with routes for API endpoints"""
from flask import request, Blueprint, Response

from .utils import check_for_ip, insert_ip, get_all_ips


api = Blueprint('api', __name__)


@api.route('/get-ip', methods=['GET'])
def get_client_ip() -> Response:
    """
    Return IP address of requesting client,
    insert to database if not present
    """
    accept_header = request.headers.get('Accept', 'text/plain')

    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    if not check_for_ip(client_ip):
        insert_ip(client_ip)

    if accept_header == 'text/xml':
        return f'<client_ip>{client_ip}</client_ip>'
    if accept_header == 'application/yaml':
        return f'client_ip: {client_ip}'
    if accept_header == 'text/html':
        return f'<html><body><p>{client_ip}</p></body></html>'
    return client_ip

@api.route('/get-ip-list', methods=['GET'])
def get_ip_list() -> Response:
    """
    Return list of all IP addresses stored in database
    """
    accept_header = request.headers.get('Accept', 'text/plain')
    return_str = get_all_ips(accept_header)

    return Response(return_str)

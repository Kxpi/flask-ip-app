"""Module with routes for API endpoints."""
import logging
from flask import request, Blueprint, Response

from ip_app.db_redis import add_ip, get_all_ips


api = Blueprint('api', __name__)


@api.route('/get-ip', methods=['GET'])
def get_client_ip() -> Response:
    """
    Return IP address of requesting client,
    insert to database if not present.
    """
    # get accept header, if not present set to text/plain
    accept_header = request.headers.get('Accept', 'text/plain')

    # retrieve client IP forwarded from behind proxy if HTTP_X_FORWARDED_FOR  is present,
    # otherwise take it straight from request
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # add IP to redis set
    add_ip(client_ip)

    # send response appropriate for each accept header
    if accept_header in ['text/xml', 'application/xml']:
        logging.info('%s - returning XML format', client_ip)
        ip_xml = f'<client_ip>{client_ip}</client_ip>'
        return Response(response = ip_xml, status = 200, mimetype = accept_header)

    if accept_header in ['text/yaml', 'text/x-yaml', 'application/x-yaml']:
        logging.info('%s - returning YAML format', client_ip)
        ip_yaml = f'client_ip: {client_ip}'
        return Response(response = ip_yaml, status = 200, mimetype = accept_header)

    if accept_header == 'text/html':
        logging.info('%s - returning HTML format', client_ip)
        ip_html = f'<html><body><p>{client_ip}</p></body></html>'
        return Response(response = ip_html, status = 200, mimetype = accept_header)

    logging.info('%s - returning plain text', client_ip)
    return Response(response = client_ip, status = 200, mimetype = accept_header)


@api.route('/get-ip-list', methods=['GET'])
def get_ip_list() -> Response:
    """
    Return list of all IP addresses stored in database.
    """
    # get accept header, if not present set to text/plain
    accept_header = request.headers.get('Accept', 'text/plain')

    # retrieve client IP forwarded from behind proxy if HTTP_X_FORWARDED_FOR  is present,
    # otherwise take it straight from request
    client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

    # add IP to redis set
    add_ip(client_ip)

    # send response appropriate for each accept header
    if accept_header in ['text/xml', 'application/xml']:
        logging.info('%s - returning list in XML format', client_ip)
        ip_list_xml = '<list>\n' + ''.join(f'<String>{ip}</String>\n' for ip in get_all_ips()) + '</list>' # pylint: disable=C0301
        return Response(response = ip_list_xml, status = 200, mimetype = accept_header)

    if accept_header in ['text/yaml', 'text/x-yaml', 'application/x-yaml']:
        logging.info('%s - returning list in YAML format', client_ip)
        ip_list_yaml = 'ip_addresses:\n' + ''.join(f'  - {ip}\n' for ip in get_all_ips())
        return Response(response = ip_list_yaml, status = 200, mimetype = accept_header)

    if accept_header == 'text/html':
        logging.info('%s - returning list in HTML format', client_ip)
        ip_list_html = '<html><body><ul>' + ''.join(f'<li>{ip}</li>' for ip in get_all_ips()) + '</ul></body></html>' # pylint: disable=C0301
        return Response(response = ip_list_html, status = 200, mimetype = accept_header)

    logging.info('%s - returning list in plain text', client_ip)
    ip_list_txt = ''.join(f'{ip}\n' for ip in get_all_ips())
    return Response(response = ip_list_txt, status = 200, mimetype = accept_header)


@api.route('/health-check', methods=['GET'])
def health_check() -> Response:
    """
    Endpoint for health check done by liveness and readiness probes.
    """
    return Response(response = 'OK', status = 200)

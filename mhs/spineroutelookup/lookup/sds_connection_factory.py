import logging
import ssl

import ldap3
from utilities import certs, config

import definitions

_LDAP_CONNECTION_RETRIES = int(config.get_config('LDAP_CONNECTION_RETRIES', default='3'))
_LDAP_CONNECTION_TIMEOUT_IN_SECONDS = int(config.get_config('LDAP_CONNECTION_TIMEOUT_IN_SECONDS', default='5'))
logger = logging.getLogger(__name__)


def build_sds_connection(ldap_address: str) -> ldap3.Connection:
    """
    Given an ldap service address this will return a ldap3 connection object
    """
    ldap3.set_config_parameter('RESTARTABLE_TRIES', _LDAP_CONNECTION_RETRIES)
    server = ldap3.Server(ldap_address, connect_timeout=_LDAP_CONNECTION_TIMEOUT_IN_SECONDS)
    logger.info('001', 'Opening LDAP connection without TLS')
    connection = ldap3.Connection(server, auto_bind=True, client_strategy=ldap3.REUSABLE)
    logger.info('002', 'LDAP connection successful')
    return connection


def build_sds_connection_tls(ldap_address: str, private_key: str, local_cert: str, ca_certs: str
                             ) -> ldap3.Connection:
    """
    This will return a connection object for the given ip along with loading the given certification files
    :param ldap_address: The URL of the LDAP server to connect to.
    :param private_key: A string containing the client private key.
    :param local_cert: A string containing the client certificate.
    :param ca_certs: A string containing certificate authority certificates
    :return: Connection object using the given cert files
    """
    certificates = certs.Certs.create_certs_files(definitions.ROOT_DIR, private_key=private_key, local_cert=local_cert,
                                                  ca_certs=ca_certs)

    load_tls = ldap3.Tls(local_private_key_file=certificates.private_key_path,
                         local_certificate_file=certificates.local_cert_path, validate=ssl.CERT_REQUIRED,
                         version=ssl.PROTOCOL_TLSv1, ca_certs_file=certificates.ca_certs_path)

    ldap3.set_config_parameter('RESTARTABLE_TRIES', _LDAP_CONNECTION_RETRIES)
    server = ldap3.Server(ldap_address, use_ssl=True, tls=load_tls, connect_timeout=_LDAP_CONNECTION_TIMEOUT_IN_SECONDS)
    logger.info('003', 'Opening LDAP connection using TLS')
    connection = ldap3.Connection(server, auto_bind=True, client_strategy=ldap3.REUSABLE)
    logger.info('004', 'LDAP connection successful')
    return connection

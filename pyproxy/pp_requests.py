from urllib.parse import urlparse

from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool

from pyproxy.const import PROXY_PROTOCOL

from .sock import ProxyProtocolSocket


class ProxyConnection(HTTPConnection):
    """Implements the actual connect using ProxyProtocolSocket"""
    def __init__(self, pp_version, host, port, src_addr=None):
        super().__init__(host)
        self.pp_version = pp_version
        self.src_addr = src_addr
        self.host = host
        self.port = port

    def connect(self):
        sock = ProxyProtocolSocket(self.pp_version, src_addr=self.src_addr)
        sock.connect((self.host, self.port))
        # pylint: disable=attribute-defined-outside-init
        self.sock = sock


class ProxyConnectionPool(HTTPConnectionPool):
    """Implements a proxy connection pool"""

    def __init__(self, pp_version, host, port, src_addr):
        super().__init__(host)
        self.pp_version = pp_version
        self.src_addr = src_addr
        self.host = host
        self.port = port

    def _new_conn(self):
        return ProxyConnection(self.pp_version, self.host, self.port,
                               self.src_addr)


class ProxyAdapter(HTTPAdapter):
    """Implements a proxy adapter"""
    def __init__(self, pp_version, src_addr):
        super().__init__()
        self.pp_version = pp_version
        self.src_addr = src_addr

    def get_connection(self, url, proxies=None):
        _url = urlparse(url)
        return ProxyConnectionPool(self.pp_version,
                                   _url.hostname,
                                   _url.port,
                                   self.src_addr)


def ProxyClient(session, pp_version=PROXY_PROTOCOL.V1, src_addr=None):
    session.mount('http://', ProxyAdapter(pp_version, src_addr=src_addr))
    session.mount('https://', ProxyAdapter(pp_version, src_addr=src_addr))
    return session

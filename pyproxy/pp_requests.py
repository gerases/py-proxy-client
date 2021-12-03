import requests
from requests.adapters import HTTPAdapter
from urllib3.connection import HTTPConnection
from urllib3.connectionpool import HTTPConnectionPool

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
    def __init__(self, pp_version, host, port, src_addr):
        super().__init__()
        self.host = host
        self.port = port
        self.pp_version = pp_version
        self.src_addr = src_addr

    def get_connection(self, url, proxies=None):
        return ProxyConnectionPool(self.pp_version, self.host, self.port,
                                   self.src_addr)


class HttpSession():
    # pylint: disable=too-many-arguments
    def __init__(self, pp_version, dst_host, dst_port, ssl=False,
                 src_addr=None):
        session = requests.Session()
        http_proto = 'http'
        if ssl:
            http_proto = 'https'
        session.mount(f'{http_proto}://',
                      ProxyAdapter(pp_version,
                                   dst_host,
                                   dst_port,
                                   src_addr=src_addr,
                                   ))
        self.session = session
        self.session_methods = [f for f in dir(session) if not
                                f.startswith('_')]

    def __getattr__(self, func):
        """
        Override the __getattr__ method to delegate calls to all
        valid methods on sessions objects to the session object

        Inspired by https://erikscode.space/index.php/
        2020/08/01/
        delegate-and-decorate-in-python-part-1-the-delegation-pattern/
        """
        def method(*args):
            if func in self.session_methods:
                return getattr(self.session, func)(*args)
            raise AttributeError
        return method

import unittest

from pyproxy.const import PROXY_PROTOCOL
from pyproxy.encode import encode_v1, encode_v2
from pyproxy.sock import ProxyProtocolSocket
from tests.integration import TestStreamServer


class ProxyProtocolV1SocketTest(unittest.TestCase):
    def setUp(self):
        self.mock_server = TestStreamServer()
        self.mock_server.start()
        self.client_port = 1000
        self.client_ip = '1.1.1.1'
        self.server_host = self.mock_server.server_host
        self.server_port = self.mock_server.server_port
        print(f'Test server running on {self.server_host}:{self.server_port}')
        src_addr = (self.client_ip, self.client_port)
        self.v1_sock = ProxyProtocolSocket(PROXY_PROTOCOL.V1,
                                           src_addr=src_addr)
        self.v2_sock = ProxyProtocolSocket(PROXY_PROTOCOL.V2,
                                           src_addr=src_addr)

    def tearDown(self):
        # self.mock_server.stop()
        self.mock_server.join(timeout=0.1)
        self.v1_sock.close()
        self.v2_sock.close()

    @property
    def mock_server_address(self):
        return (self.mock_server.server_host, self.mock_server.server_port)

    def test_proxy_protocol_v1(self):

        self.v1_sock.connect(self.mock_server_address)
        resp = self.v1_sock.recv(1024)

        header = encode_v1(PROXY_PROTOCOL.TCP4,
                           self.client_ip,
                           self.server_host,
                           self.client_port,
                           self.server_port)

        self.assertEqual(header.strip(), resp)

        self.v1_sock.sendall(b'Hello world')
        resp = self.v1_sock.recv(1024)
        self.assertEqual('Hello world', resp.decode('ascii'))

    def test_proxy_protocol_v2(self):
        self.v2_sock.connect(self.mock_server_address)
        resp = self.v2_sock.recv(1024)
        header = encode_v2(PROXY_PROTOCOL.TCP4,
                           self.client_ip,
                           self.server_host,
                           self.client_port,
                           self.server_port)

        self.assertEqual(header.strip(), resp)

        self.v2_sock.sendall(b'Hello world')
        resp = self.v2_sock.recv(1024)
        self.assertEqual('Hello world', resp.decode('ascii'))

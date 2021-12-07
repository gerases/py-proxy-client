"""
This file contains methods and utilities for creating a raw TCP connection
which uses the proxy protocol
"""
import socket

from pyproxy import encode
from pyproxy.const import TCP4, V1, V2
from pyproxy.error import ProxyProtocolError


class ProxyProtocolSocket(socket.socket):
    """
    Subclass of native python sockets which will speak proxy protocol
    v1 or v2 to the receiver
    """

    # pylint: disable=no-member
    def __init__(self, pp_version, family=socket.AF_INET,
                 sock_type=socket.SOCK_STREAM, src_addr=None):
        """
        :param pp_version: Proxy protocol version, from the const module
        :param family: Socket family
        :param sock_type: Socket transport sock_type
        :param src_addr: Set a source address to send in proxy protocol header,
            defaults to socket's source address after connection.
        """
        if pp_version not in (V1, V2):
            raise ValueError(f'Invalid version "{pp_version}"')

        self.proxy_version = pp_version
        self.pp_src_ip = self.pp_src_port = None

        if src_addr:
            try:
                self.pp_src_ip, self.pp_src_port = src_addr
            except (TypeError, ValueError) as e:
                raise ValueError(f'Invalid src_addr "{src_addr}".'
                                 ' Must be tuple of form (ip, port).') from e

            if not isinstance(self.pp_src_port, int):
                raise ValueError(f'Invalid port "{self.pp_src_port}" provided'
                                 ' in src_addr. Must be an integer.')

        super().__init__(family, sock_type)

    def _send_pp_header(self):
        """
        Sends the proxy protocol header through the socket to the remote
        machine.
        """
        dst_ip, dst_port = self.getpeername()
        if not self.pp_src_ip or not self.pp_src_port:
            self.pp_src_ip, self.pp_src_port = self.getsockname()

        if self.proxy_version == V1:
            header = encode.encode_v1(TCP4,
                                      self.pp_src_ip, dst_ip,
                                      self.pp_src_port, dst_port)
        else:
            header = encode.encode_v2(TCP4,
                                      self.pp_src_ip, dst_ip,
                                      self.pp_src_port, dst_port)

        self.sendall(header)

    def connect(self, address):
        """
        Initiate a connection to address

        :param address:     Tuple describing the address to connect to
        """
        super().connect(address)
        try:
            self._send_pp_header()
        except Exception as e:
            self.close()
            raise ProxyProtocolError(
                'Failed to send proxy protocol header',
                e
            ) from e

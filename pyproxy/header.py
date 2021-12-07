"""
This file contains methods and utilities for encoding a proxy protocol header
"""

import socket
import struct
from socket import AF_INET, AF_INET6

from pyproxy.const import V1


class HeaderEncoder:
    """
    Produce a connection header according to the protocol version

    See: https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt
    """
    # pylint: disable=too-many-arguments
    def __init__(self, proxy_proto, family, src_ip, dst_ip, src_port,
                 dst_port):
        """
        :param proxy_proto: str corresponding to either V1 or V2 constant
        :param family: int corresponding to either socket.AF_INET or
            socket.AF_INET6
        :param src_ip: str the ip address of the sender, either ipv4 or ipv6
        :param dst_ip: str the ip address of the receiver, either ipv4 or ipv6
        :param src_port: int the port of the receiver
        :param dst_port: int the port of the sender
        :returns binary string header in proxy protocol v1 format to send upon
            establishing a connection.
        """
        self.proxy_proto = proxy_proto
        self.family = family
        self.src_ip = src_ip
        self.dst_ip = dst_ip
        self.src_port = src_port
        self.dst_port = dst_port
        if family not in (AF_INET, AF_INET6):
            raise ValueError(f'Unknown protocol {family}')

    def encode(self):
        if self.proxy_proto == V1:
            return self.encode_v1()
        return self.encode_v2()

    def encode_v1(self):
        """Build v1 header"""
        if self.family == AF_INET:
            family_str = 'TCP4'
        else:
            family_str = 'TCP6'
        pieces = [
            'PROXY',
            family_str,
            self.src_ip,
            self.dst_ip,
            str(self.src_port),
            str(self.dst_port),
                ]
        header = f"{' '.join(pieces)}\r\n"
        return header.encode('ascii')

    # pylint: disable=too-many-locals
    def encode_v2(self):
        """Build v2 header"""
        sig = b'\x0D\x0A\x0D\x0A\x00\x0D\x0A\x51\x55\x49\x54\x0A'
        ver_cmd = b'\x21'  # version 2, cmd=PROXY
        if self.family == AF_INET:
            src_addr = socket.inet_aton(self.src_ip)
            dst_addr = socket.inet_aton(self.dst_ip)
            fam = b'\x11'  # TCP over IPv4
            addr_len_bytes = 4
        elif self.family == AF_INET6:
            src_addr = socket.inet_pton(AF_INET6, self.src_ip)
            dst_addr = socket.inet_pton(AF_INET6, self.dst_ip)
            fam = b'\x21'  # TCP over IPv6
            addr_len_bytes = 16
        else:
            raise NotImplementedError
        # Length of the content starting with the address/port information
        # length of 2 addresses + length of 2 ports (two bytes each)
        var_content_len = addr_len_bytes * 2 + 4
        fmt = '! 12s s s H {addr_len_bytes}s {addr_len_bytes}s H H'.\
            format(addr_len_bytes=addr_len_bytes)
        header = (sig, ver_cmd, fam, var_content_len,
                  src_addr,
                  dst_addr,
                  self.src_port,
                  self.dst_port,
                  )
        s = struct.Struct(fmt)
        return s.pack(*header)

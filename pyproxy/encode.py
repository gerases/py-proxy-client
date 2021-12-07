"""
This file contains methods and utilities for encoding a proxy protocol header
"""

import socket
import struct
from socket import AF_INET6

from pyproxy.const import TCP4, TCP6


def encode_v1(protocol, src_ip, dst_ip, src_port, dst_port):
    """
    Produce a Proxy Protocol V1 connection header according to
    https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt

    :param protocol: str one of TCP4, TCP6, UNKNOWN
    :param src_ip: str the ip address of the sender, either ipv4 or ipv6
    :param dst_ip: str the ip address of the receiver, either ipv4 or ipv6
    :param src_port: int the port of the receiver
    :param dst_port: int the port of the sender
    :returns binary string header in proxy protocol v1 format to send upon
        establishing a connection.
    """
    prot = protocol.upper()
    assert prot in (TCP4,
                    TCP6,
                    'UNKNOWN'), 'Unknown protocol {prot}'
    header = f'PROXY {prot} {src_ip} {dst_ip} {src_port} {dst_port}\r\n'
    return header.encode('ascii')


# pylint: disable=too-many-locals
def encode_v2(protocol, src_ip, dst_ip, src_port, dst_port):
    """
    Produce a Proxy Protocol V2 connection header according to
    https://www.haproxy.org/download/1.8/doc/proxy-protocol.txt
    """
    prot = protocol.upper()
    assert prot in (TCP4,
                    TCP6,
                    'UNKNOWN'), 'Unknown protocol {prot}'

    sig = b'\x0D\x0A\x0D\x0A\x00\x0D\x0A\x51\x55\x49\x54\x0A'
    ver_cmd = b'\x21'  # version 2, cmd=PROXY
    if prot == TCP4:
        src_addr = socket.inet_aton(src_ip)
        dst_addr = socket.inet_aton(dst_ip)
        fam = b'\x11'  # TCP over IPv4
        addr_len_bytes = 4
    elif prot == TCP6:
        src_addr = socket.inet_pton(AF_INET6, src_ip)
        dst_addr = socket.inet_pton(AF_INET6, dst_ip)
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
              src_port,
              dst_port)
    s = struct.Struct(fmt)
    return s.pack(*header)

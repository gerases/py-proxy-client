#!/usr/bin/env python

import textwrap
import pyproxy
from pyproxy.sock import ProxyProtocolSocket


def send_directly_via_socket(proto):
    server_host = '9.9.9.9'
    server_port = 9000
    # Create a new socket that speaks proxy protocol
    sock = ProxyProtocolSocket(proto, src_addr=(server_host, server_port))

    message = "GET /test HTTP/1.0\n\n"

    # Connect to it - This sends the proxy protocol header
    sock.connect(('127.0.0.1', 2081))

    # Send data as usual
    sock.send(textwrap.dedent(message).encode('ascii'))

    # Receive a response
    res = sock.recv(4096)
    print(res)


send_directly_via_socket(pyproxy.const.PROXY_PROTOCOL.V1)
send_directly_via_socket(pyproxy.const.PROXY_PROTOCOL.V2)

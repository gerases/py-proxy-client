#!/usr/bin/env python

import pyproxy
from pyproxy.pp_requests import HttpSession


def send_via_requests(proto):
    server_host = '9.9.9.9'
    server_port = 9000

    session = HttpSession(proto,
                          dst_host='127.0.0.1',
                          dst_port=2081,
                          src_addr=(server_host, server_port))

    resp = session.get('http://test')
    print(resp.content)


send_via_requests(pyproxy.const.PROXY_PROTOCOL.V1)
send_via_requests(pyproxy.const.PROXY_PROTOCOL.V2)

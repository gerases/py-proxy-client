#!/usr/bin/env python

import requests
from pyproxy.adapter import ProxyClient
from pyproxy.const import V1, V2


def send_via_requests(proto):
    server_host = '9.9.9.9'
    server_port = 9000

    session = ProxyClient(requests.session(),
                          proto, src_addr=(server_host, server_port))

    resp = session.get('http://127.0.0.1:2081')
    print(resp.content)


send_via_requests(V1)
send_via_requests(V2)

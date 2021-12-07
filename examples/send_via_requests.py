#!/usr/bin/env python

import requests
from pyproxy.adapter import ProxyClient
from pyproxy.const import V1, V2


def send_via_requests(pp_proto):
    server_host = '9.9.9.9'
    server_port = 9000

    # ask to wrap a requests session into our adapter
    session = ProxyClient(requests.session(),
                          pp_proto,
                          src_addr=(server_host, server_port))

    # interact with the session as usual
    resp = session.get('http://127.0.0.1:2081')
    print(resp.content)


send_via_requests(V1)
send_via_requests(V2)

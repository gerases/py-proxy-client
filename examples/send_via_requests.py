#!/usr/bin/env python

import requests
import pyproxy
from pyproxy.pp_requests import ProxyClient


def send_via_requests(proto):
    server_host = '9.9.9.9'
    server_port = 9000

    session = requests.session()
    session = ProxyClient(session, proto, src_addr=(server_host, server_port))

    resp = session.get('http://127.0.0.1:2081')
    print(resp.content)


send_via_requests(pyproxy.const.PROXY_PROTOCOL.V1)
send_via_requests(pyproxy.const.PROXY_PROTOCOL.V2)

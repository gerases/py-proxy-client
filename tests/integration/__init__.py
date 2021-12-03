from threading import Thread

import six
from gevent.server import StreamServer

if six.PY2:
    import SocketServer
else:
    import socketserver as SocketServer


class MockStreamServer(StreamServer):

    def __init__(self):
        super().__init__(('127.0.0.1', 0))

        self.last_message = None

    # pylint: disable=method-hidden
    def handle(self, socket, address):
        print('Handling connection!')
        self.last_message = socket.recv(1024)
        socket.sendall(f'Hello {address}')
        # socket.close()


class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.

    Once handle returns the underlying TCPServer will close the connection
    """

    def handle(self):
        while True:
            # self.request is the TCP socket connected to the client
            data = self.request.recv(1024).strip()
            if not data:
                print('Client closed connection')
                break

            # just send back the same data
            print(f'GOT: {data}')
            self.request.sendall(data)


class TestStreamServer(Thread):
    daemon = True

    def __init__(self):
        super().__init__()
        self.server = SocketServer.TCPServer(('127.0.0.1', 0), MyTCPHandler)
        self.server_host, self.server_port = self.server.server_address

    def run(self):
        self.server.serve_forever()

import unittest
from socket import AF_INET

from pyproxy.const import V1
from pyproxy.header import HeaderEncoder


class EncodeV1Test(unittest.TestCase):

    def test_encodes_exact_bytes(self):
        encoder = HeaderEncoder(V1,
                                AF_INET,
                                '1.1.1.1',
                                '2.2.2.2',
                                1000,
                                80,
                                )
        header = encoder.encode()
        expected_header = b'\x50\x52\x4F\x58\x59'               # 'PROXY'
        expected_header += b'\x20'                              # ' '
        expected_header += b'\x54\x43\x50\x34'                  # 'TCP4'
        expected_header += b'\x20'                              # ' '
        expected_header += b'\x31\x2e\x31\x2e\x31\x2e\x31'      # '1.1.1.1'
        expected_header += b'\x20'                              # ' '
        expected_header += b'\x32\x2e\x32\x2e\x32\x2e\x32'      # '2.2.2.2'
        expected_header += b'\x20'                              # ' '
        expected_header += b'\x31\x30\x30\x30'                  # '1000'
        expected_header += b'\x20'                              # ' '
        expected_header += b'\x38\x30'                          # '80'
        expected_header += b'\x0d\x0a'                          # '\r\n'

        self.assertEqual(expected_header, header)

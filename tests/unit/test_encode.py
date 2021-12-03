import unittest

from pyproxy.const import PROXY_PROTOCOL
from pyproxy.encode import encode_v1


class EncodeV1Test(unittest.TestCase):

    def test_encodes_exact_bytes(self):
        header = encode_v1(PROXY_PROTOCOL.TCP4, '1.1.1.1', '2.2.2.2', 1000, 80)
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

#!/usr/bin/python3

import proxy
import unittest

class TestProxy(unittest.TestCase):
    def test_request_deparse_no_options(self):
        request = proxy.HTTPRequest("GET", 
                proxy.URI("http://www.example.com"))
        expected = "GET http://www.example.com HTTP/1.1\r\n\r\n"
        actual = request.deparse()
        print("EXPECTED: %s" % repr(expected))
        print("ACTUAL: %s" % repr(actual))
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/python3

import proxy
import unittest
import subprocess
import signal
import time
import random
import socket

class TestProxy(unittest.TestCase):
    def test_listen_for_client(self):
        # Choose port
        port = random.randrange(10000,40000)
        print('proxy port: %d' % port)
        
        # Start proxy
        proc = subprocess.Popen(['./proxy.py', '-p', str(port)], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('proxy pid: %d' % proc.pid)
        time.sleep(0.5)

        # Connect client
        sock = socket.socket()
        sock.settimeout(1)
        try:
            sock.connect(('127.0.0.1', port))
            request_str = 'http://localhost HTTP/1.1\r\n\r\n'
            print('client request: %s' % repr(request_str))
            sock.send(request_str.encode())
            response_str = sock.recv(4096).decode()
            print('proxy response: %s' % repr(response_str))
            self.assertEqual(response_str, 'HTTP/1.1 400 Bad Request\r\n\r\n')
        finally:
            sock.close()

            # End proxy
            proc.send_signal(signal.SIGINT)
            print('proxy stdout: %s' % proc.stdout.read())
            proc.stdout.close()
            print('proxy stderr: %s' % proc.stderr.read())
            proc.stderr.close()


if __name__ == '__main__':
    unittest.main()

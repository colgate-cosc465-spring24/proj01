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
        # Choose ports
        proxy_port = random.randrange(10000,40000)
        print('proxy port: %d' % proxy_port)
        server_port = random.randrange(10000,40000)
        print('server port: %d' % server_port)
        
        # Start proxy
        proc = subprocess.Popen(['./proxy.py', '-p', str(proxy_port)], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print('proxy pid: %d' % proc.pid)
        time.sleep(0.5)

        # Interact with proxy
        client_sock = socket.socket()
        client_sock.settimeout(1)
        server_sock = socket.socket()
        server_sock.settimeout(1)
        try:
            server_sock.bind(('', server_port))
            server_sock.listen(1)
            client_sock.connect(('127.0.0.1', proxy_port))
            client_request_str = ('GET http://localhost:%d/unittest HTTP/1.1\r\n\r\n' % 
                    server_port)
            print('client request: %s' % repr(client_request_str))
            client_sock.send(client_request_str.encode())
            proxy_sock, proxy_addr = server_sock.accept()
            proxy_sock.settimeout(1)
            try:
                proxy_request_str = proxy_sock.recv(4096).decode()
                self.assertEqual(proxy_request_str, 'GET /unittest HTTP/1.1\r\n'
                        + 'Host: localhost\r\nConnection: close\r\n\r\n')
            except Exception as e:
                self.fail(e)
            finally:
                proxy_sock.close()
        except Exception as e:
            self.fail(e)
        finally:
            server_sock.close()
            client_sock.close()

            # End proxy
            proc.send_signal(signal.SIGINT)
            time.sleep(1)
            proc.send_signal(signal.SIGKILL)
            print('proxy stdout: %s' % proc.stdout.read())
            proc.stdout.close()
            print('proxy stderr: %s' % proc.stderr.read())
            proc.stderr.close()


if __name__ == '__main__':
    unittest.main()

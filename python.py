

import random
import telnetlib
import time


# 15% ip change
class RetryChangeProxyMiddleware(object):
    def process_request(self, request, spider):
        if random.choice(range(1, 100)) <= 15:
            tn = telnetlib.Telnet('127.0.0.1', 9051)
            tn.read_until("Escape character is '^]'.", 2)
            tn.write('AUTHENTICATE "<PASSWORD HERE>"\r\n')
            tn.read_until("250 OK", 2)
            tn.write("signal NEWNYM\r\n")
            tn.read_until("250 OK", 2)
            tn.write("quit\r\n")
            tn.close()
            time.sleep(10)


RetryChangeProxyMiddleware().process_request('', '')

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import simplejson
import urllib.parse
import random
import time
from datetime import datetime

from splitflap_proto import (
    ask_for_serial_port,
    splitflap_context,
)

context = ''

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def takeInput(self):
        p = ask_for_serial_port()
        with splitflap_context(p) as s:
            modules = s.get_num_modules()
            alphabet = s.get_alphabet()

            s.set_text('testing')
            time.sleep(5)

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        # logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
        #         str(self.path), str(self.headers), post_data.decode('utf-8'))
        # decoded = post_data.decode('utf-8')
        res = urllib.parse.parse_qs(self.path[2:])
        command = ''
        word = ''
        for key, value in res.items():
            command = key
            word = value[0]
        self.takeInput()
        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

def run(server_class=HTTPServer, handler_class=S, port=8080):
        logging.basicConfig(level=logging.INFO)
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        logging.info('Starting httpd...\n')
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()
        logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
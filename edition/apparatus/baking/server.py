"""Baking listener."""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import json


CODE = "yes"
OUTPUT_DIR = os.path.abspath("../../critical/")


class Saver(object):
    """Save the file."""
    def __init__(self, path, data):
        self.path = path
        self.data = data

    def check(self):
        """Check the data."""
        if self.data['code'] != CODE:
            return None
        return True
        path = "/api/bake/%s" % self.data['chapter']
        if self.path != path:
            return None
        return True

    def save(self):
        """Save the data"""
        filename = "%s.html" % self.data['chapter']
        path = os.path.join(OUTPUT_DIR, filename)
        with open(path, 'w') as output_fp:
            output_fp.write(self.data['html'])
    
class SaverHandler(BaseHTTPRequestHandler):
    def do_GET(self, *args, **kwargs):
        print("hello get")
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write(b"No data.")

    def do_POST(self, *args, **kwargs):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        json_data = json.loads(data.decode('utf8'))
        saver = Saver(self.path, json_data)
        ready = saver.check()

        if not ready:
            self.send_response(417)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(b"Junk input, failed")
            return

        saver.save()
        
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        # Send the html message
        if ready:
            self.wfile.write(b"Done")
            print("Happy")
        else:
            self.wfile.write(b"Junk input, failed")
        

def run(server_class=HTTPServer, handler_class=SaverHandler):
    server_address = ('', 8888)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()

#  coding: utf-8
import SocketServer
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):

    def setup(self):
        self.end = "\n\r"
        self.protocol = "HTTP/1.0"
        self.mimes = {"css" : "text/css", "html" : "text/html"}
        self.headers = {}

    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.request_header = self.data.split("\n")[0]
        print ("Got a request of: %s\n" % self.data)
        self.parse_request()
        self.payload = self.read_file()
        self.response = "200 OK"
        self.respond()

    def parse_request(self):
        self.method, path, _ = self.request_header.split(" ")
        if path.endswith("/"):
            path += "index.html"
        self.path = "./www" + path
        print(self.path, self.method)

    def read_file(self):
        with open(self.path, "r") as f:
            return f.read()

    def respond(self):
        status_line = "%s %s" % (self.protocol, self.response)
        self.set_ctype()
        response = status_line + self.end + self.build_headers() + self.end + self.payload
        # print(response)
        self.request.sendall(response)

    def set_ctype(self):
        self.headers["Content-Type: "] = self.get_mime()

    def build_headers(self):
        return "\n".join([("%s %s%s" % (k, v, self.end)) for k, v in self.headers.iteritems()])

    def add_header(self, key, value):
        self.headers[key] = value

    def get_mime(self):
        return self.mimes[self.path.split(".")[-1]]

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

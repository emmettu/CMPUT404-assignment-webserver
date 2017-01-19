#  coding: utf-8
import SocketServer

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
        self.headers = {
            "Content-Type:" : "text/html"
        }

    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.payload = self.read_file()
        #self.headers["Content-Length:"] = len(self.payload)
        self.response = "200 OK"
        self.respond()

    def read_file(self):
        with open("./www/index.html", "r") as f:
            return f.read()

    def respond(self):
        status_line = "%s %s" % (self.protocol, self.response)
        response = status_line + self.end + self.build_headers() + self.end + self.payload
        print(response)
        self.request.sendall(response)

    def build_headers(self):
        return "\n".join([("%s %s%s" % (k, v, self.end)) for k, v in self.headers.iteritems()])

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import signal
import os
import webbrowser

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
root = os.path.dirname(__file__)



#serves index if there is no index specified
class IndexHandler(tornado.web.RequestHandler):
    def initialize(self, path):
        self.path = path
    def get(self):
        self.render(self.path + "/index.html")

class StaticHandler(tornado.web.RequestHandler):
    def initialize(self, path):
        self.path = path
    def get(self):

        ext = "."+ self.request.uri.split(".")[-1]
        mimetype = "application/octet-stream"
        if(ext == ".svg"):  mimetype = "image/svg+xml"
        if(ext == ".js"):   mimetype = "application/javascript"
        if(ext == ".html"): mimetype = "text/html"
        if(ext == ".json"): mimetype = "application/json"
        if(ext == ".png"):  mimetype = "image/png"
        if(ext == ".txt"):  mimetype = "text/plain"
        if(ext == ".py"):   mimetype = "text/x-script.phyton"
        if(ext == ".ttf"):  mimetype = "application/octet-stream"
        if(ext == ".css"):  mimetype = "text/css"

        
           
        self.set_header("Content-Type", mimetype)

        with open(self.path + self.request.uri, 'rb') as f:
            self.write(f.read())
        f.closed

        self.finish()





is_closing = False
def signal_handler(signum, frame):
    global is_closing
    logging.info('exiting...')
    is_closing = True

def try_exit(): 
    global is_closing
    if is_closing:
        # clean up here
        tornado.ioloop.IOLoop.instance().stop()
        logging.info('exit success')


def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application(
        [
            (r"/", IndexHandler, {'path': os.path.join(root, 'static')}),
            (r"/.*", StaticHandler, {'path': os.path.join(root, 'static')})
        ], 

        #(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': static_path}

        static_path=os.path.join(root, 'static'),
        debug=True
        )

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)


    #allows interupt via ctrl-c
    signal.signal(signal.SIGINT, signal_handler)
    tornado.ioloop.PeriodicCallback(try_exit, 100).start() 

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    print("view at: http://127.0.0.1:8000 \nkill process with ctrl-c \n -------------------------------")
    webbrowser.open("http://localhost:8000")

    main()






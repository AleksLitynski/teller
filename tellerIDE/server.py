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
import mimetypes
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

        extension = self.request.uri.split(".")[-1]

        mimetypes.init()
        try:
            mimetype = mimetypes.types_map["."+extension]
           
        except KeyError:
            mimetype = "application/octet-stream"

        self.set_header("Content-Type", mimetype[0])

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






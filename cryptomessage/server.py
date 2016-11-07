#!/usr/bin/env python

import os.path
import time
import uuid

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from algorithms import shuffle


import json

from datetime import date
from tornado.escape import json_decode
from tornado import gen
from tornado.httpclient import AsyncHTTPClient
from tornado.options import define, options, parse_command_line


define("port", default=8888, help="run on the given port", type=int)


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '0.0.1',
                    'last_build': date.today().isoformat()}
        self.write(json.dumps(response))


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", message='')


class MessageHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self, message):
        message = shuffle.shuffle_string(str(message))
        response = {'message': message,
                    'algorithm': 'shuffle'}
        self.write(json.dumps(response))







def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/message/([0-9a-zA-Z_]+)", MessageHandler),
            (r"/version/?", VersionHandler),
        ],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()



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
from tornado.escape import json_decode
from tornado import gen
from tornado.options import define, options, parse_command_line


define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", message='')



class UpdateHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'key': None , 'value': None }
        self.write(json.dumps(response))

    def post(self):
        json_obj = json_decode(self.request.body)

        response = {'newkey': shuffle.shuffle_string(json_obj["message"])}
        self.write(json.dumps(response))


def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
            (r"/update/", UpdateHandler),
        ],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

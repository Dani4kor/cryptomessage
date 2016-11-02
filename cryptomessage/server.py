#!/usr/bin/env python

import os.path
import time
import uuid

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape

import crypt

from tornado.options import define, options, parse_command_line


define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", message='HELLO WORLD')

    def post(self):
        message = {
            "id": str(uuid.uuid4()),
            "uncrypt-message": self.get_argument("uncrypt-message"),
        }
        self.render("index.html", message=crypt.shuffle_string(message["uncrypt-message"]))



def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", MainHandler),
        ],

        cookie_secret="12345",
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        xsrf_cookies=True,
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

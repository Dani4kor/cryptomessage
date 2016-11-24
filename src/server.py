#!/usr/bin/env python

import os
import uuid

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado import httpclient
from tornado.ioloop import IOLoop

import multiprocessing
import json

from datetime import date
from tornado.escape import json_decode
from tornado import gen
from tornado.options import define, options, parse_command_line
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import time
from datetime import timedelta
import pprint




define("port", default=8888, help="run on the given port", type=int)



@gen.coroutine
def waits():
    yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)

class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '0.0.1',
                    'last_build': date.today().isoformat()}
        self.write(json.dumps(response))

class ParseHandler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())

    def post(self):
        json_obj = json_decode(self.request.body)
        response = {'img': json_obj["message"]}
        self.write(json.dumps(response))

@gen.coroutine
def get_img(url):
    response = yield httpclient.AsyncHTTPClient().fetch(url)
    soup =  BeautifulSoup(response.body, 'html.parser')
    t = [x.get('src') for x in soup.findAll('img')]
    pprint.pprint(t[1], width=1)



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        url = 'http://spacetelescope.org/images/'
        get_img(url)
        self.render("index.html")







def main():
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/?", MainHandler),
            (r"/version/?", VersionHandler),
            (r"/parse/?", ParseHandler),
        ],

        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()

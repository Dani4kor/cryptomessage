#!/usr/bin/env python

import os
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.ioloop import IOLoop
from datetime import date

import json
import tornado.httpclient
from tornado import gen
from tornado.options import define, options, parse_command_line
from bs4 import BeautifulSoup
import time

define("port", default=8889, help="run on the given port", type=int)


@gen.coroutine
def waits():
    yield gen.Task(IOLoop.instance().add_timeout, time.time() + 1)


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = {'version': '0.0.1',
                    'last_build': date.today().isoformat()}
        self.write(json.dumps(response))


class ParseHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def post(self):
        url = self.get_body_argument('message')
        if url.startswith('http://www.'):
            url = 'http://' + url[len('http://www.'):]
        elif url.startswith('www.'):
            url = 'http://' + url[len('www.'):]
        elif not url.startswith('http://'):
            url = 'http://' + url
        images = yield get_img(url)
        self.render("index.html", image_message=images)

    get = post


@gen.coroutine
def get_img(url):
    http_client = tornado.httpclient.AsyncHTTPClient()
    try:
        response = yield http_client.fetch(url)
    except Exception as e:
        x = ['http://www.theshirtlist.com/wp-content/uploads/2016/04/Nope.png']
        raise gen.Return(x)

    soup = BeautifulSoup(response.body, 'html.parser')
    t = [x.get('src') for x in soup.findAll('img')]
    raise gen.Return(t)


class MainHandler(tornado.web.RequestHandler):
    @gen.coroutine
    def get(self):
        self.render("index.html", image_message='')

    post = get


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

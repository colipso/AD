#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 21:24:51 2017

@author: hp
"""

import tornado.ioloop
import tornado.web
import time

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_cookie('username', 'peng', expires=time.time()+900)
        nowamagic = self.get_argument('name')
        print nowamagic
        local = self.get_argument('local')
        print local
        ua = self.get_cookie('username')
        print ua
        self.write(nowamagic + local)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()